#!/usr/bin/env python
from os import path
from gymnasium.spaces import Box
from gymnasium.spaces.discrete import Discrete
from zombpyg.game import Game
from zombpyg.agent import AgentActions


# TODO: When we update from nixos-23.05, we will need to make sure this properly conforms with PettingZoo's ParallelEnv.
class MultiagentZombpygEnv(object):
    """The main class for multiagent play.
    """
    # See the supported modes in the render method
    metadata = {
        'render.modes': ['human']
    }

    # reward_range doesn't appear to be mentioned in the ParallelEnv API, but we keep it anyway
    reward_range = (-float('inf'), float('inf'))

    def __init__(self, 
        world_config={
            "tag": "SingleMap",
            "parameters": {
                "map_id": "demo",
                "w": 640, 
                "h": 480,
                "initial_zombies": 0, 
                "minimum_zombies": 0
            }
        },
        rules_id="survival",
        agent_ids = [0],
        agent_weapons="rifle",
        player_specs="",
        render_mode="human",
        fps=50,
        agent_reward_configuration={},
        friendly_fire_guard=False,
        verbose=False
    ):
        if render_mode is not None and (render_mode not in self.metadata.get('render.modes', [])):
            raise ValueError(f"In gymnasium environment, render_mode {render_mode} is not valid, must be one of {', '.join(self.metadata.get('render.modes', []))}")
        self.render_mode = render_mode
        enable_rendering = True if render_mode == "human" else False

        self.game = Game(
            world_config,
            rules_id=rules_id,
            agent_ids = agent_ids,
            agent_weapons = agent_weapons,
            player_specs=player_specs,
            enable_rendering=enable_rendering,
            fps=fps,
            agent_reward_configuration=agent_reward_configuration,
            friendly_fire_guard=friendly_fire_guard,
            verbose=verbose,
        )

        self.agents = agent_ids
        self.possible_agents = agent_ids
        # self.num_agents = len(self.agents) # Is this needed by PettingZoo?
        # self.max_num_agents = len(self.possible_agents) # Is this needed by PettingZoo?
        self.action_spaces = { agent_id: Discrete(AgentActions.get_actions_n()) for agent_id in self.possible_agents }
        self.observation_spaces = self._get_observation_spaces()

    # Using default implementations of 
    # observation_space(agent: AgentID) -> Space
    # and 
    # action_space(agent: AgentID) -> Space
    # NOTE: PettingZoo also specifies a method `state() -> ndarray` for returning a global view.
    #       This will be left unimplemented for now.

    # setting observation_space in the constructor with the help of the following
    def _get_observation_spaces(self):
        return { agent_id: Box(low=0.0, high=400.0, shape=self.game.get_feedback_size()) for agent_id in self.possible_agents }

    def get_observation(self):
        ret = {}
        for agent in self.game.world.agents:
            if agent.agent_id in self.agents: # This indicates the agent was alive before the step
                agentobs = agent.sensor_feedback()
                agentobs = agentobs.reshape((1, len(agentobs), 1))
                ret[agent.agent_id] = agentobs
        # return the observation and info
        return ret, {}

    def step(self, actions):
        """
        Receives a dictionary of actions keyed by the agent name.

        Returns the observation dictionary, reward dictionary, terminated dictionary, truncated dictionary and info dictionary,
        where each dictionary is keyed by the agent.

        Args:
            actions (dict): A dictionary of actions with agent IDs as keys

        Returns:
            observation (dict): observations of the current environment for each agent ID
            reward (dict[AgentID, float]) : amount of reward returned after previous action for each agent ID
            done (dict[AgentID, bool]): whether the episode has ended for each agent ID, in which case subsequent steps() calls might not return info for such an agent
            truncated (dict[AgentID, bool]): whether the episode has expired without a clear outcome for each agent ID, in which case further step() calls will return undefined results for that agent ID
            info (dict[AgentID, dict]): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning) for each agent ID
        """
        agent_actions = []
        for agent in self.game.world.agents:
            agent_actions.append(
                actions.get(
                    agent.agent_id,
                    AgentActions.get_no_action_id()
                )
            )
        
        rewardslist, observationslist, doneflag, truncatedflag = self.game.play_actions(agent_actions)
        # form returns
        # rewardslist and observationslist are for all agents, not just those that were active at the beginning of the step or are still alive
        allrewards = { agent_id: reward for agent_id, reward in zip(self.possible_agents, rewardslist) }
        rewards = { agent_id: allrewards[agent_id] for agent_id in self.agents }
        allobservations = { agent_id: observation for agent_id, observation in zip(self.possible_agents, observationslist) }
        observations = { agent_id: allobservations[agent_id] for agent_id in self.agents }
        done = { agent_id: doneflag for agent_id in self.agents }
        truncated = { agent_id: truncatedflag for agent_id in self.agents }
        info = {}

        # Update the active list of agents
        self.agents = [ agent.agent_id for agent in self.game.world.agents if agent.life > 0]

        return observations, rewards, done, truncated, info

    def reset(self, seed=None, options=None):
        """Resets the environment to an initial state and returns an initial
        observation.

        Returns:
            dictionary of observations (dict[AgentID, ObsType]): the initial observations
            dictionary of info (dict[AgentID, dict]): additional information for each agent
        """
        self.game.reset()
        self.agents = self.possible_agents
        return self.get_observation()

    def render(self):
        """Renders the environment.  Only 'human' is supported in this implementation.
        Args:
            mode (str): the mode to render with
        """
        if self.render_mode == 'human':
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

    def __str__(self):
        return '<{} instance>'.format(type(self).__name__)

    def __enter__(self):
        """Support with-statement for the environment. """
        return self

    def __exit__(self, *args):
        """Support with-statement for the environment. """
        self.close()
        # propagate exception
        return False

