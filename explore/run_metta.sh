#!/bin/bash
# Convenient script to run Metta with different configurations
# Usage: ./run_metta.sh [train|eval|play] [experiment_name] [hardware]

set -e

# Default values
MODE="play"
EXPERIMENT="my_experiment"
HARDWARE="poplinux"  # Setting PopOS Linux as default hardware
WANDB_MODE="off"     # Default to off for non-team members

# Process arguments
if [ $# -ge 1 ]; then
  MODE=$1
fi

if [ $# -ge 2 ]; then
  EXPERIMENT=$2
fi

if [ $# -ge 3 ]; then
  HARDWARE=$3
fi

# Create hardware config if it doesn't exist
if [ ! -d "../configs/hardware" ]; then
  mkdir -p "../configs/hardware"
fi

if [ ! -f "../configs/hardware/poplinux.yaml" ]; then
  cat > "../configs/hardware/poplinux.yaml" << EOF
# PopOS Linux hardware configuration
_target_: null

# CPU settings
cpu:
  cores: "all"  # Use all available CPU cores

# GPU settings - modify based on your actual hardware
gpu:
  use: true
  device: 0     # First GPU device

# Memory settings
memory:
  fraction: 0.8  # Use 80% of available memory

# Display settings
display:
  width: 1280
  height: 720
EOF
fi

# Activate conda environment if exists
if command -v conda &> /dev/null && conda info --envs | grep -q "\bmetta\b"; then
  echo "Activating conda environment: metta"
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate metta
fi

# Print what we're doing
echo "Running Metta in $MODE mode"
echo "Experiment: $EXPERIMENT"
echo "Hardware: $HARDWARE"
echo "Working directory: $(pwd)"

# Move to the repository root to run the command
cd "$(dirname "$0")/.."

# Run the appropriate command
case $MODE in
  train)
    python3 -m tools.train run=$EXPERIMENT +hardware=$HARDWARE wandb=$WANDB_MODE
    ;;
  eval)
    python3 -m tools.eval run=$EXPERIMENT +hardware=$HARDWARE wandb=$WANDB_MODE
    ;;
  play)
    python3 -m tools.play run=$EXPERIMENT +hardware=$HARDWARE wandb=$WANDB_MODE
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Available modes: train, eval, play"
    exit 1
    ;;
esac 