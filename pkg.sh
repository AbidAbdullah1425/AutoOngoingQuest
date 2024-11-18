#!/bin/bash

# Update package lists
echo "Updating package lists..."
apt-get update -y

# Install only necessary system dependencies for the bot's functionality
echo "Installing required system dependencies..."
apt-get install -y python3 python3-pip python3-dev libffi-dev libssl-dev build-essential curl ffmpeg

# Install the required Python dependencies from the requirements.txt
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Clean up to reduce image size
echo "Cleaning up..."
apt-get clean

echo "Setup complete!"
