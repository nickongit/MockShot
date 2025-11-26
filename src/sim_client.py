import socket
import logging
import json
from threading import Event
from time import sleep
import select


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Example usage
logger = logging.getLogger(__name__)

class ShotData:
    def __init__(self):
        self.api_version = "1"
        self.shot_number = 0
        self.device_data = {
            "DeviceID": "MockShot",
            "Units": "Yards",
            "ShotNumber": self.shot_number,
            "APIversion": self.api_version
        }
        self.shot_data_options = {
            "ContainsBallData": True,
            "ContainsClubData": False,
            "LaunchMonitorIsReady": True,
            "LaunchMonitorBallDetected": True,
            "IsHeartBeat": False
        }
        self.ball_data = {}

    def new_shot(self, speed, spin_axis, total_spin, hla, vla, back_spin, side_spin):

        self.ball_data = {
            "Speed": speed,
            "SpinAxis": spin_axis,
            "TotalSpin": total_spin,
            "HLA": hla,
            "VLA": vla,
            "Backspin": back_spin,
            "SideSpin": side_spin,
            "CarryDistance": 0
        }
        self.shot_number += 1
        self.device_data["ShotNumber"] = self.shot_number
        return self.payload

    @property
    def payload(self):
        return {**self.device_data, "BallData": {**self.ball_data}, "ShotDataOptions": {**self.shot_data_options}}


class GSProClient:

    successful_send = 200

    def __init__(self) -> None:
        self._socket = None
        self._connected = False
        self._shot_data = ShotData()

    def init_socket(self, ip_address: str, port: int) -> None:
        self.terminate_session()  # Ensure any existing socket is closed
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((ip_address, port))
            self._socket.settimeout(3)
            self._connected = True
            logging.info(f"Successfully connected to {ip_address}:{port}")
        except socket.error as e:
            self._connected = False
            logging.error(f"Failed to connect to {ip_address}:{port}, Exception: {e}")
            raise

    def connected(self):
        return self._connected

    def send_msg(self, payload, attempts=2):
        if self._connected:
            for attempt in range(attempts):
                try:
                    logging.info(f"Sending to GSPro data: {payload}")
                    self._socket.sendall(payload)
                    msg = self._socket.recv(2048)
                except socket.timeout:
                    logging.info('Timed out. Retrying...')
                    if attempt >= attempts-1:
                        msg =  f'Failed to send shot to GSPro after {attempts} attempts.'
                        logging.debug(msg)
                        raise
                    Event().wait(0.5)
                    continue
                except socket.error as e:
                    msg = f'GSPro Connector socket error when trying to send shot, Exception: {format(e)}'
                    logging.debug(msg)
                    raise
                except Exception as e:
                    msg = f"GSPro Connector unknown error when trying to send shot, Exception: {format(e)}"
                    logging.debug(msg)
                    raise
                else:
                    if len(msg) == 0:
                        msg = f"GSPro closed the connection"
                        logging.debug(msg)
                        raise
                    else:
                        logging.debug(f"Response from GSPro: {msg}")
                        return

    def send_shot(self) -> None:
        logging.debug(f"Sending shot: connected = {self._connected}, shot number: {self._shot_data.shot_number}")
        if self._connected:
            logging.debug(f'Send payload: {self._shot_data.payload}')
            self.send_msg(json.dumps(self._shot_data.payload).encode("utf-8"))
            # Append CRLF so GSPro receives a complete JSON message terminated correctly
            # json_payload = json.dumps(self._shot_data.payload, separators=(',', ':'), ensure_ascii=False) + "\r\n"
            # self.send_msg(json_payload.encode("utf-8"))

    def check_for_message(self):
        message = bytes(0)
        if self._connected:
            read_socket, write_socket, error_socket = select.select([self._socket], [], [], 0)
            while read_socket:
                message += self._socket.recv(1024)
                read_socket, write_socket, error_socket = select.select([self._socket], [], [], 0)
        return message

    def terminate_session(self):
        if self._socket:
            self._socket.close()
            self._socket = None
        self._connected = False
        sleep(2)
        logging.debug("Session terminated")

    def test_shot(self):
        self._shot_data.new_shot(speed=100, spin_axis=0, total_spin=7000, hla=0.0, vla=14)
        return self._shot_data.payload
