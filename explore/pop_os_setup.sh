#!/bin/bash
# PopOS-specific setup script for Metta
# Run this after the main setup_build.sh script

set -e

echo "Installing PopOS-specific dependencies for Metta..."

# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  cmake \
  ffmpeg \
  libavcodec-dev \
  libavformat-dev \
  libavutil-dev \
  libswscale-dev \
  libjpeg-dev \
  libpng-dev \
  libopenexr-dev \
  libglfw3-dev \
  libglew-dev \
  pkg-config \
  python3.11-dev \
  python3.11-venv

# If running with NVIDIA GPU, install CUDA dependencies
if lspci | grep -q NVIDIA; then
  echo "NVIDIA GPU detected. Installing CUDA dependencies..."
  sudo apt-get install -y nvidia-cuda-toolkit
fi

echo "Installing Python dependencies specific to PopOS..."
pip install pyglet==2.0.10 pyopengl

echo "Creating symbolic links for Python 3.11 if needed..."
if [ ! -f /usr/bin/python3.11 ]; then
  echo "Creating symlink for Python 3.11..."
  sudo ln -s $(which python3.11) /usr/bin/python3.11
fi

echo "PopOS-specific setup complete!"
echo "You can now proceed with running Metta" 