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

    CHEST_GOLD = 10
    STASH = 3
    WIN_GOLD = 100
    PIRATE_STEAL = 1.0

    def __init__(self, grid=4, pirates_num=5, chests_num=10):
            self.grid = grid
            self.pirates_num = pirates_num
            self.chests_num = chests_num
            self.pirates_coords = set()
            self.chests_coords = []
            self.chests = {}
            self.player_location = (1, 1)
            self.player_gold = 10
            self.player_moves = 0

            self.generate_pirates()
            self.generate_chests()

    def random_coordinates(self):
        while True:
            x_coord = randint(1, self.grid)
            y_coord = randint(1, self.grid)
            coordinate = (x_coord, y_coord)
            if (coordinate not in self.pirates_coords and
               coordinate not in self.chests_coords):
                break
        return coordinate

    def generate_pirates(self):
        for i in range(self.pirates_num):
            if(len(self.pirates_coords) + len(self.chests_coords) <
               self.grid * self.grid):
                coordinate = self.random_coordinates()
                self.pirates_coords.add(coordinate)

    def generate_chests(self):
        for i in range(self.chests_num):
            if(len(self.pirates_coords) + len(self.chests_coords) <
               self.grid * self.grid):
                coordinate = self.random_coordinates()
                self.chests[coordinate] = GameBoard.STASH
            self.chests_coords = [x for x in self.chests.keys()]

    def check_location(self):
        result = "EMPTY"
        if self.player_location in self.pirates_coords:
            self.player_gold -= int(self.player_gold * GameBoard.PIRATE_STEAL)
            result = "PIRATE"
        elif self.player_location in self.chests_coords:
            self.chests[self.player_location] -= 1
            if self.chests[self.player_location] == 0:
                del self.chests[self.player_location]
                self.chests_coords = [x for x in self.chests.keys()]
                self.pirates_coords.add(self.player_location)
                self.pirates_num += 1
                self.chests_num -= 1
            self.player_gold += GameBoard.CHEST_GOLD
            if self.chests_num == 0:
                if self.player_gold >= GameBoard.WIN_GOLD:
                    result = "WINNER"
                else:
                    result = "LOSER"
            else:
                result = "TREASURE"

        return result

    def move_player(self, x, y):
        result = "OUT OF BOUNDS"
        new_x = self.player_location[0] + x
        new_y = self.player_location[1] + y
        if (new_x > 0 and new_x <= self.grid and
           new_y > 0 and new_y <= self.grid):
            self.player_location = (new_x, new_y)
            self.player_moves += 1
            result = self.check_location()
        return result


test = GameBoard()
