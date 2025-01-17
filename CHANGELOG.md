# 0.6.2

Avoid overlapping when generating agents, players, and zombies, 

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

