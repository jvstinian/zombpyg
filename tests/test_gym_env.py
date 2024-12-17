# tests/test_gym_env.py
import pytest
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
    observation = gym_env.reset()
    feedback_size = gym_env.game.agent_builder.get_feedback_size()
    assert observation.shape == (1,feedback_size,1)
