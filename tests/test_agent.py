# tests/agent.py
import pytest
from zombpyg.utils.surroundings import Color
from zombpyg.agent import AgentBuilder
from zombpyg.core.weapons import WeaponFactory


# class DummyMap(object):
#     def __init__(self):
#         self.walls = []


class DummyWorld(object):
    def __init__(self):
        # self.map = DummyMap()
        self.walls = []
        # self.step_time_delta = step_time_delta # TODO


# The following mostly just tests that we can instantiate an agent.
# We field in a dummy world (with map) with the bare minimum of fields required.
def test_agent_icon_basic():
    shotgun = WeaponFactory.create_weapon("shotgun")
    obj_radius = 10
    robot_sensor_length = 250
    agent_id = 0
    w = 640
    h = 480

    x = w / 2
    y = h / 2

    world = DummyWorld()
    
    agent_builder = AgentBuilder(
        obj_radius,
        Color.BLUE, 
        robot_sensor_length,
        weapon=shotgun
    )

    agent = agent_builder.build(0, x, y, world)
    assert agent.agent_id == 0
    assert agent.x == x
    assert agent.y == y
    assert agent.r == obj_radius
    assert agent.weapon.name.lower() == "shotgun"

