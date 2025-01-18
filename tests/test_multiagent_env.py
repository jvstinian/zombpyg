# tests/test_multiagent_env.py
import pytest
import numpy as np
from zombpyg.multiagent_env import MultiagentZombpygEnv


@pytest.fixture(scope="function", name="env1p")
def env1p_fixture():
    env = MultiagentZombpygEnv(
        map_id="demo",
        rules_id="extermination",
        initial_zombies=1,
        minimum_zombies=0, 
        agent_ids = [0],
        agent_weapons="rifle",
        player_specs="",
        enable_rendering=False,
        verbose=False
    )
    return env


@pytest.fixture(scope="function", name="env2p")
def env2p_fixture():
    env = MultiagentZombsoleEnv(
        map_id="demo",
        rules_id="extermination",
        initial_zombies=1,
        minimum_zombies=0, 
        agent_ids = [0, 1],
        agent_weapons="random",
        player_specs="",
        enable_rendering=False,
        verbose=False
    )
    return env


@pytest.fixture(scope="function", name="env10p")
def env32p_fixture():
    env = MultiagentZombsoleEnv(
        map_id="demo",
        rules_id="extermination",
        initial_zombies=100,
        minimum_zombies=0, 
        agent_ids = list(range(0, 10)),
        agent_weapons="random",
        player_specs="",
        enable_rendering=False,
        verbose=False
    )
    return env


def test_multiagent_env_shape(env1p):
    observations, _ = env1p.reset()
    feedback_size = env1p.game.agent_builder.get_feedback_size()
    for agent_id in observations:
        observation = observations[agent_id]
        assert observation.shape == (1,feedback_size,1)
        assert np.all(observation <= 2.0)

def test_multiagent_1pgame(env1p):
    stepcount = 0
    while True:
        _, _, done, truncated, _ = env1p.step([
            env1p.action_spaces[agent_id].sample()
            for agent_id in env1p.agents
        ])

        if done or truncated or (stepcount >=10):
            break

        stepcount += 1

    assert True

# def test_multiagent_targeted_heal(env2p):
#     env2p.game.agents[1].life = 25
#     agent1pos = env2p.game.agents[1].position
#     agent0pos = env2p.game.agents[0].position
#     relativepos = (agent1pos[0] - agent0pos[0], agent1pos[1] - agent0pos[1])
# 
#     _ = env2p.step([
#         {
#             "agent_id": 0,
#             "action_type": "heal",
#             "parameter": relativepos
#         }
#     ])
# 
#     assert env2p.game.agents[1].agent_id == 1
#     assert env2p.game.agents[1].life > 25
# 
# def test_multiagent_large_game(env32p):
#     stepcount = 0
#     while True:
#         _, _, done, truncated, _ = env32p.step([
#             {
#                 "agent_id": idx,
#                 "action_type": "attack_closest",
#                 "parameter": [0, 0]
#             } for idx in range(0, 32)
#         ])
# 
#         if done or truncated or (stepcount >=200):
#             break
# 
#         stepcount += 1
# 
#     assert True

