This is our home base for exploring multi-agent systems.

# Setting Up Metta on PopOS Linux

## Prerequisites
- Git
- Python 3.11.7
- Conda (or venv)

## Installation Steps

1. Clone the repository if you haven't already:
```bash
git clone https://github.com/Metta-AI/metta.git
cd metta
```

2. Create and activate a Conda environment:
```bash
conda create -n metta python=3.11.7
conda activate metta
```

3. Run the setup script:
```bash
./devops/setup_build.sh
```

4. Run the PopOS-specific setup script (if using PopOS):
```bash
chmod +x ./explore/pop_os_setup.sh
./explore/pop_os_setup.sh
```

## Multi-Agent Experiments

We've created utilities specifically for multi-agent experiments in the `explore/multiagent_utils.py` script.

### Creating a Multi-Agent Experiment

```bash
python explore/multiagent_utils.py create experiment_name --agents 3 --types navigator manipulator observer --env gridworld
```

### Running a Multi-Agent Experiment

```bash
python explore/multiagent_utils.py run experiment_name --mode play --hardware poplinux
```

## Running Metta

You can use our simplified run script:
```bash
chmod +x ./explore/run_metta.sh
./explore/run_metta.sh [train|eval|play] [experiment_name] [hardware]
```

Example:
```bash
./explore/run_metta.sh play my_experiment poplinux
```

### Manual Commands

#### Training a Model
```bash
python -m tools.train run=my_experiment +hardware=poplinux
```

#### Running Evaluation
```bash
python -m tools.eval run=my_experiment +hardware=poplinux
```

#### Playing the Interactive Simulation
```bash
python -m tools.play run=my_experiment +hardware=poplinux
```

Note: Add `wandb=off` parameter if you're not a member of `metta-research` on wandb, or add your own wandb config in `configs/wandb`.

## Evaluating Models

To run post-training evaluation and compare different policies:

```bash
# Add policy to existing navigation evals database
python3 -m tools.eval eval=navigation run=RUN_NAME eval.policy_uri=POLICY_URI +eval_db_uri=wandb://artifacts/navigation_db

# View results in heatmap along with other policies
python3 -m tools.analyze run=analyze +eval_db_uri=wandb://artifacts/navigation_db analyzer.policy_uri=POLICY_URI
```

## Troubleshooting

If you encounter any issues with the setup, check the following:
- Make sure all dependencies are installed
- Verify that Python 3.11.7 is being used
- Run the PopOS-specific setup script to install required system packages
- Check that your hardware configuration is properly set up in `configs/hardware/poplinux.yaml`

## PopOS-Specific Notes

The `pop_os_setup.sh` script handles installation of:
- Required system libraries including ffmpeg, graphics libraries, and build tools
- CUDA toolkit if an NVIDIA GPU is detected
- Additional Python packages like pyglet and pyopengl
- Symbolic links for Python 3.11 if needed