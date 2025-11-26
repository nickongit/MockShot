import json
import logging
from src.sim_client import GSProClient

logging.basicConfig(level=logging.INFO)

settings = {
    "ip_address": "nbond-pc",
    "port": 921,
}

payload = {
    "DeviceID": "Rapsodo MLM2PRO",
    "Units": "Yards",
    "ShotNumber": 1,
    "APIversion": "1",
    "BallData": {
        "Speed": 110.5,
        "SpinAxis": 3.0,
        "TotalSpin": 6000,
        "HLA": 2.5,
        "VLA": 18.0,
        "Backspin": 0,
        "SideSpin": 0,
        "CarryDistance": 0
    },

    "ShotDataOptions": {
        "ContainsBallData": True,
        "ContainsClubData": True,
        "LaunchMonitorIsReady": True,
        "LaunchMonitorBallDetected": True,
        "IsHeartBeat": False
    }
}

client = GSProClient()
try:
    client.init_socket(ip_address=settings["ip_address"], port=settings["port"])
    # compact JSON and append CRLF terminator required by GSPro
    json_payload = json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + "\r\n"
    logging.info("Test payload (string): %s", json_payload)
    client.send_msg(json_payload.encode("utf-8"))
finally:
    client.terminate_session()
