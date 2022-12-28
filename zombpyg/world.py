import random
import numpy
import pygame

from zombpyg.utils.geometry import _valid_angle
from zombpyg.utils.surroundings import Color
from zombpyg.object import Wall
from zombpyg.agent import Agent
from zombpyg.things import Zombie
from zombpyg.weapons import Rifle
from zombpyg.players.terminator import Terminator


class World(object):
    """World where the game is played"""
    def __init__(self, map, step_time_delta):
        self.size = map.size
        self.w = self.size[0]
        self.h = self.size[1]
        self.step_time_delta = step_time_delta
        
        self.resources = {}
        self.walls = map.walls
        self.objectives = map.objectives
        self.decorations = []
        self.agents = []
        self.players = []
        self.zombies = []
        self.bullets = []

        self.t = 0
        self.events = []
        self.deaths = 0
        self.zombie_deaths = 0
        self.player_deaths = 0
    
    def reset(self):
        self.t = 0
        self.resources = {}
        self.decorations = []
        self.agents = []
        self.players = []
        self.zombies = []
        self.bullets = []
    
    def update_step_time_delta(self, new_time_delta):
        self.step_time_delta = new_time_delta

    def get_resources(self):
        return list(self.resources.values())
    
    def get_walls(self):
        return self.walls
    
    def get_objectives(self):
        return self.objectives
    
    def get_agents_health(self):
        return sum([agent.life for agent in self.agent])

    def get_players_health(self):
        return sum([player.life for player in self.player if player.life > 0])

    def event(self, thing, message):
        """Log an event."""
        self.events.append((self.t, thing, message))

    def step(self, action_ids):
        """Forward one instant of time."""
        self.t += self.step_time_delta
        
        for bullet in self.bullets:
            bullet.next_step()

        actions = self.get_agent_actions(action_ids)
        random.shuffle(actions)
        self.execute_agent_actions(actions)
        self.execute_fighter_actions()

        # process resources
        for robot in self.agents:
            robot.consume_nearby_resource()
            
        feedbacks = self.agents[0].sensor_feedback()
        
        self.clean_dead_things()

        return feedbacks

    def collide_with_walls(self, x0, y0, x1, y1):
        flag = False
        for wall in self.walls:
            point = wall.collide((x0, y0), (x1, y1))
            if point is not None:
                flag = True
                break
        return flag
    
    def generate_resources(self, resource_spawns):
        for resource_spawn in resource_spawns:
            resource = resource_spawn.spawn_resource()
            position = resource.get_position()
            if self.resources.get(position, None) is None:
                self.resources[position] = resource
    
    def remove_resource(self, resource):
        x, y = resource.get_position()
        if self.resources.get((x, y), None) is not None:
            del self.resources[(x, y)]

    def generate_agent(self, agent_builder, agent_id, spawns):
        spawn = random.choices(spawns, k=1)[0]
        while True:
            x, y = spawn.get_spawn_location()
            radius = agent_builder.radius * 2
            
            if self.collide_with_walls(x-radius, y-radius, x+radius, y+radius):
                continue
            if self.collide_with_walls(x-radius, y+radius, x+radius, y-radius):
                continue

            self.agents.append(
                agent_builder.build(agent_id, x, y, self)
            )
            break
        
    def generate_player(self, player_builder, spawns):
        spawn = random.choices(spawns, k=1)[0]
        while True:
            x, y = spawn.get_spawn_location()
            radius = player_builder.radius * 2
            
            if self.collide_with_walls(x-radius, y-radius, x+radius, y+radius):
                continue
            if self.collide_with_walls(x-radius, y+radius, x+radius, y-radius):
                continue
            
            self.players.append(
                player_builder.create_player(x, y, self)
            )
            break

    def generate_zombie(self, zombie_builder, spawns):
        spawn = random.choices(spawns, k=1)[0]
        while True:
            x, y = spawn.get_spawn_location()
            orientation = _valid_angle(random.uniform(-180.0, 180.0))
            radius = zombie_builder.radius * 2
            
            if self.collide_with_walls(x-radius, y-radius, x+radius, y+radius):
                continue
            if self.collide_with_walls(x-radius, y+radius, x+radius, y-radius):
                continue
            
            self.zombies.append(
                zombie_builder.create_zombie(x, y, orientation, self)
            )
            break

    def add_bullet(self, bullet):
        self.bullets.append(bullet)
    
    def get_agent_actions(self, action_ids):
        actions = []
        for agent, action_id in zip(self.agents, action_ids):
            if agent.life > 0:
                actions.append(
                    agent.get_action(action_id)
                )
        return actions
        
    def execute_agent_actions(self, actions):
        for action in actions:
            action.execute_action()
    
    def execute_fighter_actions(self):
        fighters = self.players + self.zombies
        random.shuffle(fighters)
        for fighter in fighters:
            if fighter.life > 0:
                fighter.next_step()

    def clean_dead_things(self):
        self.bullets = list(filter(lambda bullet: bullet.active, self.bullets))
        self.clean_dead_resource()
        self.clean_dead_zombies()
        self.clean_dead_players()
        self.decorations = [decoration for decoration in self.decorations if decoration.life > 0]
    
    def clean_dead_resource(self):
        dead_resources = []
        for resource in self.resources.values():
            if resource.is_used_up():
                dead_resources.append(resource)

        for resource in dead_resources:
            self.remove_resource(resource)

    def clean_dead_zombies(self):
        """Remove dead things, and add dead decorations."""
        dead_zombies = [zombie for zombie in self.zombies if zombie.life <= 0]
        self.zombies = [zombie for zombie in self.zombies if zombie.life > 0]
        for thing in dead_zombies:
            if thing.dead_decoration is not None:
                x, y = thing.get_position()
                thing.dead_decoration.set_position(x, y)
                self.decorations.append(thing.dead_decoration)

            self.event(thing, u'died')
            self.zombie_deaths += 1
            self.deaths += 1

    def clean_dead_players(self):
        """Remove dead players, and add dead decorations."""
        dead_players = [player for player in self.players if player.life <= 0]
        self.players = [player for player in self.players if player.life > 0]
        for thing in dead_players:
            if thing.dead_decoration is not None:
                x, y = thing.get_position()
                thing.dead_decoration.set_position(x, y)
                self.decorations.append(thing.dead_decoration)

            self.event(thing, u'died')
            self.player_deaths += 1
            self.deaths += 1

    def draw(self, game):
        # Draw objects
        for objective in self.objectives:
            objective.draw(game)
        for resource in self.resources.values():
            resource.draw(game)
        for wall in self.walls:
            wall.draw(game)
        for decoration in self.decorations:
            decoration.draw(game)
            # As we've drawn the decoration, we decrement it's remaining "life"
            decoration.decrement_life(self.step_time_delta)
        for agent in self.agents:
            agent.draw(game)
        for player in self.players:
            player.draw(game)
        for zombie in self.zombies:
            zombie.draw(game)
        for bullet in self.bullets:
            bullet.draw(game)
