import random
import numpy
import pygame

from zombpyg.utils.surroundings import Color, get_movement_estimates
from zombpyg.actions import (
    MoveableThing,
    RotatableThing,
    AttackingThing,
    ExecutableAction,
    ForwardMoveAction,
    BackwardMoveAction,
    RotateAction,
    AttackAction
)

class Zombie(FightingThing, MoveableThing, RotatableThing, AttackingThing):
    MAX_LIFE = 100
    vision_distance = 60
    peripheral_vision_angle = 45

    def __init__(self, x, y, radius, world, orientation=0):
        life = random.randint(Zombie.MAX_LIFE / 2, Zombie.MAX_LIFE)
        dead_decoration = DeadBody(radius, 'zombie remains', Color.BRONZE)

        super(Zombie, self).__init__(
            x, y, radius,
            u'zombie', Color.DARK_RED, life, 
            ZombieClaws(), 
            dead_decoration
        )
        
        self.sensor_angle = 15
        
        self.orientation = orientation
        self.step_size = self.r / 5

        self.direction_actions_n = 2
        self.orientation_actions_n = 3
        self.orientation_actions = [-self.sensor_angle, 0, self.sensor_angle]
        self.actions_n = self.direction_actions_n + self.orientation_actions_n + 1

        self.update_steps()

        self.world = world

    def next_step(self):
        """Zombies attack if in range, else move in direction of a sighted player."""

        action = None
        # Use sensors to collect data on players and agents
        detected_player, detected_distance, detected_angle = self.seek_target()
        if detected_player is not None:
            print("Zombie found player!")
            # If a player is seen, then re-orient if necessary.
            # If the angle to target is acceptable but is not in attack range, then pursue.
            # If the angle to target is acceptable and is in attack range, then attack.
            if detected_angle < -self.sensor_angle:
                # action = self.direction_actions_n
                orientation_action = 0
                action = RotateAction(self, self.orientation_actions[orientation_action])
            elif detected_angle > self.sensor_angle:
                # action = self.direction_actions_n + 2
                orientation_action = 2
                action = RotateAction(self, self.orientation_actions[orientation_action])
            elif detected_distance > self.weapon.max_range: 
                # detected angle is within a reasonable range, 
                # but the target is too far away
                # action = 0 # move forward
                action = ForwardMoveAction(self)
            else: 
                self.targeted_player = detected_player
                action = AttackAction(self)
        else:
            # If no player is seen, but a wall is seen, then re-orient to point away
            # detected_walls, distances = self.detect_walls()
            # if detected_walls[1] is None:
            #     action = 0 # move forward
            # elif detected_walls[0] is None:
            #     action = self.direction_actions_n # Rotate left
            # elif detected_walls[2] is None:
            #     action = self.direction_actions_n + 2 # Rotate right
            # else:
            #     # If wall is seen in each direction, move or re-orient with uniform probability
            #     action = random.randint(0, self.direction_actions_n + self.orientation_actions_n - 1)
            distance_forward, has_gap_ahead, gap_ahead_width, gap_ahead_left_angle, gap_ahead_right_angle, angle_left_gap, angle_right_gap, surroundings = get_movement_estimates(
                self.get_position(), self.r, self.orientation, self.world.walls, self.vision_distance
            )
            if has_gap_ahead and (gap_ahead_width >= 3 * self.r):
                distweight = min(max(int(distance_forward/self.r) - 2, 0), 5)
                leftrotweight = 1 if gap_ahead_left_angle < -self.sensor_angle else 0
                rightrotweight = 1 if gap_ahead_right_angle > self.sensor_angle else 0
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
                    # range(0, self.direction_actions_n + self.orientation_actions_n),
                    action_choices,
                    weights=[distweight, backweight, leftrotweight, noactionweight, rightrotweight],
                    k=1
                )[0]
            else:
                print(f"angle to left gap: {angle_left_gap}, angle to right gap: {angle_right_gap}")
                # Note that the weight for a left rotation is the angle to the right-hand side gap, and 
                # the weight for a right rotation is the angle to the left-hand side gap.  
                # This means there's a higher probability of rotating to the side with an
                # opening at a smaller angle.
                action_choices = [
                    RotateAction(self, self.orientation_actions[0]),
                    RotateAction(self, self.orientation_actions[2])
                ]
                # action = self.direction_actions_n + random.choices([0, 2], weights=[angle_right_gap, numpy.abs(angle_left_gap)], k=1)[0]
                action = random.choices(
                    action_choices, weights=[angle_right_gap, numpy.abs(angle_left_gap)], k=1
                )[0]
                # if numpy.abs(angle_left_gap) <= angle_right_gap:
                #     action = self.direction_actions_n # Rotate left
                # else:
                #     action = self.direction_actions_n + 2 # Rotate right

        self.play_action(action)

        # # possible targets for movement and attack
        # humans = [thing for thing in things.values()
        #           if isinstance(thing, Player)]
        # positions = possible_moves(self.position, things)

        # if humans:
        #     # targets available
        #     target = closest(self, humans)

        #     if distance(self.position, target.position) < self.weapon.max_range:
        #         # target in range, attack
        #         action = 'attack', target
        #     else:
        #         # target not in range, _try_ to move
        #         if positions:
        #             # move
        #             best_position = closest(target, positions)
        #             action = 'move', best_position
        #         else:
        #             # if blocked by obstacles, try to break them
        #             adjacent = sort_by_distance(
        #                 target, adjacent_positions(self))
        #             for position in adjacent:
        #                 thing = things.get(position)
        #                 if isinstance(thing, (Box, Wall)):
        #                     return 'attack', thing
        # else:
        #     # no targets, just wander around
        #     if positions:
        #         action = 'move', random.choice(positions)

        # return action

    def update_steps(self):
        dx = int(self.step_size * numpy.sin(numpy.deg2rad(self.orientation)))
        dy = int(-self.step_size * numpy.cos(numpy.deg2rad(self.orientation)))
        self.step_forward = (dx, dy)

    def play_action(self, action: ExecutableAction):
        return action.execute_action()
    
    def move_forward(self) -> None:
        dx, dy = self.step_forward
        x0, y0 = self.x, self.y
        # x, y = self.world.get_valid_position(self.x, self.y, self.x+dx, self.y+dy)
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)

    def move_right(self) -> None:
        # Zombies don't move left or right
        pass

    def move_backward(self) -> None:
        dx, dy = self.step_forward
        dx = -dx
        dy = -dy
        x0, y0 = self.x, self.y
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)

    def move_left(self) -> None:
        # Zombies don't move left or right
        pass
    
    def rotate(self, angle: float):
        self.orientation = _valid_angle(self.orientation + angle)
        self.update_steps()
    
    def attack(self):
        if self.targeted_player is not None:
            damage = random.randint(*self.weapon.damage_range)
            self.targeted_player.life -= damage

    def seek_target(self):
        players = [
            agent for agent in self.world.agents if agent.life > 0
         ] + [
             player for player in self.world.players if player.life > 0
        ]
        # found_players = []
        minimum_distance_to_player = self.vision_distance * 2.0
        detected_angle = None
        detected_player = None
        
        for player in players:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, player.get_position())
            if distance >= self.vision_distance + player.r:
                continue
            
            if numpy.abs(angle) >= self.peripheral_vision_angle:
                continue
            
            wall_point = None
            for wall in self.world.walls:
                wall_point = wall.collide(self.get_position(), player.get_position())
                if wall_point is not None:
                    # There's a wall between the (positions of the) zombie and player
                    break
            if wall_point is None:
                # no wall found betwen zombie and player
                # found_players.append((distance, angle, player))
                if distance < minimum_distance_to_player:
                    minimum_distance_to_player = distance
                    detected_angle = angle
                    detected_player = player
        
        # return found_players
        return detected_player, minimum_distance_to_player, detected_angle

    def draw(self, game):
        end = (
            self.x + 5 * self.step_forward[0],
            self.y + 5 * self.step_forward[1]
        )
        pygame.draw.circle(game.DISPLAYSURF, self.color, (self.x, self.y), self.r)
        pygame.draw.line(game.DISPLAYSURF, Color.WHITE, self.get_position(), end, 1)

class ZombieBuilder(object):
    def __init__(self, radius):
        self.radius = radius

    def create_zombie(self, x, y, orientation, world):
        return Zombie(x, y, self.radius, world, orientation=orientation)
 