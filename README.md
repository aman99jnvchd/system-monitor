# System Usage Monitor

A simple system usage monitor built using [psutil](https://pypi.org/project/psutil/) and [customtkinter](https://github.com/TomSchimansky/CustomTkinter). This application displays real-time usage statistics for CPU, memory, disk, and network speed in a sleek, customizable window with support for light/dark themes.

> **Note:** When running the application inside a Docker container, extra steps are required to enable GUI (X11) support.

## Features

- **Real-time system stats:** Displays up-to-date CPU, memory, disk usage, and network speed.
- **Customizable UI:** Easily toggle between light and dark themes.
- **Draggable Window:** Move the window anywhere with a simple mouse drag.
- **Live Updates:** The UI refreshes every 2 seconds to display real-time stats.

## Installation (Local)

To run this application locally, install the dependencies:

```bash
pip install psutil customtkinter
```

### Tkinter Dependency
Ensure your Python installation includes Tkinter. On some Linux distributions, you may need to install it manually:

```bash
sudo apt-get install python3-tk
```

## Running with Docker

### Prerequisites
- **Docker Desktop for Windows** (or your preferred platform).
- **An X Server on Windows:**  
  Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (or another X server) and launch it with the following settings:
  - **Multiple Windows**
  - **Start no client**
  - **Disable access control**
- **Windows Firewall:** Allow inbound and outbound TCP connections on port **6000**.

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

Ensure VcXsrv is running on your Windows host, then execute:

```bash
docker run -it --rm system-monitor
```

This Dockerfile is pre-configured with all necessary GUI libraries, and the `DISPLAY` variable is set to `host.docker.internal:0.0`, allowing the application to open on your Windows desktop via VcXsrv.

### Troubleshooting GUI Issues

- **DISPLAY Variable:**

  - If you see errors like `TclError: no display name and no $DISPLAY environment variable`, verify the `DISPLAY` variable inside the container:
    ```bash
    echo $DISPLAY
    ```
  - Alternatively, explicitly pass your Windows host’s IP address. If your Windows host IP is `192.168.1.100`, run:
    ```bash
    docker run -it --rm -e DISPLAY=192.168.1.100:0.0 system-monitor
    ```

- **Firewall Settings:**

  - Ensure that Windows Firewall allows connections on TCP port 6000.

- **Testing X11:**

  - To check if the X server is accepting connections, try launching a GUI app inside the container (e.g., `xclock`):
    ```bash
    docker run -it --rm system-monitor xclock
    ```
  - If `xclock` appears on your Windows desktop, X11 forwarding is working correctly.

## License

This project is open-source and available under the MIT License.
