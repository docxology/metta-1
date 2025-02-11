from omegaconf import OmegaConf
import torch
import numpy as np
from mettagrid.renderer.raylib.raylib_renderer import MettaGridRaylibRenderer
from rl.pufferlib.vecenv import make_vecenv
from agent.policy_store import PolicyStore

def play(cfg: OmegaConf, policy_store: PolicyStore):
    device = cfg.device
    vecenv = make_vecenv(cfg.env, cfg.vectorization, num_envs=1, render_mode="human")

    obs, _ = vecenv.reset()
    env = vecenv.envs[0]
    policy_selector_cfg = OmegaConf.create({
            "uri": cfg.policy_uri,
            "type": "top",
            "range": 1,
            "metric": "elo",
            "filters": {}
        })

    policy_record = policy_store.policy(policy_selector_cfg)

    assert policy_record.metadata["action_names"] == env._c_env.action_names(), \
        f"Action names do not match: {policy_record.metadata['action_names']} != {env._c_env.action_names()}"
    policy = policy_record.policy()

    renderer = MettaGridRaylibRenderer(env._c_env, env._env_cfg.game)
    policy_rnn_state = None

    rewards = np.zeros(vecenv.num_agents)
    total_rewards = np.zeros(vecenv.num_agents)

    while True:
        with torch.no_grad():
            obs = torch.as_tensor(obs).to(device=device)

            # Parallelize across opponents
            if hasattr(policy, 'lstm'):
                actions, _, _, _, policy_rnn_state, _, _ = policy(obs, policy_rnn_state)
                if actions.dim() == 0:  # scalar tensor like tensor(2)
                    actions = torch.tensor([actions.item()])
            else:
                actions, _, _, _, _, _ = policy(obs) #if we are not using an RNN, then we don't need the rnn state

        renderer.update(
            env._c_env.unflatten_actions(actions.cpu().numpy()),
            obs,
            rewards,
            total_rewards,
            env._c_env.current_timestep(),
        )
        renderer.render_and_wait()
        actions = env._c_env.flatten_actions(renderer.get_actions())

        obs, rewards, dones, truncated, infos = vecenv.step(actions)
        total_rewards += rewards
        if any(dones) or any(truncated):
            print(f"Total rewards: {total_rewards}")
            break
