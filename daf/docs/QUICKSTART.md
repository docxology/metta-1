# DAF Quick Start Guide

This guide will help you get up and running with DAF (Distributed Agent Framework) in minutes.

## 🚀 One-Line Setup

```bash
# Clone and setup DAF (if not already done)
git clone <daf-repository>
cd daf

# Run complete setup
python setup.py --profile research --non-interactive
```

That's it! DAF is now installed and ready to use.

## 🎯 Quick Test

Run your first experiment:

```bash
# Quick test simulation
daf run experiment configs/experiments/quick_test.yaml

# View available configurations
daf run list

# Check system status
daf validate system
```

## 📋 What Just Happened?

The setup script performed:

1. ✅ **System Validation** - Checked Python version, memory, and dependencies
2. ✅ **DAF Installation** - Installed core framework components
3. ✅ **Metta AI Setup** - Configured Metta AI framework integration
4. ✅ **Configuration** - Set up profile-based configurations
5. ✅ **Validation** - Verified everything works together

## 🎮 Running Experiments

### Basic Experiment

```bash
# Run a basic arena experiment
daf run experiment configs/experiments/arena_basic.yaml
```

### Advanced Experiment

```bash
# Run with custom parameters
daf run experiment configs/experiments/arena_advanced.yaml \
  --timesteps 1000000 --agents 48
```

### Batch Experiments

```bash
# Run multiple experiments
daf run batch \
  configs/experiments/quick_test.yaml \
  configs/experiments/arena_basic.yaml \
  configs/experiments/arena_advanced.yaml
```

## ⚙️ Configuration

DAF uses hierarchical configuration files. Key files:

- `configs/base/global.yaml` - System-wide settings
- `configs/profiles/research.yaml` - Research profile settings
- `configs/experiments/*.yaml` - Experiment configurations

### Creating Custom Configurations

```bash
# Copy an existing config
cp configs/experiments/arena_basic.yaml configs/experiments/my_experiment.yaml

# Edit the configuration
# Modify parameters like num_agents, timesteps, etc.

# Run your custom experiment
daf run experiment configs/experiments/my_experiment.yaml
```

## 🔍 Monitoring and Analysis

### System Status

```bash
# Check overall system status
daf status

# Detailed system information
daf info

# Validate installation
daf validate installation
```

### Experiment Monitoring

Results are automatically saved to the `outputs/` directory:

```
outputs/
├── my_experiment/
│   ├── checkpoints/     # Model checkpoints
│   ├── logs/           # Execution logs
│   ├── metrics/        # Performance metrics
│   └── artifacts/      # Additional artifacts
```

## 🛠️ Development

### Using Programmatically

```python
from daf.core.simulation import SimulationRunner
from daf.config.models import SimulationConfig

# Create configuration
config = SimulationConfig(
    name="my_simulation",
    environment={"num_agents": 24, "map_size": [50, 50]},
    training={"total_timesteps": 100000},
)

# Run simulation
runner = SimulationRunner(config)
result = await runner.run()

print(f"Final reward: {result.metrics['total_reward']}")
```

### Custom Configuration

```python
from daf.core.configuration import ConfigurationManager

# Load and modify configuration
config_manager = ConfigurationManager()
config = config_manager.load_config_file("configs/experiments/arena_basic.yaml")

# Apply overrides
overrides = {"environment.num_agents": 32, "training.total_timesteps": 500000}
modified_config = config_manager.apply_overrides(config, overrides)

# Save for later use
config_manager.save_config(modified_config, "configs/experiments/my_custom.yaml")
```

## 📊 Understanding Results

Experiment results include:

- **Status**: success/failed/partial
- **Metrics**: reward, episode length, convergence time
- **Artifacts**: checkpoints, logs, analysis files
- **Metadata**: configuration, timing, system info

## 🔧 Troubleshooting

### Common Issues

**Installation Problems**
```bash
# Check system requirements
daf validate system

# Reinstall with fixes
python setup.py --clean --validate
```

**Configuration Errors**
```bash
# Validate configuration
daf validate config configs/experiments/my_experiment.yaml

# List available configs
daf run list
```

**Runtime Issues**
```bash
# Enable debug logging
export DAF_DEBUG=1
daf run experiment configs/experiments/my_experiment.yaml --verbose
```

### Getting Help

```bash
# CLI help
daf --help

# Command-specific help
daf run --help
daf install --help
daf validate --help

# Examples and documentation
cat examples/programmatic_usage.py
```

## 🎯 Next Steps

1. **Explore Examples**: Check `examples/` directory for code samples
2. **Read Documentation**: See `README.md` for detailed guides
3. **Customize**: Modify configurations in `configs/experiments/`
4. **Experiment**: Try different parameters and scenarios
5. **Analyze**: Examine results in `outputs/` directory

## 🚨 Important Notes

- **Python 3.11+** required
- **Metta AI** will be automatically installed
- **GPU** recommended for better performance
- **Results** saved to `outputs/` directory
- **Logs** available in `outputs/*/logs/`

---

**Ready to explore multi-agent reinforcement learning?** 🎉

Your DAF installation is complete and ready for research and experimentation!
