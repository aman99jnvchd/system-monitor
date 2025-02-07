# System Usage Monitor

A simple system usage monitor built using [psutil](https://pypi.org/project/psutil/) and [customtkinter](https://github.com/TomSchimansky/CustomTkinter). This application displays real-time usage statistics for CPU, memory, and disk usage in a sleek, customizable window with support for light/dark themes.

> **Note:** When running the application inside a Docker container, extra steps are required to enable GUI (X11) support.

## Features

- **Real-time system stats:** Displays up-to-date CPU, memory, and disk usage.
- **Customizable UI:** Easily toggle between light and dark themes.
- **Draggable Window:** The window can be moved around with a simple mouse drag.
- **Responsive Design:** The UI updates every 2 seconds with live system stats.

## Installation (Local)

To run this application locally (outside of Docker), run:

```bash
pip install psutil customtkinter
```

### Tkinter Dependency
Make sure your Python installation includes Tkinter. On some Linux distributions, you might need to install an additional package:

```bash
sudo apt-get install python3-tk
```

## Running with Docker

### Prerequisites
- **Docker Desktop for Windows** (or your platform of choice).
- **An X Server on Windows:**  
  Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (or an equivalent X server) and launch it with the following settings:
  - **Multiple Windows**
  - **Start no client**
  - **Disable access control**
- **Windows Firewall:** Ensure that inbound and outbound TCP connections on port **6000** are allowed.

### Dockerfile

Create a file named `Dockerfile` with the following content:

```dockerfile
# Use a Python base image
FROM python:3.9-slim

# Install system dependencies for Tkinter and X11 applications
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    x11-utils

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir psutil customtkinter

# Set the DISPLAY environment variable for X11 forwarding
ENV DISPLAY=host.docker.internal:0.0

# Run the application
CMD ["python3", "cpu_monitor_widget.py"]
```

### Building the Docker Image

Run the following command in your terminal:

```bash
docker build -t system-monitor .
```

### Running the Docker Container

Make sure VcXsrv is running on your Windows host, then run:

```bash
docker run -it --rm system-monitor
```

This command will launch the application inside the container and forward the GUI output to your X server on Windows.

## License

This project is open-source and available under the MIT License.
