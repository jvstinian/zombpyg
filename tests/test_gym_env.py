# tests/test_gym_env.py
import pytest
import numpy as np
import gymnasium.envs
from zombpyg.gym_env import ZombpygGymEnv


def test_gym_env_observation():
    gym_env = ZombpygGymEnv(
        world_config={
            "tag": "SingleMap",
            "parameters": {
                "map_id": "demo",
                "w": 640, 
                "h": 480,
                "initial_zombies": 0, 
                "minimum_zombies": 0
            }
        },
        rules_id="survival",
        player_specs="terminator:knife:0",
        render_mode=None,
        verbose=False
    )
    observation, _ = gym_env.reset()
    feedback_size = gym_env.game.agent_builder.get_feedback_size()
    assert observation.shape == (1,feedback_size,1)
    assert np.all(observation <= 2.0)

def test_gym_env_registry():
    assert "jvstinian/Zombpyg-v0" in gymnasium.envs.registry.keys()
    assert "jvstinian/Zombpyg-v1" in gymnasium.envs.registry.keys()

