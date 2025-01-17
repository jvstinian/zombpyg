#!/usr/bin/env python
# coding: utf-8
from os import path
from gym.core import Env
from gym.spaces import Text, Box, Dict, Sequence
from gym.spaces.discrete import Discrete
from zombsole.gym.observation import SurroundingsChannelsObservation
from zombsole.gym.reward import AgentRewards
from zombsole.game import Game, Map
from zombsole.renderer import NoRender
import time
import numpy as np


# TODO: When we update from nixos-23.05, we will need to make sure this properly conforms with PettingZoo's ParallelEnv.
class MultiagentZombsoleEnv(object):
    """The main Gym class for multiagent play.
    """
    # See the supported modes in the render method
    metadata = {
        'render.modes': ['human']
    }
    
    # Set these in ALL subclasses
    reward_range = (-float('inf'), float('inf')) # NOTE: For gym, is this needed for pettingzoo?
    # action_space = Sequence(
    #     Dict({
    #         "agent_id": Discrete(64),
    #         "action": Discrete(AgentActions.get_actions_n())
    #     })
    # )

    def __init__(self, 
        map_id="demo",
        rules_id="survival",
        initial_zombies=0,
        minimum_zombies=0,
        # agent_id = 0,
        agent_ids = [0],
        agent_weapons="rifle",
        player_specs="",
        verbose=False
    ):
        # We pass None for the DISPLAYSURF, and configure the rendering below.
        self.game = Game(
            640, 480, None,
            map_id=map_id,
            rules_id=rules_id,
            initial_zombies=initial_zombies,
            minimum_zombies=minimum_zombies,
            agent_ids = agent_ids,
            agent_weapons = agent_weapons,
            player_specs=player_specs,
            verbose=verbose,
        )

        self.window = None
        self.__initialize_renderer__()

        self.agents = agent_ids
        self.possible_agents = agent_ids
        # self.num_agents = len(self.agents) # Is this needed by PettingZoo?
        # self.max_num_agents = len(self.possible_agents) # Is this needed by PettingZoo?
        self.action_spaces = { agend_id: Discrete(AgentActions.get_actions_n()) for agent_id in self.possible_agents }
        self.observation_spaces = self._get_observation_spaces()

    # Using default implementations of 
    # observation_space(agent: AgentID) -> Space
    # and 
    # action_space(agent: AgentID) -> Space
    # NOTE: PettingZoo also specifies a method `state() -> ndarray` for returning a global view.
    #       This will be left unimplemented for now.

    # setting observation_space in the constructor with the help of the following
    def _get_observation_spaces(self):
        return { agend_id: Box(low=0.0, high=400.0, shape=self.game.get_feedback_size()) for agent_id in self.possible_agents }
        # return Sequence(
        #     Dict({
        #         "agent_id": Discrete(64),
        #         "observation": Box(low=0.0, high=400.0, shape=self.game.get_feedback_size())
        #     })
        # )

    def get_observation(self):
        ret = {}
        for agent in self.game.world.agents:
            if agent.agent_id in self.agents: # This indicates the agent was alive before the step
                agentobs = agent.sensor_feedback()
                agentobs = agentobs.reshape((1, len(agentobs), 1))
                ret[agent.agent_id] = agent.sensor_feedback().reshape((1, len(feedbacks), 1))
        return ret

    # Taken from zombpyg single-agent gym.  Is this needed here?
    # def get_frame_size(self):
    #     return self.game.get_feedback_size()

    # def _process_action(self, action):
    #     return {
    #         v["agent_id"]: v["action"] for v in action
    #     }

    def step(self, action):
        """
        Receives a dictionary of actions keyed by the agent name.

        Returns the observation dictionary, reward dictionary, terminated dictionary, truncated dictionary and info dictionary,
        where each dictionary is keyed by the agent.

        Args:
            actions (dict): A dictionary of actions with agent IDs as keys

        Returns:
            observation (dict): observations of the current environment for each agent ID
            reward (dict[AgentID, float]) : amount of reward returned after previous action for each agent ID
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            truncated (bool): whether the episode has expired without a clear outcome, in which case further step() calls will return undefined results
            info (dict of dicts): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning) for each agent ID
        """
        agent_actions = []
        for agent in self.game.world.agents:
            agent_actions.append(
                actions.get(
                    agent.agent_id,
                    AgentActions,get_no_action_id()
                )
            )
        # TODO: The following Game method supports only a single agent action
        reward, observation, done, truncated = self.game.play_action(agent_actions)
        info = {}

        # form returns
        # for self.players specify done and truncated
        # empyt imfo for all players
        # make sure observations are properly formatted

        # filter self.agents to only those that are still living

        return observation, reward, done, truncated, info

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
        return self.get_observation()

    def render(self, mode='human'):
        """Renders the environment.  Only 'human' is supported in this implementation.
        Args:
            mode (str): the mode to render with
        """
        if mode == 'human':
            if self.window is not None:
                self.game.draw()
            return None
        else:
            raise ValueError("mode={} is not supported".format(mode))

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    # def seed(self, seed=None):
    #     """Sets the seed for this env's random number generator(s).

    #     Note:
    #         Some environments use multiple pseudorandom number generators.
    #         We want to capture all such seeds used in order to ensure that
    #         there aren't accidental correlations between multiple generators.

    #     Returns:
    #         list<bigint>: Returns the list of seeds used in this env's random
    #           number generators. The first value in the list should be the
    #           "main" seed, or the value which a reproducer should pass to
    #           'seed'. Often, the main seed equals the provided 'seed', but
    #           this won't be true if seed=None, for example.
    #     """
    #     # NOTE: Not currently capturing the seed information used in zombsole
    #     return

    # @property
    # def unwrapped(self):
    #     """Completely unwrap this env.

    #     Returns:
    #         gym.Env: The base non-wrapped gym.Env instance
    #     """
    #     return self

    def __str__(self):
        # if self.spec is None:
        #     return '<{} instance>'.format(type(self).__name__)
        # else:
        #     return '<{}<{}>>'.format(type(self).__name__, self.spec.id)
        return '<{} instance>'.format(type(self).__name__)

    def __enter__(self):
        """Support with-statement for the environment. """
        return self

    def __exit__(self, *args):
        """Support with-statement for the environment. """
        self.close()
        # propagate exception
        return False

