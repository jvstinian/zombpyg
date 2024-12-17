# tests/test_gym_env.py
import pytest
from zombpyg.gym_env import ZombpygGymEnv


def test_gym_env_observation():
    gym_env = ZombsoleGymEnv(
        map_id="demo",
        rules_id="survival",
        player_specs="terminator:knife:0",
        initial_zombies=0,
        minimum_zombies=0, 
        verbose=False
    ):
    )
    observation = gym_env.get_observation()
    sensor_count = len(gym_env.game.agent_builder.sensor_specs)
    sensor_channels = 7
    assert observation.shape == (1,sensor_count*sensor_channels,2)

