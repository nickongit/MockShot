import tkinter as tk
from tkinter import messagebox
import random
import math
from src.sim_client import *
from src.settings import settings, club_data

class GolfApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MockShot")
        self.geometry("800x800")
        self.configure(bg="grey")

        self.selected_club = tk.StringVar()
        self.selected_club.set("DR")

        self.gspro_client = GSProClient()
        self.connected = False

        self.create_widgets()

    def create_widgets(self):
        # IP address input
        ip_frame = tk.Frame(self, bg="grey")
        ip_frame.pack(pady=10)
        tk.Label(ip_frame, text="SIM IP Address:", bg="grey", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        self.ip_entry = tk.Entry(ip_frame, width=20)
        self.ip_entry.pack(side=tk.LEFT, padx=5)
        self.ip_entry.insert(0, settings["ip_address"])

        # Port input (new)
        tk.Label(ip_frame, text="Port:", bg="grey", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        self.port_entry = tk.Entry(ip_frame, width=6)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.port_entry.insert(0, str(settings["port"]))

        # Connect button
        self.connect_button = tk.Button(ip_frame, text="Connect", command=self.toggle_connection, bg="blue", fg="white", font=("Helvetica", 10, "bold"))
        self.connect_button.pack(side=tk.LEFT, padx=5)

        # Create club buttons
        button_frame = tk.Frame(self, bg="grey")
        button_frame.pack(pady=10)

        for club in club_data.keys():
            club_container = tk.Frame(button_frame, bg="grey")
            club_container.pack(side=tk.LEFT, padx=5)

            button = tk.Radiobutton(club_container, text=club, variable=self.selected_club, value=club,
                                    indicatoron=0, width=3, height=1, command=self.update_club_data,
                                    bg="grey", fg="lightgrey", font=("Helvetica", 10, "bold"),
                                    selectcolor="darkgrey")
            button.pack()

            carry_distance = club_data[club][4]
            carry_label = tk.Label(club_container, text=f"{carry_distance}y", bg="grey", fg="lightgrey",
                                   font=("Helvetica", 8))
            carry_label.pack()

        # Default club data label
        self.default_data_label = tk.Label(self, text="Default club data", font=("Helvetica", 12, "bold"), bg="grey", fg="white")
        self.default_data_label.pack(pady=10)

        # Default club data display
        self.default_data_frame = tk.Frame(self, relief="solid", borderwidth=1, bg="grey")
        self.default_data_frame.pack(pady=10)

        self.default_data_titles = ["Club", "Club Speed", "Ball Speed", "Launch Angle", "Launch Dir.", "Spin Rate", "Carry Distance"]
        self.default_data_labels = []
        for title in self.default_data_titles:
            title_frame = tk.Frame(self.default_data_frame, bg="grey")
            title_frame.pack(side=tk.LEFT, padx=5)
            title_label = tk.Label(title_frame, text=title, bg="grey", fg="white", font=("Helvetica", 10, "bold"))
            title_label.pack()
            value_label = tk.Label(title_frame, width=10, height=3, relief="solid", anchor="center",
                                   font=("Helvetica", 10, "bold"), bg="grey", fg="white")
            value_label.pack()
            self.default_data_labels.append(value_label)

        # Shot % slider
        self.shot_percent = tk.DoubleVar()
        self.shot_percent.set(100)
        shot_percent_frame = tk.Frame(self, bg="grey")
        shot_percent_frame.pack(pady=10)
        tk.Label(shot_percent_frame, text="Shot %", bg="grey", fg="white", font=("Helvetica", 10, "bold")).pack(
            side=tk.LEFT)
        tk.Scale(shot_percent_frame, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.shot_percent, bg="grey",
                 fg="white", length=400).pack(side=tk.LEFT)

        # Launch direction and spin axis sliders
        sliders_frame = tk.Frame(self, bg="grey")
        sliders_frame.pack(pady=10)

        self.launch_direction = tk.DoubleVar()
        self.launch_direction.set(0)
        launch_direction_frame = tk.Frame(sliders_frame, bg="grey")
        launch_direction_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(launch_direction_frame, text="Launch Direction", bg="grey", fg="white", font=("Helvetica", 10, "bold")).pack()
        tk.Scale(launch_direction_frame, from_=-10, to=10, orient=tk.HORIZONTAL, variable=self.launch_direction, bg="grey", fg="white").pack()

        self.spin_axis = tk.DoubleVar()
        self.spin_axis.set(0)
        spin_axis_frame = tk.Frame(sliders_frame, bg="grey")
        spin_axis_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(spin_axis_frame, text="Spin Axis", bg="grey", fg="white", font=("Helvetica", 10, "bold")).pack()
        tk.Scale(spin_axis_frame, from_=-20, to=20, orient=tk.HORIZONTAL, variable=self.spin_axis, bg="grey", fg="white").pack()

        # Hit Shot button
        self.hit_shot_button = tk.Button(self, text="Hit Shot", command=self.calculate_shot, bg="green", fg="white",
                                         font=("Helvetica", 10, "bold"), width=10, height=2)
        self.hit_shot_button.pack(pady=10)

        # Actual shot data label
        self.actual_shot_label = tk.Label(self, text="Actual shot data", font=("Helvetica", 14, "bold"), bg="grey", fg="white")
        self.actual_shot_label.pack(pady=10)

        # Actual shot data display
        self.actual_shot_frame = tk.Frame(self, relief="solid", borderwidth=1, bg="grey")
        self.actual_shot_frame.pack(pady=10)

        self.actual_shot_titles = ["Club", "Club Speed", "Ball Speed", "Launch Angle", "Launch Dir.", "Back Spin", "Side Spin"]
        self.actual_shot_labels = []
        for title in self.actual_shot_titles:
            title_frame = tk.Frame(self.actual_shot_frame, bg="grey")
            title_frame.pack(side=tk.LEFT, padx=5)
            title_label = tk.Label(title_frame, text=title, bg="grey", fg="white", font=("Helvetica", 10, "bold"))
            title_label.pack()
            value_label = tk.Label(title_frame, width=5, height=2, relief="solid", anchor="center",
                                   font=("Arial", 20), bg="grey", fg="white", padx=5, pady=0)
            value_label.pack()
            self.actual_shot_labels.append(value_label)

        # Initialize with default club data
        self.update_club_data()

    def update_club_data(self):
        club = self.selected_club.get()
        data = club_data[club]
        labels_text = [club] + data[:3] + [0] + data[3:]
        for i, label in enumerate(self.default_data_labels):
            label.config(text=labels_text[i])

    def toggle_connection(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        logging.debug("Connecting to GSPro")
        ip_address = self.ip_entry.get()
        port_str = self.port_entry.get()
        try:
            port = int(port_str)
        except Exception as e:
            msg = f"Invalid port: {port_str}"
            messagebox.showerror("Connection Error", msg)
            logging.error(msg)
            return
        try:
            self.gspro_client.init_socket(ip_address=ip_address, port=port)
            self.connected = True
            self.connect_button.config(text="Disconnect", bg="red")
            logging.info("Connected to GSPro")
        except Exception as e:
            msg = f"Failed to connect to GSPro: {e}"
            messagebox.showerror("Connection Error", msg)
            logging.error(msg)

    def disconnect(self):
        if self.gspro_client:
            self.gspro_client.terminate_session()
            self.connected = False
            self.connect_button.config(text="Connect", bg="blue")
            logging.info("Disconnected from GSPro")

    def calculate_shot(self):
        club = self.selected_club.get()
        data = club_data[club]
        shot_percent = self.shot_percent.get() / 100

        actual_club_speed = self.randomize_value(data[0] * shot_percent)
        actual_ball_speed = self.randomize_value(data[1] * shot_percent)
        actual_spin_rate = self.randomize_value(data[3] * shot_percent)
        actual_spin_axis = self.randomize_value(self.spin_axis.get(), is_zero_allowed=True)
        spin_axis_rad = math.radians(actual_spin_axis)
        actual_back_spin = actual_spin_rate * math.cos(spin_axis_rad)
        actual_side_spin = actual_spin_rate * math.sin(spin_axis_rad)
        actual_launch_direction = self.randomize_value(self.launch_direction.get(), is_zero_allowed=True)

        labels_text = [
            club,
            round(actual_club_speed),
            round(actual_ball_speed),
            f"{data[2]:.1f}°",
            f"{actual_launch_direction:.1f}°",
            round(actual_back_spin),
            round(actual_side_spin)
        ]
        for i, label in enumerate(self.actual_shot_labels):
            label.config(text=labels_text[i])

        # Flash the Hit Shot button
        self.flash_button()

        # Reset sliders
        self.shot_percent.set(100)
        self.launch_direction.set(0)
        self.spin_axis.set(0)

        if self.connected:
            # Round values to safe precision for GSPro
            send_ball_speed = round(actual_ball_speed, 2)
            send_spin_axis = round(actual_spin_axis, 2)
            send_total_spin = int(round(actual_spin_rate))
            send_hla = round(actual_launch_direction, 2)
            send_vla = int(round(data[2]))
            send_back_spin = round(actual_back_spin)
            send_side_spin = round(actual_side_spin)

            self.gspro_client._shot_data.new_shot(
                speed=send_ball_speed,
                spin_axis=send_spin_axis,
                total_spin=send_total_spin,
                hla=send_hla,
                vla=send_vla,
                back_spin=send_back_spin,
                side_spin=send_side_spin,
            )
            self.gspro_client.send_shot()

    def randomize_value(self, value, is_zero_allowed=False):
        if value == 0 and is_zero_allowed:
            return value + random.uniform(-0.5, 0.5)
        return value * (1 + random.uniform(-0.01, 0.01))

    def flash_button(self):
        current_color = self.hit_shot_button.cget("bg")
        new_color = "red" if current_color == "green" else "green"
        self.hit_shot_button.config(bg=new_color)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = GolfApp()
    app.mainloop()
