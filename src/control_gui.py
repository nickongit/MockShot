import tkinter as tk

class SliderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Slider App")
        self.geometry("600x600")

        self.button_state = 0
        self.slider_moving = False

        # Create the main button
        self.main_button = tk.Button(self, text="Back", command=self.on_button_click, width=20, height=10)
        self.main_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the vertical slider bar
        self.slider = tk.Canvas(self, width=65, height=500, bg="white")
        self.slider.place(x=50, rely=0.5, anchor=tk.CENTER)
        self.slider_rect = self.slider.create_rectangle(5, 480, 25, 500, fill="blue")

        # Create the horizontal slider bar
        self.h_slider = tk.Canvas(self, width=500, height=25, bg="white")
        self.h_slider.place(rely=0.9, x=90, anchor=tk.W)
        self.h_slider_rect1 = self.h_slider.create_rectangle(0, 5, 20, 25, fill="blue")
        self.h_slider_rect2 = self.h_slider.create_rectangle(480, 5, 500, 25, fill="blue")

        # Add marks and labels to the vertical slider bar
        self.add_marks()

        # Create the Reset button
        self.reset_button = tk.Button(self, text="Reset", command=self.reset, width=20, height=5)
        self.reset_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    def add_marks(self):
        for i in range(0, 121, 10):
            y = 500 - (i * 500 / 120)
            if i % 50 == 0:
                self.slider.create_line(0, y, 30, y, fill="black", width=2)
                if i in [0, 50, 100, 120]:
                    self.slider.create_text(45, y, text=str(i), anchor=tk.W)  # Adjusted position
            else:
                self.slider.create_line(10, y, 20, y, fill="black")

    def on_button_click(self):
        if self.button_state == 0:
            self.main_button.config(text="Down")
            self.button_state = 1
            self.stop_slider()  # Stop the vertical slider
        elif self.button_state == 1:
            self.main_button.config(text="Hit")
            self.button_state = 2
            self.start_horizontal_slider()
        elif self.button_state == 2:
            self.main_button.config(text="Back")
            self.button_state = 0
            self.stop_slider()

    def start_slider(self):
        self.slider_moving = True
        self.move_slider()

    def start_horizontal_slider(self):
        self.slider_moving = True
        self.move_horizontal_slider()

    def stop_slider(self):
        self.slider_moving = False

    def move_slider(self):
        if self.slider_moving:
            current_pos = self.slider.coords(self.slider_rect)
            if current_pos[1] > 0:
                self.slider.move(self.slider_rect, 0, -1)
                self.after(3, self.move_slider)  # Move the slider every 3 milliseconds to complete in 1.5 seconds

    def move_horizontal_slider(self):
        if self.slider_moving:
            current_pos1 = self.h_slider.coords(self.h_slider_rect1)
            current_pos2 = self.h_slider.coords(self.h_slider_rect2)
            if current_pos1[2] < 500 and current_pos2[0] > 0:
                self.h_slider.move(self.h_slider_rect1, 1, 0)
                self.h_slider.move(self.h_slider_rect2, -1, 0)
                self.after(3, self.move_horizontal_slider)  # Move the sliders every 3 milliseconds

    def reset(self):
        self.button_state = 0
        self.main_button.config(text="Back")
        self.stop_slider()
        self.slider.coords(self.slider_rect, 5, 480, 25, 500)
        self.h_slider.coords(self.h_slider_rect1, 0, 5, 20, 25)
        self.h_slider.coords(self.h_slider_rect2, 480, 5, 500, 25)

if __name__ == "__main__":
    app = SliderApp()
    app.mainloop()