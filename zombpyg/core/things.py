import random
import numpy
import pygame

from zombpyg.core.sensor import Sensor
from zombpyg.utils.surroundings import Color, get_movement_estimates
from zombpyg.utils.geometry import _valid_angle, get_angle_and_distance_to_point
from zombpyg.actions import (
    MoveableThing,
    RotatableThing,
    AttackingThing,
    ExecutableAction,
    ForwardMoveAction,
    RightMoveAction,
    BackwardMoveAction,
    LeftMoveAction,
    RotateAction,
    AttackAction
)


class Thing(object):
    """Something in the world."""
    MAX_LIFE = 1

    def __init__(
        self, name, color, life,
        dead_decoration=None,
    ):
        self.name = name
        self.color = color
        self.life = life
        self.status = u''
        self.dead_decoration = dead_decoration

    def next_step(self, things, t):
        return None

    def draw(self):
        pass

class CircularThing(Thing):
    def __init__(
        self, x, y, r,
        name, color, life,
        dead_decoration=None,
    ):
        super(CircularThing, self).__init__(
            name, color, life,
            dead_decoration=dead_decoration,
        )
        self.x = x
        self.y = y
        self.r = r
        
    def get_position(self):
        return self.x, self.y
    
    def get_radius(self):
        return self.r
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self, game):
        pygame.draw.circle(game.DISPLAYSURF, self.color, (self.x, self.y), self.r)

class RectangularThing(Thing):
    def __init__(
        self, left, top, width, height,
        name, color, life,
        dead_decoration=None,
    ):
        super(RectangularThing, self).__init__(
            name, color, life,
            dead_decoration=dead_decoration,
        )
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
    def draw(self, game):
        pygame.draw.rect(
            game.DISPLAYSURF, self.color, 
            (self.left, self.top, self.width, self.height)
        )

class Weapon(object):
    """Weapon, capable of doing damage to things."""
    def __init__(self, name, damage_range, max_range):
        self.name = name
        self.damage_range = damage_range
        self.max_range = max_range
    
    def get_weapon_id(self) -> int:
        pass
    
    def reset(self):
        pass

class FightingThing(CircularThing):
    """Thing that has a weapon."""
    def __init__(
        self,
        x, y, radius,
        name, color, life, weapon,
        dead_decoration=None
    ):
        super(FightingThing, self).__init__(
            x, y, radius,
            name, color, life,
            dead_decoration=dead_decoration
        )

        self.weapon = weapon
    
    def get_valid_position(self, x0, y0, x1, y1, world):
        dx = x1 - x0
        dy = y1 - y0
        angle = numpy.rad2deg(numpy.arctan2(dx, -dy))
        if angle >= -45 and angle <= 45:
            flag = world.collide_with_walls(x0, y0, x1-self.r, y1-self.r) or world.collide_with_walls(x0, y0, x1+self.r, y1-self.r)
        elif angle > 45 and angle <= 135:
            flag = world.collide_with_walls(x0, y0, x1+self.r, y1-self.r) or world.collide_with_walls(x0, y0, x1+self.r, y1+self.r)
        elif angle > 135 or angle < -135:
            flag = world.collide_with_walls(x0, y0, x1-self.r, y1+self.r) or world.collide_with_walls(x0, y0, x1+self.r, y1+self.r)
        else:
            flag = world.collide_with_walls(x0, y0, x1-self.r, y1-self.r) or world.collide_with_walls(x0, y0, x1-self.r, y1+self.r)
         
        if not flag:
            flag = world.fighter_collides_with_others(self, (x1, y1))

        if flag:
            x = x0
            y = y0
        else:
            x = x1
            y = y1

        if x < 0: x = 0
        if x >= world.w: x = world.w - 1
        if y < 0: y = 0
        if y >= world.h: y = world.h - 1

        return x, y

class DeadBody(CircularThing):
    """Dead body."""
    def __init__(self, r, name, color, display_time=2.0):
        super(DeadBody, self).__init__(
            0, 0, r,
            name, color, 0,
        )
        self.life = display_time

    def decrement_life(self, t):
        self.life -= t
