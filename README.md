# System Usage Monitor

A comprehensive system usage monitor built using [psutil](https://pypi.org/project/psutil/) and [customtkinter](https://github.com/TomSchimansky/CustomTkinter). This application displays real-time usage statistics for CPU, memory, disk, and network speed in a sleek, customizable window with support for light/dark themes. It also includes a FastAPI backend for API access and a CLI fallback mode.

> **Note:** When running the application inside a Docker container, extra steps are required to enable GUI (X11) support.

## 🚀 Features

- **Real-time system stats:** Displays up-to-date CPU, memory, disk usage, and network speed
- **Dual Interface Modes:**
  - **GUI Mode:** Modern, draggable window with CustomTkinter
  - **CLI Mode:** Command-line interface as fallback when GUI is unavailable
- **API Access:** RESTful API endpoints for system metrics via FastAPI
- **Customizable UI:** Easily toggle between light and dark themes
- **Draggable Window:** Move the window anywhere with a simple mouse drag
- **Live Updates:** The UI refreshes every second to display real-time stats
- **Smart Color Coding:** Metrics change color based on usage thresholds (Green < 50%, Yellow 50-90%, Red > 90%)
- **Always on Top:** Window stays visible above other applications
- **CI/CD Ready:** Jenkins pipeline for automated building and deployment

## 📁 Project Structure

```
System Monitor/
├── main.py              # Main entry point with GUI/CLI fallback
├── api.py               # FastAPI application for REST API
├── modules/
│   ├── metrics.py       # Core system metrics collection
│   ├── gui.py          # CustomTkinter GUI implementation
│   └── cli.py          # Command-line interface
├── Dockerfile           # Docker configuration for containerization
├── docker-compose.yml   # Docker Compose configuration
├── Jenkinsfile          # CI/CD pipeline configuration
├── requirements.txt     # Python dependencies
└── .dockerignore        # Docker build exclusions
```

## 🛠️ Installation (Local)

To run this application locally, install the dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install fastapi uvicorn psutil customtkinter
```

### Tkinter Dependency
Ensure your Python installation includes Tkinter. On some Linux distributions, you may need to install it manually:

```bash
sudo apt-get install python3-tk
```

## 🚀 Running the Application

### GUI Mode (Default)
```bash
python main.py
```

### CLI Mode (Fallback)
The application automatically falls back to CLI mode if GUI is unavailable:
```bash
python main.py
# If Tkinter fails, CLI mode starts automatically
```

### API Mode
```bash
python api.py
# Or use uvicorn directly:
uvicorn api:app --host 0.0.0.0 --port 8800
```

## 🌐 API Endpoints

The FastAPI backend provides the following endpoints:

- **GET /metrics** - Returns all system metrics in JSON format:
  ```json
  {
    "cpu": 25.5,
    "memory": 67.2,
    "disk": 45.8,
    "network": {
      "upload_kbps": 12.3,
      "download_kbps": 45.7
    }
  }
  ```

## 🐳 Running with Docker

### Prerequisites
- **Docker Desktop for Windows** (or your preferred platform)
- **An X Server on Windows:**  
  Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (or another X server) and launch it with the following settings:
  - **Multiple Windows**
  - **Start no client**
  - **Disable access control**
- **Windows Firewall:** Allow inbound and outbound TCP connections on port **6000**

### Building the Docker Image

Run the following command in your terminal:

```bash
docker build -t system-monitor .
```

### Running the Docker Container

#### GUI Mode
Ensure VcXsrv is running on your Windows host, then execute:

```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0.0 system-monitor python main.py
```

#### API Mode
```bash
docker run -d --name system-monitor -p 8800:8800 system-monitor
```

The container exposes port 8800 for the FastAPI application.

### Docker Compose
```bash
docker-compose up -d
```

## 🔄 CI/CD Pipeline

This project includes a Jenkins pipeline (`Jenkinsfile`) that automates:

1. **Clean Workspace** - Removes previous build artifacts
2. **Clone Repository** - Fetches latest code from Git
3. **Build Docker Image** - Creates the system-monitor Docker image
4. **Run Container** - Deploys the application
5. **Push to Docker Hub** - Publishes the image to Docker Hub

## 🔧 Troubleshooting

### GUI Issues

- **DISPLAY Variable:**
  - If you see errors like `TclError: no display name and no $DISPLAY environment variable`, verify the `DISPLAY` variable inside the container:
    ```bash
    echo $DISPLAY
    ```
  - Alternatively, explicitly pass your Windows host's IP address. If your Windows host IP is `192.168.1.100`, run:
    ```bash
    docker run -it --rm -e DISPLAY=192.168.1.100:0.0 system-monitor python main.py
    ```

- **Firewall Settings:**
  - Ensure that Windows Firewall allows connections on TCP port 6000

- **Testing X11:**
  - To check if the X server is accepting connections, try launching a GUI app inside the container (e.g., `xclock`):
    ```bash
    docker run -it --rm system-monitor xclock
    ```
  - If `xclock` appears on your Windows desktop, X11 forwarding is working correctly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open-source and available under the MIT License.
