
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

This game was inspired by both the console game (`zombsole`)[https://github.com/fisadev/zombsole], 
as well as the author's extensions of this game (`zombsole-lib`)[https://github.com/jvstinian/zombsole], 
and the pellet-eating robot in the (`demo`)[https://github.com/PacktPublishing/Python-Reinforcement-Learning-Projects/tree/master/Chapter03/demo] game.  


Getting started
===============

The game does come with packaging for installing from the code repository, but 
is not packaged for PyPi at this time.  

```
git clone https://github.com/jvstinian/zombpyg.git
sudo pip install -e zombpyg
```

To play an example in single-player mode, the following can be run: 
```
./zombpyg extermination terminator:axe:1,terminator:gun:1 -n 30 
```

The command-line options of the `zombpyg` script should be easy to understand, and can be 
found by running `zombpyg --help`.  

Create your own players
=======================

TBD

Creating maps
=============

TBD

