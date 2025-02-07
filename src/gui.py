import tkinter as tk
from tkinter import ttk
import random

# Club data
club_data = {
    "DR": [105, 155, 12, 2500, 250],
    "3w": [100, 145, 14, 3250, 230],
    "5w": [95, 140, 16, 3750, 215],
    "4i": [85, 125, 17, 4500, 195],
    "5i": [80, 120, 18, 5000, 180],
    "6i": [75, 115, 19, 5500, 170],
    "7i": [72, 110, 20, 6000, 160],
    "8i": [68, 105, 23, 6500, 150],
    "9i": [65, 100, 26, 7500, 140],
    "PW": [62, 90, 28, 8500, 130],
    "GW": [60, 85, 31, 9000, 110],
    "SW": [58, 80, 34, 10000, 100],
    "LW": [45, 75, 37, 10500, 90],
    "PT": [0, 0, 0, 0, 0]  # Placeholder for Putter
}

class GolfApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MockShot")
        self.geometry("800x800")
        self.configure(bg="grey")

        self.selected_club = tk.StringVar()
        self.selected_club.set("DR")

        self.create_widgets()

    def create_widgets(self):
        # Create club buttons
        button_frame = tk.Frame(self, bg="grey")
        button_frame.pack(pady=10)

        for club in club_data.keys():
            button = tk.Radiobutton(button_frame, text=club, variable=self.selected_club, value=club,
                                    indicatoron=0, width=3, height=1, command=self.update_club_data,
                                    bg="grey", fg="lightgrey", font=("Helvetica", 10, "bold"),
                                    selectcolor="darkgrey")
            button.pack(side=tk.LEFT, padx=5)

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

        self.actual_shot_titles = ["Club", "Club Speed", "Ball Speed", "Launch Angle", "Launch Dir.", "Spin Rate", "Spin Axis"]
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


    def calculate_shot(self):
        club = self.selected_club.get()
        data = club_data[club]
        shot_percent = self.shot_percent.get() / 100

        actual_club_speed = self.randomize_value(data[0] * shot_percent)
        actual_ball_speed = self.randomize_value(data[1] * shot_percent)
        actual_spin_rate = self.randomize_value(data[3] * shot_percent)
        actual_spin_axis = self.randomize_value(self.spin_axis.get(), is_zero_allowed=True)
        actual_launch_direction = self.randomize_value(self.launch_direction.get(), is_zero_allowed=True)

        labels_text = [
            club,
            round(actual_club_speed),
            round(actual_ball_speed),
            f"{data[2]:.1f}°",
            f"{actual_launch_direction:.1f}°",
            round(actual_spin_rate),
            f"{actual_spin_axis:.1f}°"
        ]
        for i, label in enumerate(self.actual_shot_labels):
            label.config(text=labels_text[i])

        # Flash the Hit Shot button
        self.flash_button()

        # Reset sliders
        self.shot_percent.set(100)
        self.launch_direction.set(0)
        self.spin_axis.set(0)


    def randomize_value(self, value, is_zero_allowed=False):
        if value == 0 and is_zero_allowed:
            return value + random.uniform(-0.5, 0.5)
        return value * (1 + random.uniform(-0.01, 0.01))

    def flash_button(self):
        current_color = self.hit_shot_button.cget("bg")
        new_color = "red" if current_color == "green" else "green"
        self.hit_shot_button.config(bg=new_color)

if __name__ == "__main__":
    app = GolfApp()
    app.mainloop()