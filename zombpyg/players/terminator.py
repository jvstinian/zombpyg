import numpy
import random
import pygame

from zombpyg.core.player import Player
from zombpyg.core.bullet import Bullet
from zombpyg.core.sensor import Sensor
from zombpyg.utils.surroundings import Color, get_movement_estimates
from zombpyg.utils.geometry import _valid_angle, get_angle_and_distance_to_point
from zombpyg.core.weapons import Rifle
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

# This player is loosely inspired by the terminator from zombsole
class Terminator(Player, MoveableThing, RotatableThing, AttackingThing):
    """A player that stays still and shoots zombies."""
    vision_distance = 80
    peripheral_vision_angle = 75

    def __init__(self, x, y, radius, world, weapon=Rifle()):
        super(Terminator, self).__init__(
            x, y, radius,
            u'terminator', Color.BLUE,
            weapon,
        )
        
        self.minimum_rotation_angle = 5
        
        self.orientation = 0
        self.step_size = self.r / 5

        self.direction_actions_n = 2
        self.orientation_actions_n = 3
        self.orientation_actions = [-self.minimum_rotation_angle, 0, self.minimum_rotation_angle]
        self.actions_n = self.direction_actions_n + self.orientation_actions_n + 1

        self.step_forward = (0, int(-self.step_size))

        self.zombies_killed = 0
        self.attack_count = 0
        self.attack_hits = 0
        self.fratricide = 0
        self.friendly_fire = 0
        self.friendly_fire_avoided = 0

        self.world = world

    def next_step(self):
        action = None
        # Collect data on zombies
        detected_target, detected_distance, detected_angle = self.seek_target()
        if detected_target is not None:
            # If a player is seen, then re-orient if necessary.
            # If the angle to target is acceptable but is not in attack range, then pursue.
            # If the angle to target is acceptable and is in attack range, then attack.
            if detected_angle < -self.minimum_rotation_angle:
                orientation_action = 0
                action = RotateAction(self, self.orientation_actions[orientation_action])
            elif detected_angle > self.minimum_rotation_angle:
                orientation_action = 2
                action = RotateAction(self, self.orientation_actions[orientation_action])
            elif detected_distance > self.weapon.max_range: 
                action = ForwardMoveAction(self)
            else: 
                self.attack_target = detected_target
                action = AttackAction(self)
        else:
            distance_forward, has_gap_ahead, gap_ahead_width, gap_ahead_left_angle, gap_ahead_right_angle, angle_left_gap, angle_right_gap, surroundings = get_movement_estimates(
                self.get_position(), self.r, self.orientation, self.world.walls, self.vision_distance
            )
            if has_gap_ahead and (gap_ahead_width >= 3 * self.r):
                distweight = min(max(int(distance_forward/self.r) - 2, 0), 5)
                leftrotweight = 1 if gap_ahead_left_angle < -self.minimum_rotation_angle else 0
                rightrotweight = 1 if gap_ahead_right_angle > self.minimum_rotation_angle else 0
                backweight = 1
                noactionweight = 1
                action_choices = [
                    ForwardMoveAction(self),
                    BackwardMoveAction(self),
                    RotateAction(self, self.orientation_actions[0]),
                    RotateAction(self, self.orientation_actions[1]),
                    RotateAction(self, self.orientation_actions[2])
                ]
                action = random.choices(
                    action_choices,
                    weights=[distweight, backweight, leftrotweight, noactionweight, rightrotweight],
                    k=1
                )[0]
            else:
                # Note that the weight for a left rotation is the angle to the right-hand side gap, and 
                # the weight for a right rotation is the angle to the left-hand side gap.  
                # This means there's a higher probability of rotating to the side with an
                # opening at a smaller angle.
                action_choices = [
                    RotateAction(self, self.orientation_actions[0]),
                    RotateAction(self, self.orientation_actions[2])
                ]
                action = random.choices(
                    action_choices, weights=[angle_right_gap, numpy.abs(angle_left_gap)], k=1
                )[0]

        self.play_action(action)

    def update_steps(self):
        dx = int(self.step_size * numpy.sin(numpy.deg2rad(self.orientation)))
        dy = int(-self.step_size * numpy.cos(numpy.deg2rad(self.orientation)))
        self.step_forward = (dx, dy)

    def play_action(self, action: ExecutableAction):
        return action.execute_action()
    
    def move_forward(self) -> None:
        dx, dy = self.step_forward
        x0, y0 = self.x, self.y
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)

    def move_right(self) -> None:
        # Terminators don't (currently) move left or right
        pass

    def move_backward(self) -> None:
        dx, dy = self.step_forward
        dx = -dx
        dy = -dy
        x0, y0 = self.x, self.y
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)

    def move_left(self) -> None:
        # Terminators don't (currently) move left or right
        pass
    
    def rotate(self, angle: float):
        self.orientation = _valid_angle(self.orientation + angle)
        self.update_steps()
    
    def attack(self):
        self.weapon.use(self)

    def seek_target(self):
        targets = [zombie for zombie in self.world.zombies if zombie.life > 0]
        minimum_distance_to_target = self.vision_distance * 2.0
        detected_angle = None
        detected_target = None
        
        for target in targets:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, target.get_position())
            if distance >= self.vision_distance + target.r:
                continue

            rectified_angle = numpy.rad2deg(numpy.arctan2(target.r, distance))
            if angle < -self.peripheral_vision_angle-rectified_angle or angle > self.peripheral_vision_angle+rectified_angle:
                continue
            
            wall_point = None
            for wall in self.world.walls:
                wall_point = wall.collide(self.get_position(), target.get_position())
                if wall_point is not None:
                    # There's a wall between the (positions of the) terminator and target
                    break
            if wall_point is None:
                # no wall found betwen terminator and target
                if distance < minimum_distance_to_target:
                    minimum_distance_to_target = distance
                    detected_angle = angle
                    detected_target = target
        
        return detected_target, minimum_distance_to_target, detected_angle

    def draw(self, game):
        end = (
            self.x + 5 * self.step_forward[0],
            self.y + 5 * self.step_forward[1]
        )
        pygame.draw.circle(game.DISPLAYSURF, self.color, (self.x, self.y), self.r)
        pygame.draw.line(game.DISPLAYSURF, Color.WHITE, self.get_position(), end, 1)
 
