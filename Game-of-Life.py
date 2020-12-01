from tkinter import *

class Tile(Canvas):
    '''a class to represent one square in a game of life'''
    
    def __init__(self, master):
        '''Tile(master, x, y) -> Tile
        create a new Tile with left handed coordinates
        x and y'''
        # canvas purely to show state using the background
        Canvas.__init__(self, master, width=10, height=10, bg='white', bd=0)
        self.state = False # a boolean to represent whether a tile is alive
        self.settable = True # if true, the tile can be toggled by clicking
        
    def get_state(self):
        '''Tile.get_state()
        returns the Tile.state attribute'''
        return self.state

    def change_state(self, tiles):
        '''Tile.change_state(tiles)
        changes the tile's current state
        tiles should be a list of the surrounding tiles'''
        # calculate the number of neighbouring tiles are alive
        neighbour_count = sum([1 for i in tiles if i.get_state()])
        # triggers on the two death conditions of overcrowding or underpop
        if neighbour_count == 1 or neighbour_count >= 4:
            self.state = False
        # triggers on the reproduction condition
        elif neightbour_count == 3 and not self.state:
            self.state = True

        # all other states result in no change

    def set_state(self, event):
        '''Tile.set_state(event)
        handler method for game initiation'''
        if self.settable:
            self.state = self.state ^ True # toggles state
            self.update_display()
            
    def update_display(self):
        '''Tile.update_disply()
        used to update every tile at once'''
        if self.state:
            self['bg'] = 'black'
        else:
            self['bg'] = 'white'

class GameOfLife(Frame):
    '''frame for the game of life'''
    def __init__(self, master, width, height):
        '''GameOfLife(master, name) -> GameOfLife
        create a new game of life
        width and height are both measured in tiles'''
        # set up Frame object
        Frame.__init__(self, master)
        self.grid()
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                self.tiles[(i, j)] = Tile(master)
                self.tiles[(i, j)].grid()
        
        

    
        
        
        
