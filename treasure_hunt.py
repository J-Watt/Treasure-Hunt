#-------------------------------------------------------------------------------
# Name:        treasure_hunt
# Purpose:     Simple grid based game about collecting gold & avoiding pirates
#
# Author:      Jordan Alexander Watt
#
# Created:     01-12-2015
# Copyright:   (c) Jordan 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import game_board
import menus
from tkinter import *

def testing():
    print("testing")

if __name__ == '__main__':
    Game = GameBoard()

    #Create the window object using tkinter
    App = Tk()

    #Modify app window
    App.title("Treasure Hunt")
    App.geometry("575x425")

    #connects window class to app, adds all objects on gui to root window
    Application = Window(App)

    #Kick off the event loop
    App.mainloop()
