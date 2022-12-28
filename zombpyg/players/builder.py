from abc import ABC, abstractmethod
from .terminator import Terminator
from zombpyg.weapons import WeaponFactory

class PlayerBuilder(object):
    def __init__(self, player_id, weapon_id, radius):
        self.player_id = player_id
        self.weapon_id = weapon_id
        self.radius = radius

    def create_player(self, x, y, world):
        weapon = WeaponFactory.create_weapon(self.weapon_id)
        if self.player_id == "terminator":
            return Terminator(x, y, self.radius, world, weapon=weapon)
        else:
            return Terminator(x, y, self.radius, world, weapon=weapon)
