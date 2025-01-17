# tests/test_gym_env.py
import pytest
import numpy as np
import gym.envs
from zombpyg.gym_env import ZombpygGymEnv


def test_gym_env_observation():
    gym_env = ZombpygGymEnv(
        map_id="demo",
        rules_id="survival",
        player_specs="terminator:knife:0",
        initial_zombies=0,
        minimum_zombies=0, 
        verbose=False
    )
    observation, _ = gym_env.reset()
    feedback_size = gym_env.game.agent_builder.get_feedback_size()
    assert observation.shape == (1,feedback_size,1)
    assert np.all(observation <= 2.0)

def test_gym_env_registry():
    assert "zombpyg/Zombpyg-v0" in gym.envs.registry.keys()

