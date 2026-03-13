# tests/test_gym_env.py
import pytest
from tests.helpers import not_raises
import numpy as np
import gymnasium as gym
import gymnasium.envs
from gymnasium.utils.env_checker import check_env
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

def test_gym_make_env_v0():
    env = gym.make("jvstinian/Zombpyg-v0", render_mode=None)
    with not_raises(Exception):
        check_env(env.unwrapped, skip_render_check=True)

def test_gym_make_env_v1():
    env = gym.make("jvstinian/Zombpyg-v1", render_mode=None)
    with not_raises(Exception):
        check_env(env.unwrapped, skip_render_check=True)

