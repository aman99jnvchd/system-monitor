# Use Python base image
FROM python:3.9-slim

# Install required system libraries
RUN apt-get update && apt-get install -y python3-tk

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir psutil customtkinter

# Run the app
CMD ["python3", "cpu_monitor_widget.py"]
