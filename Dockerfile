# Use Python base image
FROM python:3.9-slim

# Install Tkinter and X11 utilities (for GUI apps)
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    x11-utils

# Set working directory
WORKDIR /app

# Copy your application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir psutil customtkinter

# Set the DISPLAY environment variable so GUI apps know where to render
ENV DISPLAY=host.docker.internal:0.0

# Run your application
CMD ["python3", "cpu_monitor_widget.py"]
