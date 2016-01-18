# ------------------------------------------------------------------------------
# Name:        game_board
# Purpose:     Game grid, objects and info to be displayed in menus
#
# Author:      Jordan Alexander Watt
#
# Created:     01-12-2015
# Copyright:   (c) Jordan 2015
# Licence:     <your licence>
# ------------------------------------------------------------------------------

from random import randint


class GameBoard(object):
    """Object containing all of the game instances information. To be called
    from treasure_hunt.py when starting a game and sends information to
    menus.py for display.
    """

    # GameBoard constants. Permenantly alters parameters across all new games.
    # Change these to adjust game difficulty and length.
    CHEST_GOLD = 10  # Gold recieved each time a chest is accessed
    STASH = 3  # Number of times a chest can be opened.
    WIN_GOLD = 100  # Gold necessary to win after all chests opened
    PIRATE_STEAL = 1.0  # Gold stolen by pirates in percent (ie 1.0 = 100%)

    def __init__(self, grid=8, pirates_num=5, chests_num=10):
        """Initializes game with chests & pirates based on the arguments
        provided.

        Args:
            grid: Game's square grid size. Default 8 x 8
            pirates_num: Number of pirate squares. Default 5
            chests_num: Number of chest squares. Default 10

        Other instance variables:
            pirates_coords: Set of (x, y) coordinates of every pirate square
            chests_coords: List of (x, y) coordinates of every chest square
            chests: Dictionary of every chest. Each chest is organized as
                    KEY: (x, y) coordinates
                    VALUE: Number of times chest can be accessed. Initial STASH
            player_location: Current (x, y) coordinates of the player
            player_gold: Gold player has accumulated
            player_moves: Total number of moves by the player
        """

        self.grid = grid
        self.pirates_num = pirates_num
        self.chests_num = chests_num
        self.pirates_coords = set()
        self.chests_coords = []
        self.chests = {}
        self.player_location = (1, 1)
        self.player_gold = 0
        self.player_moves = 0

        # Randomly place chests and pirates throughout the grid
        self.generate_pirates()
        self.generate_chests()

    # Generate an unused coordinate
    def random_coordinates(self):
        while True:
            x_coord = randint(1, self.grid)
            y_coord = randint(1, self.grid)
            coordinate = (x_coord, y_coord)
            if (coordinate not in self.pirates_coords and
               coordinate not in self.chests_coords):
                break
        return coordinate

    # Creates starting pirate locations
    def generate_pirates(self):
        for i in range(self.pirates_num):

            # Prevents making more pirates than locations available
            if(len(self.pirates_coords) + len(self.chests_coords) <
               self.grid * self.grid):
                coordinate = self.random_coordinates()
                self.pirates_coords.add(coordinate)

    # Creates starting chest locations
    def generate_chests(self):
        for i in range(self.chests_num):

            # Prevents making more chests than locations available
            if(len(self.pirates_coords) + len(self.chests_coords) <
               self.grid * self.grid):
                coordinate = self.random_coordinates()

                # Since coordinates are unique, can be used as KEYS
                self.chests[coordinate] = GameBoard.STASH
            self.chests_coords = [x for x in self.chests.keys()]

    def check_location(self):
        """Checks the player's coordinates against pirates and chests and
        triggers appropriate event.

        Returns a string depicting the results of checking the location
        """

        result = "EMPTY"
        if self.player_location in self.pirates_coords:
            self.player_gold -= int(self.player_gold * GameBoard.PIRATE_STEAL)
            result = "PIRATE"
        elif self.player_location in self.chests_coords:

            # Reduces the number of times chest can be opened
            self.chests[self.player_location] -= 1

            # If the chest cannot be opened any more, remove it and add pirate
            if self.chests[self.player_location] == 0:
                del self.chests[self.player_location]
                self.chests_coords = [x for x in self.chests.keys()]
                self.pirates_coords.add(self.player_location)
                self.pirates_num += 1
                self.chests_num -= 1

            self.player_gold += GameBoard.CHEST_GOLD

            # If no more chests, declare if player won or lost
            if self.chests_num == 0:
                if self.player_gold >= GameBoard.WIN_GOLD:
                    result = "WINNER"
                else:
                    result = "LOSER"

            else:
                result = "TREASURE"

        return result

    def move_player(self, x, y):
        """Changes player_location to reflect movement input by the player.
        Checks to make sure the movement is within boundaries of the grid.

        Args:
            x: Horizontal squares to move in integers
            y: Vertical squares to move in integers

        Returns the result of check_location in a string reflecting the
        events within that square.
        """
        result = "OUT OF BOUNDS"
        new_x = self.player_location[0] + x
        new_y = self.player_location[1] + y
        if (new_x > 0 and new_x <= self.grid and
           new_y > 0 and new_y <= self.grid):
            self.player_location = (new_x, new_y)
            self.player_moves += 1
            result = self.check_location()
        return result
