#-------------------------------------------------------------------------------
# Name:        menus
# Purpose:     game GUI and interface options
#
# Author:      Jordan Alexander Watt
#
# Created:     01-12-2015
# Copyright:   (c) Jordan 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from game_board import GameBoard
import tkinter as tk

class TreasureHunt(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.Game = GameBoard()
        self.reveal = tk.IntVar()

        for i in (MainMenu, GameMenu, EndMenu):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, menu):

        frame = self.frames[menu]
        frame.refresh()
        frame.tkraise()

#Creates GUI
class MainMenu(tk.Frame):
    def __init__(self, master, treasure_h):
        tk.Frame.__init__(self, master)
        self.reveal = tk.IntVar()
        self.treasure_h = treasure_h
        self.grid()
        self.main_menu()

    #All immediately visable objects on interface
    def main_menu(self): # lambda: (character.toggle_gender(), self.refresh())

        #Button sends arguments to game_board and starts a new game
        self.play_game = tk.Button(self)
        self.play_game["text"] = "Play"
        self.play_game["command"] = self.play
        self.play_game.grid(row = 1, column = 1)

        #Button exits the program
        self.quit_game = tk.Button(self)
        self.quit_game["text"] = "Quit"
        self.quit_game["command"] = quit_app
        self.quit_game.grid(row = 2, column = 1)

        #Extra options unlocked after first playthrough
        #Label & Entry for the grid size
        self.grid_label = tk.Label(self)
        self.grid_label["text"] = "Grid:"
        self.grid_label.grid(row = 1, column = 2)

        self.grid_entry = tk.Entry(self)
        self.grid_entry["width"] = 4
        self.grid_entry.grid(row = 1, column = 3)
        self.grid_entry.insert(0, '8')
##        self.grid_entry["state"] = tk.DISABLED

        #Label & Entry for chest quantity
        self.chest_label = tk.Label(self)
        self.chest_label["text"] = "Chests:"
        self.chest_label.grid(row = 2, column = 2)

        self.chest_entry = tk.Entry(self)
        self.chest_entry["width"] = 4
        self.chest_entry.grid(row = 2, column = 3)
        self.chest_entry.insert(0, '10')
##        self.chest_entry["state"] = tk.DISABLED

        #Label & Entry for pirate quantity
        self.pirate_label = tk.Label(self)
        self.pirate_label["text"] = "Pirates:"
        self.pirate_label.grid(row = 3, column = 2)

        self.pirate_entry = tk.Entry(self)
        self.pirate_entry["width"] = 4
        self.pirate_entry.grid(row = 3, column = 3)
        self.pirate_entry.insert(0, '5')
##        self.pirate_entry["state"] = tk.DISABLED

        #The following code reveals all chests/pirates on
        #the board when checked. Uncomment to enable for debugging
        self.reveal_check = tk.Checkbutton(self)
        self.reveal_check["text"] = "Reveal Board"
        self.reveal_check["variable"] = self.treasure_h.reveal
        self.reveal_check.grid(row = 4, column = 1)

    def play(self):
        grid_size = int(self.grid_entry.get())
        chest_no = int(self.chest_entry.get())
        pirate_no = int(self.pirate_entry.get())
        print(grid_size)
        print(chest_no)
        print(pirate_no)
        self.treasure_h.Game = GameBoard(grid_size, pirate_no, chest_no)
        self.treasure_h.show_frame(GameMenu)

    def unlock(self):
        self.grid_entry["state"] = tk.NORMAL
        self.chest_entry["state"] = tk.NORMAL
        self.pirate_entry["state"] = tk.NORMAL

    def refresh(self):
        pass

class GameMenu(tk.Frame):
    def __init__(self, master, treasure_h):
        tk.Frame.__init__(self, master)

        self.treasure_h = treasure_h

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight = 1)
        top.columnconfigure(0, weight = 1)

        self.rowconfigure(0)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)

        #Label & Entry for pirate quantity
        self.result_label = tk.Label(self)
        self.result_label["text"] = ""
        self.result_label.grid(row = 0, column = 0)

        self.canvas = tk.Canvas(self, borderwidth=2, highlightthickness=0,
                                width=75, height=75, background="bisque")
        self.canvas.grid(row = 1, column = 0, columnspan = 4, sticky = tk.NSEW)
        self.canvas.bind("<Configure>", self.redraw)

        #Button sends arguments to game_board and starts a new game
        self.menu_button = tk.Button(self)
        self.menu_button["text"] = "Main Menu"
        self.menu_button["command"] = lambda: treasure_h.show_frame(MainMenu)
        self.menu_button.grid(row = 0, column = 2)

        #Button exits the program
        self.quit_game = tk.Button(self)
        self.quit_game["text"] = "Quit"
        self.quit_game["command"] = quit_app
        self.quit_game.grid(row = 0, column = 3)

        self.move_x_label = tk.Label(self)
        self.move_x_label["text"] = "Left/Right:"
        self.move_x_label.grid(row = 2, column = 0)

        self.move_x_entry = tk.Spinbox(self)
        self.move_x_entry["width"] = 4
        self.move_x_entry["from_"] = -(self.treasure_h.Game.grid)
        self.move_x_entry["to"] = self.treasure_h.Game.grid
        self.move_x_entry.grid(row = 2, column = 1)

        self.move_y_label = tk.Label(self)
        self.move_y_label["text"] = "Up/Down:"
        self.move_y_label.grid(row = 3, column = 0)

        self.move_y_entry = tk.Entry(self)
        self.move_y_entry["width"] = 4
        self.move_y_entry.grid(row = 3, column = 1)
        self.move_y_entry.insert(0, '0')

        self.move_button = tk.Button(self)
        self.move_button["text"] = "GO!"
        self.move_button["command"] = self.move
        self.move_button.grid(row = 2, column = 2)

        self.gold_label = tk.Label(self)
        self.gold_label["text"] = "Gold: 0"
        self.gold_label.grid(row = 2, column = 3)

        self.moves_label = tk.Label(self)
        self.moves_label["text"] = "Moves: 0"
        self.moves_label.grid(row = 3, column = 3)

    def move(self):
        x = int(self.move_x_entry.get())
        y = int(self.move_y_entry.get())
        result = self.treasure_h.Game.move_player(x, y)
        print (result)
        self.refresh()

    def redraw(self, event):
        self.refresh()

    def refresh(self):
        self.gold_label["text"] = "Gold: " + str(self.treasure_h.Game.player_gold)
        self.moves_label["text"] = "Moves: " + str(self.treasure_h.Game.player_moves)
        self.move_x_entry["from_"] = -(self.treasure_h.Game.grid)
        self.move_x_entry["to"] = self.treasure_h.Game.grid
        self.canvas.delete("square")
        grid_wpx = self.canvas.winfo_width()
        grid_hpx = self.canvas.winfo_height()
        grid_s = self.treasure_h.Game.grid
        tile_width = grid_wpx / grid_s
        tile_height = grid_hpx / grid_s
        player = self.treasure_h.Game.player_location
        chests = self.treasure_h.Game.chests_coords
        pirates = self.treasure_h.Game.pirates_coords
        for row in range(grid_s):
            for col in range(grid_s):
                x1 = (col * tile_width)
                y1 = (grid_hpx - (row + 1) * tile_height)
                x2 = x1 + tile_width
                y2 = (grid_hpx - row * tile_height)
                if (player[0], player[1]) == (col+1, row+1):
                    color = "green"
                elif (col+1, row+1) in pirates and self.treasure_h.reveal.get():
                    color = "red"
                elif (col+1, row+1) in chests and self.treasure_h.reveal.get():
                    color = "yellow"
                else:
                    color = "blue"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill = color, outline="black", tags="square")

class EndMenu(tk.Frame):
    def __init__(self, master, treasure_h):
        tk.Frame.__init__(self, master)

    def refresh(self):
        pass


    # ----- refresh -----

def quit_app():
    App.destroy()

if __name__ == '__main__':

    #Create the window object using tkinter
    App = TreasureHunt()

    #Modify app window
    App.title("Treasure Hunt")
    App.geometry("575x425")

    #Kick off the event loop
    App.mainloop()