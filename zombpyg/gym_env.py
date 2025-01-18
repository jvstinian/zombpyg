#!/usr/bin/env python
from gymnasium.spaces.discrete import Discrete
from gymnasium.spaces.box import Box
from gymnasium.envs.registration import register
import pygame
from zombpyg.game import Game
from zombpyg.agent import AgentActions


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
    # See the supported modes in the render method
    metadata = {'render.modes': ['human']}

    # Set these in ALL subclasses
    reward_range = (-float('inf'), float('inf'))
    action_space = Discrete(AgentActions.get_actions_n())

    # observation_space = None

    def __init__(
        self,
        map_id="demo",
        rules_id="survival",
        initial_zombies=0, minimum_zombies=0,
        # agent_id = 0,
        agent_weapon="rifle",
        player_specs="",
        enable_rendering=True,
        verbose=False
    ):
        # We pass None for the DISPLAYSURF, and configure the rendering below.
        self.game = Game(
            640, 480,
            map_id=map_id,
            rules_id=rules_id,
            initial_zombies=initial_zombies,
            minimum_zombies=minimum_zombies,
            agent_ids = [0],
            agent_weapons = [agent_weapon],
            player_specs=player_specs,
            enable_rendering=enable_rendering,
            verbose=verbose,
        )

        self.observation_space = Box(low=0.0, high=400.0, shape=self.game.get_feedback_size())

    def get_observation(self):
        return self.game.get_current_feedback()
    
    def get_frame_size(self):
        return self.game.get_feedback_size()

    def step(self, action_id):
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
        reward, observation, done, truncated = self.game.play_action(action_id)
        info = {}
            
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
        return self.get_observation(), {}

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
            self.game.draw()
            return None
        else:
            raise ValueError("mode={} is not supported".format(mode))

    def close(self):
        """Override close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        self.game.close()

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

# TODO: Will keep this for now, but should we register here?
register(
    id='zombpyg/Zombpyg-v0', 
    entry_point='zombpyg.gym_env:ZombpygGymEnv', 
    max_episode_steps=300*50,
    kwargs={
    }
)

