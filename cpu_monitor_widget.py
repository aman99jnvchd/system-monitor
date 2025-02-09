import psutil
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.geometry("350x250+10+10")

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
        self.toggle_btn.place(relx=0.89, rely=0)

        # Header
        self.header = ctk.CTkLabel(
            self,
            text="System Usage",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.header.pack(side="top", padx=20, pady=(35, 15))

        # Create Metrics
        self.cpu_label = self.create_metric("CPU")
        self.memory_label = self.create_metric("Memory")
        self.disk_label = self.create_metric("Disk")
        self.network_label = self.create_metric("Network")

        # Store previous network data
        self.prev_bytes_sent, self.prev_bytes_recv = self.get_network_data()

        # Update Metrics
        self.update_metrics()
    
    def start_move(self, event):
        """ Track initial position when dragging starts """
        self._offset_x = event.x
        self._offset_y = event.y

    def on_move(self, event):
        """This method is called when the user moves the mouse while holding down the left button."""
        delta_x = event.x - self._offset_x
        delta_y = event.y - self._offset_y
        # Move the window by the distance the mouse has moved
        new_x = self.winfo_x() + delta_x
        new_y = self.winfo_y() + delta_y
        self.geometry(f"+{new_x}+{new_y}")

    def create_metric(self, name):
        """ Create a labeled metric display """
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=5, padx=30, fill="x")
        # Label
        label = ctk.CTkLabel(
            frame,
            text=name,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(side="left")
        # Value
        value = ctk.CTkLabel(
            frame,
            text="0%",
            text_color="#28A745",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        value.pack(side="right")
        return value

    def get_network_data(self):
        """ Get current network I/O data """
        net_io = psutil.net_io_counters()
        return net_io.bytes_sent, net_io.bytes_recv

    def update_metrics(self):
        """ Update system metrics and network speed """
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # updating usage
        self.cpu_label.configure(text=f"{cpu}%")
        self.memory_label.configure(text=f"{memory}%")
        self.disk_label.configure(text=f"{disk}%")

        # change color after certain threshold - CPU
        self.set_label_color(self.cpu_label, cpu)
        self.set_label_color(self.memory_label, memory)
        self.set_label_color(self.disk_label, disk)

        # Calculate Network Speed
        new_bytes_sent, new_bytes_recv = self.get_network_data()
        upload_speed = (new_bytes_sent - self.prev_bytes_sent) / 1024 / 2  # KB/s
        download_speed = (new_bytes_recv - self.prev_bytes_recv) / 1024 / 2 # KB/s

        # Store current values for next calculation
        self.prev_bytes_sent, self.prev_bytes_recv = new_bytes_sent, new_bytes_recv
        # Update Network Label
        self.network_label.configure(text=f"↑ {upload_speed:.1f} KB/s ↓ {download_speed:.1f} KB/s")

        # calling itself after every 2 seconds
        self.after(2000, self.update_metrics)

    def set_label_color(self, label, usage):
        """ Change label color based on usage percentage """
        if usage > 50:
            if usage > 90:
                label.configure(text_color="#DC3545")  # Red
            else:
                label.configure(text_color="#E7A911")  # Yellow
        else:
            label.configure(text_color="#28A745")  # Green

    def on_close(self):
        """ Close the application """
        self.destroy()

    def toggle_theme(self):
        """ Toggle between Dark and Light themes """
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"

        if current_mode == "Dark":
            new_mode = "Light"
            self.close_btn.configure(fg_color="#DC3545")
            self.toggle_btn.configure(text=" Night ", fg_color="#3a90c9", hover_color="#3a90c9")
            self.toggle_btn.place(relx=0.862, rely=0)
        else:
            new_mode = "Dark"
            self.close_btn.configure(fg_color="transparent")
            self.toggle_btn.configure(text=" Day ", fg_color="transparent", hover_color="#E7A911")
            self.toggle_btn.place(relx=0.89, rely=0)

        # set new theme
        ctk.set_appearance_mode(new_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
