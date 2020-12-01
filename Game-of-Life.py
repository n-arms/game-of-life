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
        

        
        
