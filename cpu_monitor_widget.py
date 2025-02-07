import psutil
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.geometry("300x200+10+10")

        # Set default theme
        ctk.set_appearance_mode("Dark")

        # Set the window to always be on top
        self.wm_attributes("-topmost", 1)

        # Variables to store the initial position of the mouse click
        self._offset_x = 0
        self._offset_y = 0

        # Bind mouse events
        self.bind("<Button-1>", self.start_move)  # This event triggers when the left mouse button is clicked. We use this to start the drag operation.
        self.bind("<B1-Motion>", self.on_move)  # This event triggers when the left mouse button is held down and the mouse is moved. We use this to move the window.

        # Close Button
        self.close_btn = ctk.CTkButton(
            self,
            text="×",
            width=30,
            anchor="center",
            corner_radius=0,
            fg_color="transparent",
            hover_color="#DC3545",
            command=self.on_close,
            font=ctk.CTkFont(size=17)
        )
        self.close_btn.place(relx=0, rely=0)

        # Theme Toggle Button
        self.toggle_btn = ctk.CTkButton(
            self,
            text=" Day ",
            width=30,
            height=30,
            anchor="center",
            corner_radius=0,
            fg_color="transparent",
            hover_color="#E7A911",
            command=self.toggle_theme,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.toggle_btn.place(relx=0.87, rely=0)

        # Header
        self.header = ctk.CTkLabel(
            self,
            text="System Usage",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.header.pack(side="top", padx=20, pady=20)

        # Create Metrics
        self.cpu_label = self.create_metric("CPU")
        self.memory_label = self.create_metric("Memory")
        self.disk_label = self.create_metric("Disk")

        # Update Metrics
        self.update_metrics()
    
    def start_move(self, event):
        """This method is called when the user clicks the mouse to start dragging."""
        self._offset_x = event.x
        self._offset_y = event.y

    # move window
    def on_move(self, event):
        """This method is called when the user moves the mouse while holding down the left button."""
        delta_x = event.x - self._offset_x
        delta_y = event.y - self._offset_y
        # Move the window by the distance the mouse has moved
        new_x = self.winfo_x() + delta_x
        new_y = self.winfo_y() + delta_y
        self.geometry(f"+{new_x}+{new_y}")

    # Create Metric
    def create_metric(self, name):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=5, padx=30, fill="x")
        # label
        label = ctk.CTkLabel(
            frame,
            text=name,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(side="left")
        # value
        value = ctk.CTkLabel(
            frame,
            text="0%",
            text_color="#28A745",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        value.pack(side="right")
        return value

    # Update Metrics
    def update_metrics(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        # updating usage
        self.cpu_label.configure(text=f"{cpu}%")
        self.memory_label.configure(text=f"{memory}%")
        self.disk_label.configure(text=f"{disk}%")
        # change color after certain threshold - CPU
        if cpu > 50:
            if cpu > 90:
                self.cpu_label.configure(text_color="#DC3545")
            else:
                self.cpu_label.configure(text_color="#E7A911")
        else:
            self.cpu_label.configure(text_color="#28A745")
        # memory
        if memory > 50:
            if memory > 90:
                self.memory_label.configure(text_color="#DC3545")
            else:
                self.memory_label.configure(text_color="#E7A911")
        else:
            self.memory_label.configure(text_color="#28A745")
        # disk
        if disk > 50:
            if disk > 90:
                self.disk_label.configure(text_color="#DC3545")
            else:
                self.disk_label.configure(text_color="#E7A911")
        else:
            self.disk_label.configure(text_color="#28A745")

        # calling itself after every 2 seconds
        self.after(2000, self.update_metrics)

    # Close Window
    def on_close(self):
        self.destroy()

    # Toggle Between Themes
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        if current_mode == "Dark":
            new_mode = "Light"
            self.close_btn.configure(fg_color="#DC3545")
            self.toggle_btn.configure(text=" Night ", fg_color="#3a90c9", hover_color="#3a90c9")
            self.toggle_btn.place(relx=0.84, rely=0)
        else:
            new_mode = "Dark"
            self.close_btn.configure(fg_color="transparent")
            self.toggle_btn.configure(text=" Day ", fg_color="transparent", hover_color="#E7A911")
            self.toggle_btn.place(relx=0.87, rely=0)

        # set new theme
        ctk.set_appearance_mode(new_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
