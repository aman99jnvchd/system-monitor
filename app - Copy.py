# pyinstaller --onefile --noconsole cpu_monitor_widget.py
import tkinter as tk
import psutil
import pystray
from PIL import Image, ImageDraw
from ttkthemes import ThemedStyle

class ModernWidget:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.98)  # Transparency
        self.root.attributes("-topmost", True)
        self.root.geometry("220x150+50+50")
       
        # Custom Style Configuration (CSS-like)
        self.style = ThemedStyle(root)
        self.set_theme("dark")  # Default theme
       
        # Widget Frame with rounded corners (simulated)
        self.canvas = tk.Canvas(root, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_rounded_rectangle(0, 0, 220, 150, radius=30, fill=self.bg_color)
       
        # Header
        self.header = tk.Label(
            self.canvas,
            text="System Usage",
            bg=self.bg_color,
            fg=self.accent_color,
            font=("Segoe UI", 12, "bold")
        )
        self.header.place(x=20, y=10)
       
        # Close Button
        self.close_btn = tk.Label(
            self.canvas,
            text="×",
            font=("Segoe UI", 16),
            fg=self.text_color,
            bg=self.bg_color,
            cursor="hand2"
        )
        self.close_btn.place(x=190, y=5)
        self.close_btn.bind("<Button-1>", lambda e: self.on_close())
       
        # Metrics
        self.create_metric("CPU", 20, 50)
        self.create_metric("Memory", 20, 85)
        self.create_metric("Disk", 20, 120)
       
        # Draggable functionality
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)
       
        # System tray
        self.setup_tray()
        self.update_metrics()

    # ----------------------
    # Style Management
    # ----------------------
    def set_theme(self, theme_name):
        self.style.set_theme("equilux" if theme_name == "dark" else "arc")
        self.bg_color = "#2d2d2d" if theme_name == "dark" else "#f5f6f7"
        self.text_color = "#ffffff" if theme_name == "dark" else "#333333"
        self.accent_color = "#4CAF50"  # Green accent color

    def draw_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    # ----------------------
    # Widget Components
    # ----------------------
    def create_metric(self, name, x, y):
        frame = tk.Frame(self.canvas, bg=self.bg_color)
        frame.place(x=x, y=y)
       
        # Label
        tk.Label(
            frame,text=f"{name}:", anchor="w",
            bg=self.bg_color, fg=self.text_color,
            font=("Segoe UI", 9)
        ).pack(side="left")
       
        # Value
        value_label = tk.Label(
            frame, text="0%",
            bg=self.bg_color, fg=self.accent_color,
            font=("Segoe UI", 9, "bold")
        )
        value_label.pack(side="left", padx=5)
       
        setattr(self, f"{name.lower()}_label", value_label)

    # ----------------------
    # Core Functionality
    # ----------------------
    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        x = self.root.winfo_x() - self.start_x + event.x
        y = self.root.winfo_y() - self.start_y + event.y
        self.root.geometry(f"+{x}+{y}")

    def update_metrics(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        self.cpu_label.config(text=f"{cpu}%")
        self.memory_label.config(text=f"{memory}%")
        self.disk_label.config(text=f"{disk}%")
       
        # Color warning for high usage
        for metric, value in [("cpu", cpu), ("memory", memory), ("disk", disk)]:
            label = getattr(self, f"{metric}_label")
            label.config(fg="#ff4444" if value > 80 else self.accent_color)

        self.root.after(2000, self.update_metrics)

    # ----------------------
    # System Tray
    # ----------------------
    def setup_tray(self):
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill="#4CAF50")
       
        menu = (
            pystray.MenuItem("Toggle Theme", self.toggle_theme),
            pystray.MenuItem("Exit", self.on_close)
        )
       
        self.tray_icon = pystray.Icon("monitor_icon", image, "System Usage", menu)
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def toggle_theme(self):
        current_theme = "dark" if self.bg_color == "#2d2d2d" else "light"
        self.set_theme("light" if current_theme == "dark" else "dark")
        self.canvas.config(bg=self.bg_color)
        self.redraw_ui()

    def redraw_ui(self):
        # Update all colors
        self.canvas.itemconfig("all", fill=self.bg_color)
        self.header.config(bg=self.bg_color, fg=self.accent_color)
        self.close_btn.config(bg=self.bg_color, fg=self.text_color)
       
        # Update metric labels
        for widget in [self.cpu_label, self.memory_label, self.disk_label]:
            widget.config(bg=self.bg_color)

    def minimize_to_tray(self):
        self.root.withdraw()
        self.tray_icon.run()

    def on_close(self):
        self.tray_icon.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    widget = ModernWidget(root)
    root.mainloop()