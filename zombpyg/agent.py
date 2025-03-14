import numpy, pygame
import bisect
from zombpyg.core.bullet import Bullet
from zombpyg.core.sensor import Sensor
from zombpyg.utils.geometry import _valid_angle, get_angle_and_distance_to_point, calculate_distance
from zombpyg.utils.surroundings import Color
from zombpyg.core.player import Player
from zombpyg.actions import (
    MoveableThing,
    RotatableThing,
    AttackingThing,
    HealingThing,
    ExecutableAction,
    ForwardMoveAction,
    RightMoveAction,
    BackwardMoveAction,
    LeftMoveAction,
    RotateAction,
    AttackAction,
    HealSelfAction,
    HealPlayerAction
)
from zombpyg.core.weapons import WeaponFactory


class AgentActions(object):
    direction_actions_n = 4
    orientation_actions = [-30.0, -5.0, -1.0, 0.0, 1.0, 5.0, 30.0]

    @classmethod
    def get_actions_n(cls):
        return cls.direction_actions_n + len(cls.orientation_actions) + 3

    @classmethod
    def get_forward_move_action_id(cls):
        return 0
    
    @classmethod
    def get_right_move_action_id(cls):
        return 1
    
    @classmethod
    def get_backward_move_action_id(cls):
        return 2
    
    @classmethod
    def get_left_move_action_id(cls):
        return 3
    
    @classmethod
    def get_no_action_id(cls):
        return cls.direction_actions_n + int(len(cls.orientation_actions)/2)
    
    @classmethod
    def get_smallest_left_rotation_action_id(cls):
        return cls.direction_actions_n + int(len(cls.orientation_actions)/2) - 1
    
    @classmethod
    def get_smallest_right_rotation_action_id(cls):
        return cls.direction_actions_n + int(len(cls.orientation_actions)/2) + 1
    
    @classmethod
    def get_use_weapon_action_id(cls):
        return cls.direction_actions_n + len(cls.orientation_actions)

    @classmethod
    def get_self_heal_action_id(cls):
        return cls.direction_actions_n + len(cls.orientation_actions) + 1
    
    @classmethod
    def get_heal_player_action_id(cls):
        return cls.direction_actions_n + len(cls.orientation_actions) + 2
    

class Agent(Player, MoveableThing, RotatableThing, AttackingThing):
    def __init__(
        self, 
        x, y, radius, world,
        agent_id, color, sensor_specs,
        weapon=None
    ):
        super().__init__(
            x, y, radius,
            'agent', color, weapon=weapon
        )
        self.agent_id = agent_id
        
        self.sensors = [
            Sensor([x, y], sensor_angle, sensor_length, world.walls, self) 
            for sensor_angle, sensor_length in sensor_specs
        ]
        self.max_sensor_length = max(list(map(lambda sensor: sensor.length, self.sensors)))
        
        self.orientation = 0
        self.step_size = self.r / 2

        self.direction_actions_n = AgentActions.direction_actions_n
        self.orientation_actions_n = len(AgentActions.orientation_actions)
        self.orientation_actions = AgentActions.orientation_actions
        self.actions_n = AgentActions.get_actions_n()

        self.step_forward = (0, int(-self.step_size))
        self.step_right = (int(self.step_size), 0)

        self.healing_capacity = Player.MAX_LIFE
        self.zombies_killed = 0
        self.attack_count = 0
        self.attack_hits = 0
        self.fratricide = 0
        self.friendly_fire = 0
        self.friendly_fire_avoided = 0
        self.healing_of_others = 0
        self.checkpoints_reached = 0

        self.world = world

    def update_steps(self):
        dx = int(self.step_size * numpy.sin(numpy.deg2rad(self.orientation)))
        dy = int(-self.step_size * numpy.cos(numpy.deg2rad(self.orientation)))
        self.step_forward = (dx, dy)
        self.step_right = (-dy, dx)

    """An interactive agent, with the next action determined by a separate process."""
    def play_action(self, action_id: int):
        action = self.get_action(action_id)
        action.execute_action()
    
    def get_action(self, action_id: int):
        if action_id < self.direction_actions_n:
            if action_id == 0:
                return ForwardMoveAction(self)
            elif action_id == 1:
                return RightMoveAction(self)
            elif action_id == 2:
                return BackwardMoveAction(self)
            elif action_id == 3:
                return LeftMoveAction(self)
            else:
                raise Exception("What's happening here?")
        elif (action_id >= self.direction_actions_n) and (action_id < self.direction_actions_n + self.orientation_actions_n):
            orientation_action = action_id - self.direction_actions_n
            dorientation = self.orientation_actions[orientation_action]
            return RotateAction(self, dorientation) # Do nothing
        elif action_id == (self.direction_actions_n + self.orientation_actions_n):
            return AttackAction(self)
        elif action_id == (self.direction_actions_n + self.orientation_actions_n + 1):
            return HealSelfAction(self)
        elif action_id == (self.direction_actions_n + self.orientation_actions_n + 2):
            return HealPlayerAction(self)
        else: # action_id >= self.actions_n:
            return RotateAction(self, 0.0) # Shouldn't happen but do nothing just in case

    def move_forward(self) -> None:
        self.status = 'moving'
        dx, dy = self.step_forward
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)
        for sensor in self.sensors:
            sensor.set_center(x, y)

    def move_right(self) -> None:
        self.status = 'moving'
        dx, dy = self.step_right
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)
        for sensor in self.sensors:
            sensor.set_center(x, y)

    def move_backward(self) -> None:
        self.status = 'moving'
        dx, dy = self.step_forward
        dx = -dx
        dy = -dy
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)
        for sensor in self.sensors:
            sensor.set_center(x, y)

    def move_left(self) -> None:
        self.status = 'moving'
        dx, dy = self.step_right
        dx = -dx
        dy = -dy
        x, y = self.get_valid_position(self.x, self.y, self.x+dx, self.y+dy, self.world)
        self.set_position(x, y)
        for sensor in self.sensors:
            sensor.set_center(x, y)
    
    def rotate(self, angle: float):
        self.status = 'rotating'
        self.orientation = _valid_angle(self.orientation + angle)
        self.update_steps()
        for sensor in self.sensors:
            sensor.set_orientation(self.orientation)
    
    def attack(self):
        self.weapon.use(self)

    def heal_self(self):
        self.status = 'healing self'
        if (self.life < Player.MAX_LIFE) and (self.healing_capacity > 0):
            self.life += 1
            self.healing_capacity -= 1
    
    def heal_player(self):
        self.status = 'healing player'
        target_player = self.find_heal_target()
        if target_player is not None:
            if (target_player.life < Player.MAX_LIFE) and (self.healing_capacity > 0):
                target_player.life += 1
                self.healing_capacity -= 1
                self.healing_of_others += 1
            
    def find_nearby_resources(self):
        consumption_angle = 60
        resources = self.world.get_resources()
        found_resources = []
        
        for resource in resources:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, resource.get_position())
            if distance >= self.r + resource.r:
                continue
            rectified_angle = numpy.rad2deg(numpy.arctan2(resource.r, distance))
            if angle >= -consumption_angle-rectified_angle and angle <= consumption_angle+rectified_angle:
                found_resources.append(resource)
        
        return found_resources
    
    def find_resources(self):
        resources = self.world.get_resources()
        ammo_distances = [2*sensor.length for sensor in self.sensors]
        medical_distances = [2*sensor.length for sensor in self.sensors]
        sensor_angles = list(map(lambda sensor: sensor.angle, self.sensors))
        
        for resource in resources:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, resource.get_position())
            if distance >= self.max_sensor_length + resource.r:
                continue
            
            rectified_angle = numpy.rad2deg(numpy.arctan2(resource.r, distance))
            lb = bisect.bisect_left(sensor_angles, angle - rectified_angle)
            ub = bisect.bisect_right(sensor_angles, angle + rectified_angle)
            for idx in range(lb, ub):
                if distance >= self.sensors[idx].length + resource.r:
                    continue
                if resource.resource_type == "ammo":
                    ammo_distances[idx] = min(ammo_distances[idx], distance)
                elif resource.resource_type == "medical":
                    medical_distances[idx] = min(medical_distances[idx], distance)

        return ammo_distances, medical_distances
        
    def detect_zombies(self):
        zombies = [zombie for zombie in self.world.zombies if zombie.life > 0]
        distances = [2*sensor.length for sensor in self.sensors]
        sensor_angles = list(map(lambda sensor: sensor.angle, self.sensors))
        
        for zombie in zombies:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, zombie.get_position())
            if distance >= self.max_sensor_length + zombie.r:
                continue
            rectified_angle = numpy.rad2deg(numpy.arctan2(zombie.r, distance))

            lb = bisect.bisect_left(sensor_angles, angle - rectified_angle)
            ub = bisect.bisect_right(sensor_angles, angle + rectified_angle)
            for idx in range(lb, ub):
                if distance >= self.sensors[idx].length + zombie.r:
                    continue
                distances[idx] = min(distances[idx], distance)
        
        return distances
        
    def detect_players(self):
        players_found = [
            (agent, 'agent') for agent in self.world.agents if agent.life > 0
        ] + [
            (player, 'player') for player in self.world.players if player.life > 0
        ] 
        distances = [2*sensor.length for sensor in self.sensors]
        sensor_angles = list(map(lambda sensor: sensor.angle, self.sensors))

        for player, _ in players_found:
            if player == self:
                continue
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, player.get_position())
            if distance >= self.max_sensor_length + player.r:
                continue
            rectified_angle = numpy.rad2deg(numpy.arctan2(player.r, distance))

            lb = bisect.bisect_left(sensor_angles, angle - rectified_angle)
            ub = bisect.bisect_right(sensor_angles, angle + rectified_angle)
            for idx in range(lb, ub):
                if distance >= self.sensors[idx].length + player.r:
                    continue
                distances[idx] = min(distances[idx], distance)
        
        return distances
    
    def find_heal_target(self):
        heal_distance = 4 * self.r
        max_heal_angle = 30.0
        players = [
            agent for agent in self.world.agents if agent.life > 0
        ] + [
            player for player in self.world.players if player.life > 0
        ]
        min_distance = 1.01 * heal_distance # Set larger than healing distance
        target_player = None
        
        for player in players:
            if player == self:
                continue
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, player.get_position())
            if distance >= heal_distance:
                continue
            
            rectified_angle = numpy.rad2deg(numpy.arctan2(player.r, distance))
            if angle >= -max_heal_angle-rectified_angle and angle <= max_heal_angle+rectified_angle:
                if distance < min_distance:
                    min_distance = min(min_distance, distance)
                    target_player = player
        
        return target_player
    
    def detect_wall(self):
        return [sensor.detect_wall() for sensor in self.sensors]
    
    def detect_objective(self):
        objectives = self.world.get_objectives()
        distances = []

        if any([objective.contains(self.get_position()) for objective in objectives]):
            distances = [0] * len(self.sensors)
        else:
            for sensor in self.sensors:
                distance = sensor.detect_objective(objectives)
                distances.append(distance)
        return distances
    
    def sensor_feedback(self):
        thres = 2
        feedbacks = numpy.ones((len(self.sensors), 8), dtype="float32") * thres
        
        # Set state
        feedbacks[:, 7] = numpy.zeros((len(self.sensors),), dtype="float32")
        feedbacks[0, 7] = self.life / Player.MAX_LIFE
        feedbacks[1, 7] = self.healing_capacity / Player.MAX_LIFE
        if self.weapon is not None:
            feedbacks[2, 7] = self.weapon.get_weapon_id() / 64.0 # else keep 0
        if self.weapon is not None and self.weapon.is_firearm:
            feedbacks[3, 7] = self.weapon.ammo / self.weapon.max_ammo
        
        # resources
        ammo_distances, medical_distances = self.find_resources()
        for i, distance in enumerate(ammo_distances):
            feedbacks[i, 0] = min(feedbacks[i, 0], distance/self.sensors[i].length)
        for i, distance in enumerate(medical_distances):
            feedbacks[i, 1] = min(feedbacks[i, 1], distance/self.sensors[i].length)

        zombie_distances = self.detect_zombies()
        for i, distance in enumerate(zombie_distances):
            feedbacks[i, 2] = min(feedbacks[i, 2], distance/self.sensors[i].length)

        player_distances = self.detect_players()
        for i, distance in enumerate(player_distances):
            feedbacks[i, 3] = min(feedbacks[i, 3], distance/self.sensors[i].length)

        # objectives
        objective_distances_by_sensor = self.detect_objective()
        for i in range(len(self.sensors)):
            feedbacks[i, 4] = objective_distances_by_sensor[i] / self.sensors[i].length

        # checkpoints
        checkpoint_distances_by_sensor = self.find_checkpoints()
        for i in range(len(self.sensors)):
            feedbacks[i, 5] = checkpoint_distances_by_sensor[i] / self.sensors[i].length

        distances = self.detect_wall()
        for i in range(len(self.sensors)):
            feedbacks[i, 6] = distances[i] / self.sensors[i].length
            if feedbacks[i, 0] > feedbacks[i, 6]:
                feedbacks[i, 0] = thres
            if feedbacks[i, 1] > feedbacks[i, 6]:
                feedbacks[i, 1] = thres
            if feedbacks[i, 2] > feedbacks[i, 6]:
                feedbacks[i, 2] = thres
            if feedbacks[i, 3] > feedbacks[i, 6]:
                feedbacks[i, 3] = thres
            if feedbacks[i, 4] > feedbacks[i, 6]:
                feedbacks[i, 4] = thres
            if feedbacks[i, 5] > feedbacks[i, 6]:
                feedbacks[i, 5] = thres
        
        return feedbacks.flatten()
    
    def consume_nearby_resource(self):
        resources = self.find_nearby_resources()
        
        for resource in resources:
            resource.use_by(self)
    
    def find_nearby_checkpoints(self):
        consumption_angle = 60
        checkpoints = self.world.get_checkpoints()
        found_checkpoints = []
        
        for checkpoint in checkpoints:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, checkpoint.get_position())
            if distance >= self.r + checkpoint.r:
                continue
            rectified_angle = numpy.rad2deg(numpy.arctan2(checkpoint.r, distance))
            if angle >= -consumption_angle-rectified_angle and angle <= consumption_angle+rectified_angle:
                found_checkpoints.append(checkpoint)
        
        return found_checkpoints
    
    def check_in_to_nearby_checkpoints(self):
        checkpoints = self.find_nearby_checkpoints()
        
        for checkpoint in checkpoints:
            checkpoint.check_in(self)
    
    def find_checkpoints(self):
        checkpoints= self.world.get_checkpoints()
        checkpoint_distances = [2*sensor.length for sensor in self.sensors]
        sensor_angles = list(map(lambda sensor: sensor.angle, self.sensors))
        
        for checkpoint in checkpoints:
            angle, distance, _ = get_angle_and_distance_to_point(self.get_position(), self.orientation, checkpoint.get_position())
            if distance >= self.max_sensor_length + checkpoint.r:
                continue
            
            rectified_angle = numpy.rad2deg(numpy.arctan2(checkpoint.r, distance))
            lb = bisect.bisect_left(sensor_angles, angle - rectified_angle)
            ub = bisect.bisect_right(sensor_angles, angle + rectified_angle)
            for idx in range(lb, ub):
                if distance >= self.sensors[idx].length + checkpoint.r:
                    continue
                checkpoint_distances[idx] = min(checkpoint_distances[idx], distance)

        return checkpoint_distances
    
    def draw(self, game):
        super().draw(game)
        for sensor in self.sensors:
            sensor.draw(game)
        
    def is_at_objective(self):
        if any([objective.contains(self.get_position()) for objective in self.world.get_objectives()]):
            return True
        return False

class AgentBuilder(object):
    def __init__(
        self, radius, color, 
        front_sensor_length,
        friendly_fire_guard=False
    ):
        self.radius = radius
        self.color = color 
        self.sensor_specs = [
            (-165 + 15*idx, 50) for idx in range(7)
        ] + [
            (-60 + 5*idx, front_sensor_length) for idx in range(25)
        ] + [
            (75 + 15*idx, 50) for idx in range(7)
        ]
        self.friendly_fire_guard = friendly_fire_guard
    
    def build(self, agent_id, x, y, weapon_id, world):
        weapon = WeaponFactory.create_weapon(weapon_id, friendly_fire_guard=self.friendly_fire_guard)
        return Agent(
            x, y, self.radius, world,
            agent_id, self.color, self.sensor_specs,
            weapon=weapon
        )
    
    def get_feedback_size(self):
        return 8 * len(self.sensor_specs)

    def get_actions(self):
        actions_n = AgentActions.get_actions_n() # 4 + 5 + 3
        return list(range(actions_n))
