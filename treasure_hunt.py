#-------------------------------------------------------------------------------
# Name:        treasure_hunt
# Purpose:     Simple grid based game about collecting gold & avoiding pirates
#
# Author:      Jordan Alexander Watt
#
# Release:    19-1-2016
# Version:     1.0
#
# Copyright:   (c) Jordan Watt 2015
#-------------------------------------------------------------------------------

from game_board import GameBoard
import tkinter as tk

class TreasureHunt(tk.Tk):
    """The game's top-level window. Parent of three in game menus each
    corresponding to a frame. Initializes all frames and switches between
    them using 'show_frame' method. All frames are persistent even when hidden.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Class variables for game window. frames holds each menu, game creates
        #object from game_board, reveal, unlock, and score used for in game.
        self.frames = {}
        self.Game = GameBoard()
        self.reveal = tk.IntVar()
        self.unlock = False
        self.score = {"CURRENT": {"RESULT": "", "GOLD": 0, "MOVES": 0},
                      "BEST": {"RESULT": "", "GOLD": 0, "MOVES": 0}}

        #top-level frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Dictionary of frames for use in 'show_frame'
        for i in (MainMenu, GameMenu, EndMenu):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    #Raises the called frame to the top
    def show_frame(self, menu):

        frame = self.frames[menu]
        if frame == self.frames[GameMenu]:
            frame.refresh()
        frame.widgets()
        frame.tkraise()

class MainMenu(tk.Frame):
    """Default starting frame. Widgets self-explanatory. In game main menu
    for settings and starting a new game.
    NOTE: Uncomment 'self.reveal_check' lines for debugging. See below.
    """

    def __init__(self, master, treasure_h):
        tk.Frame.__init__(self, master)
        self.reveal = tk.IntVar()
        self.treasure_h = treasure_h
        self.grid()

    #Creates interface widgets, descriptive names make them self-explanatory
    def widgets(self):

        self.play_game = tk.Button(self)
        self.play_game["text"] = "Play"
        self.play_game["command"] = self.play
        self.play_game.grid(row = 1, column = 1)

        self.quit_game = tk.Button(self)
        self.quit_game["text"] = "Quit"
        self.quit_game["command"] = quit_app
        self.quit_game.grid(row = 2, column = 1)

        self.grid_label = tk.Label(self)
        self.grid_label["text"] = "Grid:"
        self.grid_label.grid(row = 1, column = 2)

        self.grid_entry = tk.Entry(self)
        self.grid_entry["width"] = 4
        self.grid_entry.grid(row = 1, column = 3)
        self.grid_entry.insert(0, '8')

        self.chest_label = tk.Label(self)
        self.chest_label["text"] = "Chests:"
        self.chest_label.grid(row = 2, column = 2)

        self.chest_entry = tk.Entry(self)
        self.chest_entry["width"] = 4
        self.chest_entry.grid(row = 2, column = 3)
        self.chest_entry.insert(0, '10')

        self.pirate_label = tk.Label(self)
        self.pirate_label["text"] = "Pirates:"
        self.pirate_label.grid(row = 3, column = 2)

        self.pirate_entry = tk.Entry(self)
        self.pirate_entry["width"] = 4
        self.pirate_entry.grid(row = 3, column = 3)
        self.pirate_entry.insert(0, '5')

        #The following code reveals all chests/pirates on
        #the board when checked. Uncomment to enable for debugging
##        self.reveal_check = tk.Checkbutton(self)
##        self.reveal_check["text"] = "Reveal Board"
##        self.reveal_check["variable"] = self.treasure_h.reveal
##        self.reveal_check.grid(row = 4, column = 1)

        #Enables/Disables extra game options after beating the game
        if self.treasure_h.unlock:
            self.grid_entry["state"] = tk.NORMAL
            self.chest_entry["state"] = tk.NORMAL
            self.pirate_entry["state"] = tk.NORMAL
        else:
            self.grid_entry["state"] = tk.DISABLED
            self.chest_entry["state"] = tk.DISABLED
            self.pirate_entry["state"] = tk.DISABLED

    #Takes values input into the widgets and creates a new GameBoard object
    #before switching to the game-play frame
    def play(self):
        grid_size = int(self.grid_entry.get())
        chest_no = int(self.chest_entry.get())
        pirate_no = int(self.pirate_entry.get())
        self.treasure_h.Game = GameBoard(grid_size, pirate_no, chest_no)
        self.treasure_h.show_frame(GameMenu)


class GameMenu(tk.Frame):
    """Game-play screen providing graphical user interface for interacting with
    GameBoard object.
    """

    def __init__(self, master, treasure_h):
        tk.Frame.__init__(self, master)
        self.grid()
        self.treasure_h = treasure_h
        self.widgets()

    #Creates interface widgets, descriptive names make them self-explanatory
    def widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight = 1)
        top.columnconfigure(0, weight = 1)

        self.rowconfigure(0)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, pad = 15)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)

        self.canvas = tk.Canvas(self, borderwidth=2, highlightthickness=0,
                                width=75, height=75, background="bisque")
        self.canvas.grid(row = 1, column = 0, columnspan = 4, sticky = tk.NSEW)
        self.canvas.bind("<Configure>", self.redraw)

        self.menu_button = tk.Button(self)
        self.menu_button["text"] = "Main Menu"
        self.menu_button["command"] = lambda: self.treasure_h.show_frame(MainMenu)
        self.menu_button.grid(row = 0, column = 0, sticky = tk.W)

        self.quit_game = tk.Button(self)
        self.quit_game["text"] = "Quit"
        self.quit_game["command"] = quit_app
        self.quit_game.grid(row = 0, column = 3, sticky = tk.E)

        self.move_x_label = tk.Label(self)
        self.move_x_label["text"] = "Left/Right:"
        self.move_x_label.grid(row = 2, column = 0, sticky = tk.E)

        self.move_x_entry = tk.Spinbox(self)
        self.move_x_entry["width"] = 4
        self.move_x_entry["from_"] = -(self.treasure_h.Game.grid)
        self.move_x_entry["to"] = self.treasure_h.Game.grid
        self.move_x_entry.grid(row = 2, column = 1, sticky = tk.W)

        self.move_y_label = tk.Label(self)
        self.move_y_label["text"] = "Up/Down:"
        self.move_y_label.grid(row = 3, column = 0, sticky = tk.E)

        self.move_y_entry = tk.Spinbox(self)
        self.move_y_entry["width"] = 4
        self.move_y_entry["from_"] = -(self.treasure_h.Game.grid)
        self.move_y_entry["to"] = self.treasure_h.Game.grid
        self.move_y_entry.grid(row = 3, column = 1, sticky = tk.W)

        self.result_label = tk.Label(self)
        self.result_label["text"] = ""
        self.result_label.grid(row = 2, column = 2, sticky = tk.E)

        self.move_button = tk.Button(self)
        self.move_button["text"] = "GO!"
        self.move_button["command"] = self.move
        self.move_button.grid(row = 3, column = 2, sticky = tk.W)

        self.gold_label = tk.Label(self)
        self.gold_label["text"] = "Gold: 0"
        self.gold_label.grid(row = 2, column = 3)

        self.moves_label = tk.Label(self)
        self.moves_label["text"] = "Moves: 0"
        self.moves_label.grid(row = 3, column = 3)

    #Takes values from widgets and sends to GameBoard object. Simple logic
    #determines if any other actions are taken.
    def move(self):
        x = int(self.move_x_entry.get())
        y = int(self.move_y_entry.get())
        result = self.treasure_h.Game.move_player(x, y)
        player = str(self.treasure_h.Game.player_location)
        self.result_label["text"] = player + " " + result
        self.refresh()
        if (result == "WINNER" or result == "LOSER"):
            self.result_label["text"] = ""
            gold = self.treasure_h.Game.player_gold
            moves = self.treasure_h.Game.player_moves
            self.treasure_h.score["CURRENT"]["RESULT"] = result
            self.treasure_h.score["CURRENT"]["GOLD"] = gold
            self.treasure_h.score["CURRENT"]["MOVES"] = moves
            if (result == "WINNER" and gold >= self.treasure_h.score["BEST"]["GOLD"]):
                self.treasure_h.score["BEST"]["RESULT"] = result
                self.treasure_h.score["BEST"]["GOLD"] = gold
                self.treasure_h.score["BEST"]["MOVES"] = moves
            self.treasure_h.show_frame(EndMenu)

    #Configure bind to canvas sends event, refresh handling done without event
    #Can be optimized
    def redraw(self, event):
        self.refresh()

    #Re-draws canvas of squares with new changes every time the screen is
    #resized or a button is pressed. Also updates related labels
    def refresh(self):
        self.canvas.delete("square")
        grid_wpx = self.canvas.winfo_width()
        grid_hpx = self.canvas.winfo_height()
        grid_s = self.treasure_h.Game.grid
        tile_width = grid_wpx / grid_s
        tile_height = grid_hpx / grid_s
        player = self.treasure_h.Game.player_location
        chests = self.treasure_h.Game.chests_coords
        pirates = self.treasure_h.Game.pirates_coords

        #Creates squares column by column for every row reaching provided
        #grid size. Tkinter draws squares from top-left to bot-right hence the
        #logic used for x-y values
        for row in range(grid_s):
            for col in range(grid_s):
                x1 = (col * tile_width)
                y1 = (grid_hpx - (row + 1) * tile_height)
                x2 = x1 + tile_width
                y2 = (grid_hpx - row * tile_height)

                #Colors squares based on GameBoard values
                #NOTE: above range starts at 0, game coordinates begin at (1,1)
                #So values are adjusted accordingly.
                if (player[0], player[1]) == (col+1, row+1):
                    color = "green"
                elif (col+1, row+1) in pirates and self.treasure_h.reveal.get():
                    color = "red"
                elif (col+1, row+1) in chests and self.treasure_h.reveal.get():
                    color = "yellow"
                else:
                    color = "#a98d70"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill = color,
                                             outline="black", tags="square")

        #Updates labels with new info. Adjusts movement entries max/min values
        self.gold_label["text"] = "Gold: " + str(self.treasure_h.Game.player_gold)
        self.moves_label["text"] = "Moves: " + str(self.treasure_h.Game.player_moves)
        self.move_x_entry["from_"] = -(player[0] - 1)
        self.move_x_entry["to"] = grid_s - player[0]
        self.move_y_entry["from_"] = -(player[1] - 1)
        self.move_y_entry["to"] = grid_s - player[1]

class EndMenu(tk.Frame):
    """Post-game frame displaying results and records.
    Simple/self-exlanatory.
    """

    def __init__(self, master, treasure_h):
        tk.Frame.__init__(self, master)
        self.grid()
        self.treasure_h = treasure_h

    #Creates interface widgets, descriptive names make them self-explanatory
    def widgets(self):

        #After reaching this screen once, main menu settings will permenantly
        #be unlocked.
        self.treasure_h.unlock = True

        #Creates strings for display in following widgets
        current = ("CURRENT:\n\n" + self.treasure_h.score["CURRENT"]["RESULT"] +
                 "\ngold: " + str(self.treasure_h.score["CURRENT"]["GOLD"]) +
                 "\nmoves: " + str(self.treasure_h.score["CURRENT"]["MOVES"]))
        best = ("BEST:\n" +
                 "\ngold: " + str(self.treasure_h.score["BEST"]["GOLD"]) +
                 "\nmoves: " + str(self.treasure_h.score["BEST"]["MOVES"]))

        self.menu_button = tk.Button(self)
        self.menu_button["text"] = "Main Menu"
        self.menu_button["command"] = lambda: self.treasure_h.show_frame(MainMenu)
        self.menu_button.grid(row = 0, column = 0, sticky = tk.W)

        self.quit_game = tk.Button(self)
        self.quit_game["text"] = "Quit"
        self.quit_game["command"] = quit_app
        self.quit_game.grid(row = 0, column = 2, sticky = tk.E)

        self.current_label = tk.Label(self)
        self.current_label["text"] = current
        self.current_label.grid(row = 1, column = 1, pady = 15)

        self.best_label = tk.Label(self)
        self.best_label["text"] = best
        self.best_label.grid(row = 2, column = 1, pady = 15)

#Callable throughout program. Safely exits program.
def quit_app():
    App.destroy()

if __name__ == '__main__':

    #Create the window object using tkinter
    App = TreasureHunt()

    #Modify app window
    App.title("Treasure Hunt")
    App.geometry("450x475")

    #Keyboard shortcuts available on any frame
    App.bind_all("<Escape>", lambda event: quit_app())
    App.bind_all("<F1>", lambda event: App.show_frame(MainMenu))

    #Kick off the event loop
    App.mainloop()
