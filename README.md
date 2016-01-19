TREASURE HUNT
======================

By Jordan Alexander Watt  

Developed by request.  
Simple grid based game about collecting gold and avoiding pirates.
Move around the grid to discover hidden treasure. Encountering
a pirate will cause you to lose all of your gold.


What's Included
---------------

Treasure Hunt
* game_board.py
* treasure_hunt.py
* README.md


Usage
-----

#####To Play:
Run `treasure_hunt.py`.  

**Note:**
Python necessary to run `.py` files. Programs written using Python 3.

#####To Modify:
`treasure_hunt.py` is the menus and GUI displayed during gameplay. Written
using tkinter. loads game_board class and runs the game. This can
easily be modified to enhance the basic interface provided or 
replaced altogether. Can modify to run multiple game_board instances
or enable pausing/saving/recording games. 
For debugging: Search and uncomment reveal_check to make all items 
in game visable.

`game_board.py` can be modified to alter each game instance. 
adjust values such as gold recieved from chests/stolen from pirates 
here. This module is the actual game itself and can be used without
the included GUI by calling the methods using the comments for
direction.


Gameplay
--------

```
Select Play and you will be shown a grid (default 8x8) with a green 
highlighted square in the bottom left (1,1). Adjust the "Right/Left"
option to state how many squares you intend to move (positive values
for moving right, negative values for moving left). Same principle
for "Up/Down" movement. Note: This does not take you to the coordinates
but moves you that number of squares. When you have recorded how far
you would like to move press "GO!" to perform the action. Results
will be displayed increasing gold, moves, and ending the
game if there are no more treasure chests. From the gameover screen
you may return to the menu with new options unlocked or quit the 
program.

```


Bug Reports
-----------

* No currently known bugs.

Please report any bugs to JordanAlexWatt@hotmail.com


Versioning
----------

Treasure Hunt 1.0 - 19-01-2016
* game_board.py
* treasure_hunt.py



Credits
-------

Treasure Hunt written by Jordan Alexander Watt (JAW)
 - JordanAlexWatt@hotmail.com  


***

*Last edited January 19 2016*