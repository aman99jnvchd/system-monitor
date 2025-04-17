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
RUN pip install -r requirements.txt

# Set the DISPLAY environment variable so GUI apps know where to render
ENV DISPLAY=host.docker.internal:0.0

# Expose port (default FastAPI port -> 8000)
EXPOSE 8800

# Run the FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8800"]
