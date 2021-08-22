# snake_game

To play the game on arcade mode on your win10-64 without having to install python:
  1) Download the folder dist. 
  2) Find and run SnakeGame.exe

Keep in mind:
  1) The main file to run is `SnakeGame.py`. 
  2) `Init.py` contains some variables and functions that are used by the whole project.
  3) `Level.py` and `Snake.py` contain the implementations of the named classes.
  4) Make sure all the files are exported to the same directory.
  5) To switch to and from arcade mode (only possible if you're using the source code):
      - At the end of SnakeGame.py toggle between `arcade_mode_on == True` and `== False`
  6) On arcade mode:
      - Walls are created randomly. 
      - The number of walls increases each time you level up. (So beware of the impossible configurations as mentioned in the issues!) 
  7) On level mode (== not arcade mode):
      - There are two built-in levels,
      - Adding new ones is possible via `SnakeGame.initialize_levels()`. 
  8) It's a game, keep it fun.
