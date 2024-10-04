#!/usr/bin/env python
# coding: utf-8
from os import path, system
# import gym
from gym.core import Env
from gym.spaces.discrete import Discrete
from gym.spaces.box import Box
from gym.envs.registration import register
# from gym import error
# from gym.utils import closer
from zombpyg.game import Game
from zombpyg.agent import AgentActions
import time
import numpy as np

# TODO: Other approach        
from threading import Thread
import pygame

# env_closer = closer.Closer()

class ZombpygGymEnv(object):
    """The main OpenAI Gym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed.

    The main API methods that users of this class need to know are:

        step
        reset
        render
        close
        seed

    And set the following attributes:

        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards

    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.

    The methods are accessed publicly as "step", "reset", etc...
    """
    # Set this in SOME subclasses
    metadata = {'render.modes': ['human', 'ansi']}
    reward_range = (-float('inf'), float('inf'))
    # spec = None

    # TODO: Is this needed?
    # game_actions = [
    #     { 
    #         'action_type': 'move',
    #         'parameter': [0, 1]
    #     },
    #     { 
    #         'action_type': 'move',
    #         'parameter': [-1, 0]
    #     },
    #     { 
    #         'action_type': 'move',
    #         'parameter': [0, -1]
    #     },
    #     { 
    #         'action_type': 'move',
    #         'parameter': [1, 0]
    #     },
    #     {
    #         'action_type': 'attack_closest'
    #     },
    #     {
    #         'action_type': 'heal'
    #     }
    # ]

    # Set these in ALL subclasses
    # TODO: Can this be a member of the instance and not a class variable?
    # action_space = Discrete(len(game_actions))
    # observation_space = None

    def __init__(
        self,
        map_id="demo",
        rules_id="survival",
        initial_zombies=0, minimum_zombies=0,
        # agent_ids = ['robot'], # TODO
        player_specs="", 
        verbose=False
    ):
        # self.game = game
    
        # def _render(game):
        #     while True:
        #         game.draw()
        #         for event in pygame.event.get():
        #             if event.type == pygame.KEYDOWN:
        #                 if event.key == pygame.K_9:
        #                     game.increase_fps()
        #                 elif event.key == pygame.K_0:
        #                     game.decrease_fps()    
        # pygame.init()
        # DISPLAYSURF = pygame.display.set_mode((640, 480), 0, 32)
        # pygame.display.set_caption('zombpyg')
        self.window = None
        self.game = Game(
            640, 480, None, # DISPLAYSURF,  # TODO
            map_id=map_id,
            rules_id=rules_id,
            initial_zombies=initial_zombies,
            minimum_zombies=minimum_zombies,
            player_specs=player_specs,
            verbose=verbose,
        )
        # game = Game(640, 480, DISPLAYSURF, initial_zombies=8, minimum_zombies=1, rules_id="safehouse", map_id="open_room") #, player_specs="terminator:axe:1")
        # self.t = Thread(target=lambda: _render(self.game))
        # self.t.start()
        
        # game = Game(640, 480, DISPLAYSURF, initial_zombies=20, minimum_zombies=10, rules_id="safehouse")

        # self.action_space = Discrete(game.get_available_actions()) # TODO: See above
        self.action_space = Discrete(AgentActions.get_actions_n()) # TODO: See above
        self.observation_space = Box(low=0.0, high=400.0, shape=self.game.get_feedback_size())

    def get_observation(self):
        # TODO: make a method for retrieving state
        # observation = {
        #     'world': self.draw_world_simple(),
        #     'ticks': self.world.t,
        #     'deaths': self.world.deaths,
        #     'players': [
        #         (
        #             player.name,
        #             player.life,
        #             player.position[0],
        #             player.position[1],
        #             player.weapon.name, # or 'unarmed'
        #         ) for player in (self.players + self.agents)
        #     ]
        # }

        # TODO: Commenting out the following
        # observation = np.array(self.encode_world_simple())
        # return observation.reshape( (1,) + observation.shape )
        # TODO: Looks like the shape already has a leading (1,)
        return self.game.get_current_feedback()
    
    def get_frame_size(self):
        # TODO: The following was commented out
        # return tuple(reversed(self.map.size))
        return self.game.get_feedback_size()


    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        reward, observation, done = self.game.play_action(action)
        info = {}
            
        return observation, reward, done, info


    def reset(self):
        """Resets the environment to an initial state and returns an initial
        observation.

        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.

        Returns:
            observation (object): the initial observation.
        """
        self.game.reset()
        # super(ZombsoleGymEnv, self).__initialize_world__() # TODO
        return self.get_observation()

    def __render_human__(self):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption('zombpyg')
            self.window = pygame.display.set_mode((self.game.w, self.game.h), 0, 32)
            self.game.set_display(self.window)
        
        self.game.draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    self.game.increase_fps()
                elif event.key == pygame.K_0:
                    self.game.decrease_fps()
        
    def render(self, mode='human'):
        """Renders the environment.

        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:

        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).

        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.

        Args:
            mode (str): the mode to render with

        Example:

        class MyEnv(Env):
            metadata = {'render.modes': ['human', 'rgb_array']}

            def render(self, mode='human'):
                if mode == 'rgb_array':
                    return np.array(...) # return RGB frame suitable for video
                elif mode == 'human':
                    ... # pop up a window and render
                else:
                    super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        if mode == 'human':
            # system('clear') # TODO: What do we do with this?
            # print(self.draw_world())
            # self.game.draw()
            self.__render_human__()
            return None
        else:
            raise ValueError("mode={} is not supported".format(mode))

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        # pass
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
        # self.t.join() # TODO

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        # NOTE: Not currently capturing the seed information used in zombsole
        return

    @property
    def unwrapped(self):
        """Completely unwrap this env.

        Returns:
            gym.Env: The base non-wrapped gym.Env instance
        """
        return self

    def __str__(self):
        if self.spec is None:
            return '<{} instance>'.format(type(self).__name__)
        else:
            return '<{}<{}>>'.format(type(self).__name__, self.spec.id)

    def __enter__(self):
        """Support with-statement for the environment. """
        return self

    def __exit__(self, *args):
        """Support with-statement for the environment. """
        self.close()
        # propagate exception
        return False

register(
    id='zombpyg/Zombpyg-v0', 
    entry_point='zombpyg.gym_env:ZombpygGymEnv', 
    max_episode_steps=300*50,
    kwargs={
    }
)

# class GoalEnv(Env):
#     """A goal-based environment. It functions just as any regular OpenAI Gym environment but it
#     imposes a required structure on the observation_space. More concretely, the observation
#     space is required to contain at least three elements, namely `observation`, `desired_goal`, and
#     `achieved_goal`. Here, `desired_goal` specifies the goal that the agent should attempt to achieve.
#     `achieved_goal` is the goal that it currently achieved instead. `observation` contains the
#     actual observations of the environment as per usual.
#     """

#     def reset(self):
#         # Enforce that each GoalEnv uses a Goal-compatible observation space.
#         if not isinstance(self.observation_space, gym.spaces.Dict):
#             raise error.Error('GoalEnv requires an observation space of type gym.spaces.Dict')
#         for key in ['observation', 'achieved_goal', 'desired_goal']:
#             if key not in self.observation_space.spaces:
#                 raise error.Error('GoalEnv requires the "{}" key to be part of the observation dictionary.'.format(key))

#     def compute_reward(self, achieved_goal, desired_goal, info):
#         """Compute the step reward. This externalizes the reward function and makes
#         it dependent on a desired goal and the one that was achieved. If you wish to include
#         additional rewards that are independent of the goal, you can include the necessary values
#         to derive it in 'info' and compute it accordingly.

#         Args:
#             achieved_goal (object): the goal that was achieved during execution
#             desired_goal (object): the desired goal that we asked the agent to attempt to achieve
#             info (dict): an info dictionary with additional information

#         Returns:
#             float: The reward that corresponds to the provided achieved goal w.r.t. to the desired
#             goal. Note that the following should always hold true:

#                 ob, reward, done, info = env.step()
#                 assert reward == env.compute_reward(ob['achieved_goal'], ob['goal'], info)
#         """
#         raise NotImplementedError


# class Wrapper(Env):
#     """Wraps the environment to allow a modular transformation.

#     This class is the base class for all wrappers. The subclass could override
#     some methods to change the behavior of the original environment without touching the
#     original code.

#     .. note::

#         Don't forget to call ``super().__init__(env)`` if the subclass overrides :meth:`__init__`.

#     """
#     def __init__(self, env):
#         self.env = env
#         self.action_space = self.env.action_space
#         self.observation_space = self.env.observation_space
#         self.reward_range = self.env.reward_range
#         self.metadata = self.env.metadata

#     def __getattr__(self, name):
#         if name.startswith('_'):
#             raise AttributeError("attempted to get missing private attribute '{}'".format(name))
#         return getattr(self.env, name)

#     @property
#     def spec(self):
#         return self.env.spec

#     @classmethod
#     def class_name(cls):
#         return cls.__name__

#     def step(self, action):
#         return self.env.step(action)

#     def reset(self, **kwargs):
#         return self.env.reset(**kwargs)

#     def render(self, mode='human', **kwargs):
#         return self.env.render(mode, **kwargs)

#     def close(self):
#         return self.env.close()

#     def seed(self, seed=None):
#         return self.env.seed(seed)

#     def compute_reward(self, achieved_goal, desired_goal, info):
#         return self.env.compute_reward(achieved_goal, desired_goal, info)

#     def __str__(self):
#         return '<{}{}>'.format(type(self).__name__, self.env)

#     def __repr__(self):
#         return str(self)

#     @property
#     def unwrapped(self):
#         return self.env.unwrapped


# class ObservationWrapper(Wrapper):
#     def reset(self, **kwargs):
#         observation = self.env.reset(**kwargs)
#         return self.observation(observation)

#     def step(self, action):
#         observation, reward, done, info = self.env.step(action)
#         return self.observation(observation), reward, done, info

#     def observation(self, observation):
#         raise NotImplementedError


# class RewardWrapper(Wrapper):
#     def reset(self, **kwargs):
#         return self.env.reset(**kwargs)

#     def step(self, action):
#         observation, reward, done, info = self.env.step(action)
#         return observation, self.reward(reward), done, info

#     def reward(self, reward):
#         raise NotImplementedError


# class ActionWrapper(Wrapper):
#     def reset(self, **kwargs):
#         return self.env.reset(**kwargs)

#     def step(self, action):
#         return self.env.step(self.action(action))

#     def action(self, action):
#         raise NotImplementedError

#     def reverse_action(self, action):
#         raise NotImplementedError
