import random
import pygame
from pygame.locals import *
from itertools import cycle, islice
from zombpyg.map.map import MapFactory
from zombpyg.rules.factory import RulesFactory
from zombpyg.world import World
from zombpyg.core.wall import Wall
from zombpyg.agent import Agent, AgentBuilder
from zombpyg.core.zombie import ZombieBuilder
from zombpyg.utils.surroundings import Color
from zombpyg.core.weapons import Shotgun
from zombpyg.players.builder import PlayerBuilder

# GYM: Decide whether to conform to gym interface
# class ActionSpace(object):
#     def __init__(self, actions):
#         self.actions = actions
#         self.n = len(actions)

class AgentReward(object):
    class AgentState(object):
        def __init__(self, agent):
            self.alive = (agent.life > 0)
            self.life = agent.life
            self.healing_capacity = agent.healing_capacity
            self.zombies_killed = agent.zombies_killed
            self.fratricide = agent.fratricide
            self.friendly_fire = agent.friendly_fire
            self.accuracy = 100 * agent.attack_hits / agent.attack_count if agent.attack_count > 0 else 0
            self.adj_accuracy = min(max((agent.attack_count - 10)/40.0, 0.0), 1.0) * self.accuracy
            self.ammo_level = agent.weapon.ammo / agent.weapon.max_ammo if (agent.weapon is not None and agent.weapon.is_firearm) else 0.0
            self.healing_of_others = agent.healing_of_others

        def get_total_reward(self):
            return (
                self.life
                + self.healing_capacity/2.0
                + 5*self.zombies_killed 
                - 100 * self.fratricide 
                - 10 * self.friendly_fire
                + self.adj_accuracy/10.0
                + 100*self.ammo_level
                + self.healing_of_others
            )

    def __init__(self, agent):
        self.agent_state = AgentReward.AgentState(agent)

    def update(self, agent):
        prev_reward = self.agent_state.get_total_reward()
        self.agent_state = AgentReward.AgentState(agent)
        return self.agent_state.get_total_reward() - prev_reward

    def get_total_reward(self):
        return self.agent_state.get_total_reward()
        
class Game:
    """An instance of game controls the flow of the game.

       This includes player and zombies spawning, game main loop, deciding when
       to stop, importing map data, drawing each update, etc.
    """
    def __init__(
        self, w, h,
        map_id="demo",
        rules_id="survival",
        initial_zombies=0, minimum_zombies=0,
        agent_ids = ['robot'],
        agent_weapons="random",
        player_specs="",
        initialize_game=False,
        enable_rendering=True,
        verbose=False
    ):
        
        self.w = w
        self.h = h
        self.DISPLAYSURF = None
        self.fpsClock = None
        self.__initialize_renderer__()
        self.fps = 50
        
        self.obj_radius = 10
        self.robot_sensor_length = 250
        
        self.check_terminate = True
        
        self.agent_ids = agent_ids
        # The following processes the provided weapon names into a list of weapon names 
        # with length matching the length of agent_ids
        self.__process_weapon_name_inputs__(agent_weapons)

        self.map = MapFactory.build_map(map_id, self.w, self.h)
        self.initial_zombies = initial_zombies
        self.minimum_zombies = minimum_zombies

        self.world = World(self.map, 1.0/self.fps)
        self.agent_builder = AgentBuilder(
            self.obj_radius,
            Color.BLUE, 
            self.robot_sensor_length
        )
        self.zombie_builder = ZombieBuilder(self.obj_radius)

        self.rules_id = rules_id
        self.rules = RulesFactory.get_rules(self.rules_id, self.world, self.map.objectives)
        
        self.feedback_size = self.agent_builder.get_feedback_size()
        # Decide whether to use gym interface
        # self.action_space = ActionSpace(self.get_available_actions())

        self.__process_player_specs__(player_specs)

        self.verbose = verbose

        self.continue_without_agents = False

        # Initialize world, players, agents
        if initialize_game:
            self.reset()

    def __initialize_renderer__(self):
        if self.DISPLAYSURF is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('zombpyg')
            self.DISPLAYSURF = pygame.display.set_mode((self.w, self.h), 0, 32)
            self.set_display(self.DISPLAYSURF)
 
    def __process_player_specs__(self, player_specs):
        self.player_builders = []
        for player_spec in player_specs.split(','):
            player_spec_parts = player_spec.split(':')
            part_count = len(player_spec_parts)
            if (part_count == 0) or (player_spec_parts[0] == ""):
                continue
            else:
                weapon_id = player_spec_parts[1] if part_count >= 2 else 'random'
                player_id = player_spec_parts[0]
                player_count = int(player_spec_parts[2]) if part_count >= 3 else 1
                self.player_builders.extend(
                    [PlayerBuilder(player_id, weapon_id, self.obj_radius)] * player_count
                )

    def __process_weapon_name_inputs__(self, agent_weapons):
        agent_count = len(self.agent_ids) if self.agent_ids else 0
        if isinstance(agent_weapons, (str,)):
            self.agent_weapons = [agent_weapons] * agent_count
        elif isinstance(agent_weapons, (list,)):
            self.agent_weapons = list(islice(cycle(agent_weapons), agent_count))
        else:
            raise ValueError(f"{agent_weapons} is not a valid value for argument agent_weapons.  Value must be the weapon name as a string or a list of weapon names.")

    def spawn_resources(self):
        self.world.generate_resources(self.map.resource_spawns)

    def spawn_agents(self):
        for agent_id, agent_weapon in zip(self.agent_ids, self.agent_weapons):
            self.world.generate_agent(
                self.agent_builder, agent_id, agent_weapon, self.map.player_spawns
            )

    def spawn_players(self):
        for player_builder in self.player_builders:
            self.world.generate_player(player_builder, self.map.player_spawns)

    def spawn_zombies(self, count, initial_spawn=False):
        """Spawn N zombies in the world."""
        zombie_spawns = self.map.zombie_spawns
        if not initial_spawn: # exclude initial-only spawns
            zombie_spawns = [spawn for spawn in zombie_spawns if not spawn.initial_spawn_only]

        for _ in range(count):
            self.world.generate_zombie(
                self.zombie_builder, zombie_spawns
            )

    def spawn_zombies_to_maintain_minimum(self):
        """maintain the flow of zombies if necessary."""
        zombies = [zombie for zombie in self.world.zombies if zombie.life > 0]
        if len(zombies) < self.minimum_zombies:
            self.spawn_zombies(self.minimum_zombies - len(zombies), initial_spawn=False)

    def initialize_rewards(self):
        self.agent_rewards = list(
            map(AgentReward, self.world.agents)
        )
    
    def update_rewards(self):
        def apply_update(reward_agent_tuple):
            reward, agent = reward_agent_tuple
            return reward.update(agent)

        return list(
            map(apply_update, zip(self.agent_rewards, self.world.agents))
        )

    def reset(self):
        self.world.reset()
        self.agent_builder.reset()
        self.spawn_resources()
        self.spawn_agents()
        self.spawn_players()
        self.spawn_zombies(self.initial_zombies, initial_spawn=True)
        self.initialize_rewards()

    def get_feedback_size(self):
        return (self.feedback_size, 1)

    def play_actions(self, action_ids, num_frames=1):
        assert num_frames == 1

        feedbacks = self.world.step(action_ids)
        rewards = self.update_rewards()
        if self.verbose and any([reward != 0.0 for reward in rewards]):
            for agent_id, reward in zip(self.agent_ids, rewards):
                if reward != 0.0:
                    print(f"Reward for {agent_id}: {reward}")

        self.spawn_zombies_to_maintain_minimum()
       
        done = False
        truncated = False

        if self.rules.game_ended():
            won, description = self.rules.game_won()
            done = True
            if won:
                if self.verbose:
                    print(f"WIN!  {description}")
                # Grant the winners reward to the survivors
                for idx, agent in enumerate(self.world.agents):
                    if agent.life > 0:
                        rewards[idx] += 1000.0
            else:
                if self.verbose:
                    print(f"GAME OVER.  {description}")
        elif all([agent.life <= 0 for agent in self.world.agents]) and not self.continue_without_agents:
            if self.verbose:
                print("GAME OVER.  All agents dead.")
            done = True
        elif self.world.t >= 300:
            if self.verbose:
                print("GAME OVER.  Reached 300 seconds, stopping.")
            truncated = True

        observations = [feedback.reshape((1, len(feedback), 1)) for feedback in feedbacks]
        return rewards, observations, done, truncated
    
    def play_action(self, action_id, num_frames=1):
        rewards, observations, done, truncated = self.play_actions([action_id], num_frames=num_frames)
        return rewards[0], observations[0], done, truncated
    
    # This is used by the train method
    def get_total_reward(self):
        return self.agent_rewards[0].get_total_reward()
    
    # This is used by the train method
    # This might be useful for gym later.
    def get_available_actions(self):
        return self.agent_builder.get_actions()
    
    # This is used by the train method
    # This might be useful for gym later.
    def get_current_feedback(self, num_frames=1):
        assert num_frames == 1
        feedbacks = self.world.agents[0].sensor_feedback()
        return feedbacks.reshape((1, len(feedbacks), 1))
    
    def increase_fps(self):
        self.fps = min(300, self.fps+10)
        self.world.update_step_time_delta(1.0/self.fps)
        
    def decrease_fps(self):
        self.fps = max(1, self.fps-10)
        self.world.update_step_time_delta(1.0/self.fps)

    def set_display(self, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.fpsClock = pygame.time.Clock()

    def draw(self):
        if self.DISPLAYSURF is not None:
          # Draw objects
          self.DISPLAYSURF.fill(Color.BACKGROUND)
          self.world.draw(self)

          pygame.display.update()
          self.fpsClock.tick(self.fps)

          if self.verbose:
              time_used = self.fpsClock.get_rawtime()
              if time_used > 0:
                  print(f"Estimated FPS: {1000.0/time_used}")

    def close(self):
        if self.DISPLAYSURF is not None:
            pygame.display.quit()
            pygame.quit()
