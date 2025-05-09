
import hydra
from omegaconf import DictConfig

from eval import simulate_policy
from rl.wandb.wandb_context import WandbContext
from util.runtime_configuration import setup_mettagrid_environment

@hydra.main(version_base=None, config_path="../configs", config_name="eval")
def main(cfg: DictConfig):
    setup_mettagrid_environment(cfg)
    with WandbContext(cfg) as wandb_run:
        simulate_policy(cfg, wandb_run)

if __name__ == "__main__":
    main()
