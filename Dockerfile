# Use Python base image
FROM python:3.9-slim
# FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install psutil customtkinter

# Run the app
CMD ["python3", "cpu_monitor_widget.py"]