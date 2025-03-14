# 0.10.0

Switching from gym to gymnasium.
Changing the environments to take the render mode rather than a rendering flag as a constructor argument.
In the Game class, the `enable_rendering` flag is used to determine whether to set up the pygame display surface.
The setting of display parameters when initializing rendering in the Game class has been improved.

# 0.9.1

Changing the namespace of the zombpyg gym environments.  The single-map version is v0 while a new version v1 has been added that supports world configurations.

# 0.9.0

We add support for world configurations which allow for multiple maps and game initial conditions.
The single-agent gym environment is still configured to use the single-map approach, using a class method
to call the new constructor with suitable parameters.

# 0.8.6

Adding checkpoints to the catacombs map and updating the resource spawns to be consistent with the checkpoints.
Removing reset method from agent builder.

# 0.8.5

Updating reward calculations to take friendly fire incidents avoided and checkpoints reached into account.
Adding support for configuring the reward calculator, enabling the friendly fire guard, and specifying the FPS
in the multiagent environment.
Adding checkpoints to the elevator map.
Disabling the friendly fire guard in the game play script.

# 0.8.4

Fixing the fighter collision logic to only include living fighters.

# 0.8.3

Adding checkpoints to provide a path to the safehouse for the agents.

# 0.8.2

Adding a reward for an agent reaching the objective when playing with the goal of reaching the safehouse.

# 0.8.1

Adding friendly fire guards to weapons.
Adding counters for the number of friendly fire incidents avoided to both the agent and existing players.
Adding support for using friendly fire guards in the agent and player builders.
Adding a flag for whether to use the friendly fire guards to the game and gym environment.

# 0.8.0

Adding support for configuring the reward calculator in the game and gym environment.

# 0.7.2

Adding addional maps.  In some of the maps, a large number of locations have been added with smaller quantities of resources.

# 0.7.1

Player statistics tracking for melee weapon attacks has been fixed.

# 0.7.0

Adding support for a game step with actions for all agents.  This is needed for supporting multi-agent environments.
Starting to adapt the multiagent environment to the PettingZoo parallel environment interface.

# 0.6.4

Adding support for a game step with actions for all agents. This is needed for supporting multi-agent environments.
The single-agent step now wraps the game step for all agents. The new interface represents a superset of the preceding version.

# 0.6.3

Adding support for spawn regions that are only used when initializing a world.

# 0.6.2

Avoid overlapping when spawning agents, players, and zombies, 

# 0.6.1

Adding a map making exit easy and with a lot of resources.

# 0.6.0

Rescaling the agent attributes (health, healing capacity, weapon ID, ammunition) in the gym observations to be
consistent with the sensor feedback and the gym observation space specification.

# 0.5.0

Adjusting the reset method in the gym implementation to return both an initial observation and an info dictionary.
This is to align with the gym specification.

# 0.4.0

Game class now manages the pygame rendering. The constructors for the game class and gym environment take a boolean argument indicating whether to render.

# 0.3.0

Associating weapons with agents at generation.  
Adding support for specifying agent weapons to the Game class and gym environment.

# 0.2.0

Adding a single-agent gym environment.

# 0.1.3

Adding support to the weapons factory for assigning a random weapon.

# 0.1.2

Adding the ability to pass an argument for the map id in the run script.

# 0.1.1

Running game in main thread.

# 0.1.0

Initial version.

