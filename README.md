
Zombpyg
=======

Zombpyg is a multi-player, first-person shooter game in which players cooperate to 
fight and survive in a world beset by zombies.  

The game and underlying package offer the player or developer the ability to 

* play in single-player mode,
* program simple bots for automated play, or 
* train agents using more complex models.  

There are four different game objectives:

* *Extermination*: you must kill all zombies, and at least 1 player must survive.
* *Evacuation*: all living players must get together at any place to be evacuated,
  and at least half of the initial team must survive.
* *Safe House*: all players must travel and get inside a safe house. At least 1 player 
  must reach it, but to win, all the living players must be  inside.
* *Survival*: There is no escape.  

This game was inspired by both the console programming game [`zombsole`](https://github.com/fisadev/zombsole), 
as well as the author's extensions of this game [`zombsole-lib`](https://github.com/jvstinian/zombsole), 
and the pellet-eating robot in the [`demo`](https://github.com/PacktPublishing/Python-Reinforcement-Learning-Projects/tree/master/Chapter03/demo) game.  


Installation
============

The game does come with packaging for installing from the code repository, but 
is not packaged for PyPi at this time.  

If you do not plan to modify the game code, then the package 
can be installed from the repo using 
```
pip install git+https://github.com/jvstinian/zombpyg
```

If you plan to create your own bots or edit the code for the game, 
the best approach for installing is to clone the repo 
and install with the editable flag:  
```
git clone https://github.com/jvstinian/zombpyg.git
cd zombpyg
sudo pip install -e zombpyg
```

Single-player Mode
==================

To play an example in single-player mode, the following can be run: 
```
zombpyg -r extermination --players terminator:axe:1,terminator:gun:1 -n 10
```

| Action | Key |
| ------ | --- |
| Move forward | w |
| Move right | d |
| Move backward | s |
| Move left | a |
| Rotate left | left arrow |
| Rotate right | right arrow |
| Use weapon | space |
| Heal self | h |
| Heal player ahead | g |

The command-line options of the `zombpyg` script should be easy to understand, and can be 
found by running `zombpyg --help`.  


Create your own players
=======================

We will only provide an overview for adding new player bots here.  
To add a new bot, the recommended approach would be to 
* make a copy of the file for an existing player in the directory `zombpyg/players/`, 
* edit the method `next_step` as desired, making sure to call `self.play_action(action)` at 
  the end of the method, and 
* add logic for the new player to the method `create_player` for the class `PlayerBuilder` in 
  the file `zombpyg/players/builder.py`.  

The bot should then be available to use with the "--players" flag to the `zombpyg` script.  
When specifying the player type, make sure to use the player type specified in the `create_player` 
waterfall logic rather than the class name (e.g., "terminator" rather than "Terminator").   

Creating maps
=============

TBD

