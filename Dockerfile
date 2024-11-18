# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install system dependencies and necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    ffmpeg \
    gcc \
    python3-pip \
    python3-dev \
    aria2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Set environment variables (Docker will use the .env file, so no need to set them here)
# Docker will pick them up when starting the app

# Expose the port the app will run on (if needed for your app)
EXPOSE 8000

# Run the application (ensure this is the correct entry point)
CMD ["python3", "bot.py"]
