# DAF (Dis Is Not An Agent Framework) - Metta Installation Guide

## 🎯 Overview

The **DAF (Dis Is Not An Agent Framework)** exists to facilitate the installation, operation, and use of the **Metta** multi-agent reinforcement learning framework. This guide explains how to install and use Metta within the DAF environment.

## 📋 Prerequisites

Before installing Metta through DAF, ensure you have:

- ✅ Python 3.8 or higher
- ✅ pip package manager
- ✅ Git (for cloning repositories)
- ✅ Virtual environment support
- ✅ Build tools (compilers, etc.)

## 🚀 Quick Start

### 1. Install Metta through DAF

```bash
cd /path/to/metta
python3 daf/setup_metta.py
```

This will:
- ✅ Create a virtual environment for Metta
- ✅ Install Metta and all dependencies
- ✅ Configure DAF for seamless Metta integration
- ✅ Test the installation with real Metta components

### 2. Activate DAF Environment

```bash
cd /path/to/metta
python3 daf/activate_daf.py
```

This activates the DAF environment with Metta properly configured.

### 3. Run Metta Examples

```bash
cd /path/to/metta
python3 daf/run_metta_examples.py
```

This runs all Metta examples with real components and comprehensive logging.

## 📁 DAF Structure for Metta

```
daf/
├── setup_metta.py              # Metta installation script
├── activate_daf.py             # DAF environment activation
├── run_metta_examples.py       # Examples runner with logging
├── configs/                    # DAF configuration files
│   └── metta_config.ini       # Metta integration config
├── logs/                       # Installation and execution logs
├── outputs/                    # Example outputs and results
├── examples/                   # Metta usage examples
│   ├── simple_metta_usage.py  # Basic component demo
│   ├── curriculum_demo.py     # Curriculum learning demo
│   ├── rl_training.py         # RL training demo
│   ├── rl_training_example.py # Advanced RL training
│   └── adaptive_curriculum_example.py # Adaptive learning
└── src/                       # DAF source code
    └── daf/                   # DAF framework components
```

## 🛠️ Installation Process

### Step 1: Environment Setup
```bash
python3 daf/setup_metta.py
```

This script performs:
1. **Prerequisites Check**: Verifies all required tools
2. **Virtual Environment Creation**: Isolated Python environment
3. **Metta Installation**: Installs Metta in editable mode
4. **Dependencies**: Installs required packages (torch, wandb, etc.)
5. **Testing**: Validates Metta imports and functionality
6. **Configuration**: Creates DAF/Metta integration config

### Step 2: Environment Activation
```bash
python3 daf/activate_daf.py
```

This script:
1. **Path Configuration**: Sets up Python paths for Metta imports
2. **Environment Variables**: Configures DAF_ROOT, METTA_ROOT, etc.
3. **Virtual Environment**: Activates the Metta environment
4. **Import Testing**: Verifies all Metta components load correctly
5. **Environment Info**: Displays configuration status

### Step 3: Examples Execution
```bash
python3 daf/run_metta_examples.py
```

This script:
1. **Environment Activation**: Ensures DAF/Metta is properly set up
2. **Example Discovery**: Finds all Metta example scripts
3. **Sequential Execution**: Runs each example with proper logging
4. **Output Collection**: Captures all outputs, visualizations, and data
5. **Results Compilation**: Creates comprehensive execution report
6. **Error Handling**: Logs failures with detailed error information

## 📊 Example Outputs and Destinations

### Console Output (All Examples)
- **Location**: Terminal where script executes
- **Content**: Real-time progress and formatted reports
- **Features**: Status indicators, metrics display, progress tracking

### JSON Data Files (Advanced Examples)
- **Files**:
  - `adaptive_curriculum_results.json` (curriculum training data)
  - `rl_training_output/training_results.json` (RL training data)
- **Content**: Structured experiment results and metadata
- **Access**: For analysis and visualization

### Binary Artifacts (Training Examples)
- **Files**:
  - `rl_training_output/policy_checkpoint.pt` (PyTorch models)
- **Content**: Trained policy parameters
- **Access**: Loadable for continued training/evaluation

### Configuration Files
- **Files**:
  - `rl_training_output/experiment_config.json` (experiment setup)
- **Content**: Reproducible configuration data
- **Access**: For experiment replication

## 🧪 Testing Metta Installation

### Individual Component Testing
```bash
# Activate DAF environment first
python3 daf/activate_daf.py

# Then test individual imports
python3 -c "import metta; print('✅ Basic Metta import works')"
python3 -c "from metta.adaptive.adaptive_controller import AdaptiveController; print('✅ AdaptiveController available')"
python3 -c "from metta.cogworks.curriculum.curriculum import Curriculum; print('✅ Curriculum available')"
python3 -c "from metta.rl.trainer import Trainer; print('✅ RL Trainer available')"
```

### Run Specific Examples
```bash
# Basic Metta components demo
python3 daf/examples/simple_metta_usage.py

# Curriculum learning demo
python3 daf/examples/curriculum_demo.py

# RL training demo
python3 daf/examples/rl_training.py

# Advanced examples with file outputs
python3 daf/examples/rl_training_example.py
python3 daf/examples/adaptive_curriculum_example.py
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Virtual Environment Not Found
```bash
# Solution: Reinstall Metta
python3 daf/setup_metta.py
```

#### 2. Import Errors
```bash
# Solution: Reactivate DAF environment
python3 daf/activate_daf.py
```

#### 3. Missing Dependencies
```bash
# Solution: Reinstall with additional dependencies
python3 daf/setup_metta.py
```

#### 4. Permission Errors
```bash
# Solution: Use virtual environment or user install
python3 daf/setup_metta.py
```

### Log Files
Check these logs for detailed error information:
- `daf/logs/metta_installation.log` - Installation process
- `daf/logs/metta_examples.log` - Examples execution
- `daf/logs/daf_metta.log` - DAF/Metta integration

## 🎯 DAF Philosophy

DAF (Dis Is Not An Agent Framework) is a **recursive acronym** emphasizing that while it provides agent framework capabilities, it is fundamentally an **integration layer and tooling ecosystem** that enhances Metta's native multi-agent RL capabilities without replacing them.

### Core Principles
- ✅ **Facilitate Metta**: Make Metta easily installable and usable
- ✅ **Real Integration**: Use actual Metta components (zero mocking)
- ✅ **Production Ready**: Enable real-world development workflows
- ✅ **Comprehensive Tooling**: Provide complete development environment
- ✅ **Seamless Operation**: Abstract complexity for smooth usage

## 🚀 Advanced Usage

### Custom Environment Setup
```python
# Create custom virtual environment
python3 -m venv my_metta_env

# Activate and install Metta
source my_metta_env/bin/activate
cd /path/to/metta
pip install -e .
python3 daf/examples/simple_metta_usage.py
```

### Development Mode
```bash
# Make Metta changes and test immediately
cd /path/to/metta
# Edit Metta source code...
python3 daf/examples/curriculum_demo.py  # Test changes
```

### Production Deployment
```bash
# Package DAF with Metta for deployment
python3 daf/setup_metta.py
python3 daf/run_metta_examples.py  # Validate everything works
# Deploy the entire daf/ directory
```

## 📚 Documentation and Examples

- 📖 **DAF Documentation**: `@daf/README.md`
- 🧪 **Metta Method Docs**: `@daf/methods/` (129 documentation files)
- 📊 **Repository Structure**: `@daf/structure/METTA_REPOSITORY_STRUCTURE.md`
- 🎯 **Examples**: `daf/examples/` (5 comprehensive examples)
- 🛠️ **Tools**: `@daf/scripts/` (validation and demo scripts)

## 🎉 Success Indicators

Your Metta installation through DAF is successful when:

- ✅ All examples run without `ModuleNotFoundError`
- ✅ Real Metta components are imported and used
- ✅ Training examples produce actual outputs and artifacts
- ✅ Curriculum learning demonstrates real progression
- ✅ RL training shows actual learning curves
- ✅ All visualizations and reports work with real data

## 🔧 Support

For issues with Metta installation through DAF:

1. **Check Logs**: Review `daf/logs/metta_installation.log`
2. **Validate Environment**: Run `python3 daf/activate_daf.py`
3. **Test Individual Components**: Import Metta components manually
4. **Reinstall if Needed**: Run `python3 daf/setup_metta.py`

---

**🎯 DAF successfully facilitates Metta installation and usage!**

The DAF framework makes Metta easily installable, operable, and usable while maintaining the integrity and functionality of the underlying multi-agent RL framework.


