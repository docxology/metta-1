#!/bin/bash
# Script to install dependencies for Metta

set -e

echo "Installing Metta dependencies..."
cd "$(dirname "$0")/.."

# Install Python requirements
pip3 install -r requirements.txt

# Create deps directory
mkdir -p deps
cd deps

# Fast GAE
if [ ! -d "fast_gae" ]; then
  echo "Cloning fast_gae"
  git clone https://github.com/Metta-AI/fast_gae.git
fi
cd fast_gae
git pull
echo "Building fast_gae"
python3 setup.py build_ext --inplace
echo "Installing fast_gae"
pip3 install -e .
cd ..

# Pufferlib
if [ ! -d "pufferlib" ]; then
  echo "Cloning pufferlib"
  git clone https://github.com/Metta-AI/pufferlib.git
fi
cd pufferlib
echo "Fetching pufferlib"
git fetch
echo "Checking out metta branch"
git checkout metta
git pull
echo "Installing pufferlib"
pip3 install -e .
cd ..

# Mettagrid
if [ ! -d "mettagrid" ]; then
  echo "Cloning mettagrid"
  git clone https://github.com/Metta-AI/mettagrid.git
fi
cd mettagrid
echo "Fetching mettagrid"
git fetch
echo "Installing mettagrid"
pip3 install -r requirements.txt
echo "Building mettagrid"
python3 setup.py build_ext --inplace
echo "Installing mettagrid"
pip3 install -e .
cd ..

# Carbs
if [ ! -d "carbs" ]; then
  echo "Cloning carbs"
  git clone https://github.com/kywch/carbs.git
fi
cd carbs
echo "Fetching carbs"
git pull
echo "Installing carbs"
pip3 install -e .
cd ..

# Wandb Carbs
if [ ! -d "wandb_carbs" ]; then
  echo "Cloning wandb_carbs"
  git clone https://github.com/Metta-AI/wandb_carbs.git
fi
cd wandb_carbs
echo "Fetching wandb_carbs"
git pull
echo "Installing wandb_carbs"
pip3 install -e .
cd ..

echo "All dependencies installed successfully!" 