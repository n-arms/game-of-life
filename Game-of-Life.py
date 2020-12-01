from tkinter import *
from time import sleep
import threading

class Tile(Canvas):
    '''a class to represent one square in a game of life'''
    
    def __init__(self, master):
        '''Tile(master, x, y) -> Tile
        create a new Tile with left handed coordinates
        x and y'''
        # canvas purely to show state using the background
        Canvas.__init__(self, master, width=10, height=10, bg='white', bd=0)
        self.state = False # a boolean to represent whether a tile is alive
        self.return_state = False # the state that the tile will return
        self.re_bind()
        
    def get_state(self):
        '''Tile.get_state()
        returns the Tile.state attribute'''
        return self.return_state

    def change_state(self, tiles):
        '''Tile.change_state(tiles)
        changes the tile's current state
        tiles should be a list of the surrounding tiles'''
        # calculate the number of neighbouring tiles are alive
        neighbour_count = sum([1 for i in tiles if i.get_state()])
        if self.state: #remove yourself from the count
            neighbour_count -= 1
        # triggers on the two death conditions of overcrowding or underpop
        if neighbour_count <= 1 or neighbour_count >= 4:
            self.state = False
        # triggers on the reproduction condition
        elif neighbour_count == 3:
            self.state = True

        # all other states result in no change

    def set_state(self, event):
        '''Tile.set_state(event)
        handler method for game initiation'''
        self.state = self.state ^ True # toggles state
        self.update_display()
            
    def update_display(self):
        '''Tile.update_disply()
        used to update every tile at once'''
        self.return_state = self.state
        if self.state:
            self['bg'] = 'black'
        else:
            self['bg'] = 'white'
    def un_bind(self):
        '''Tile.unbind()
        unbinds the tile to optimize lag'''
        self.unbind('<Button-1>')
    def re_bind(self):
        '''Tile.rebind()
        binds the tile'''
        self.bind('<Button-1>', self.set_state)
        

class GameOfLife(Frame):
    '''frame for the game of life'''
    def __init__(self, master, width, height, time):
        '''GameOfLife(master, name) -> GameOfLife
        create a new game of life
        width and height are both measured in tiles'''
        # set up Frame object
        Frame.__init__(self, master)
        self.grid() 
        self.tiles = {} # a dict to hold each tile and it's position
        for i in range(width):
            for j in range(height):
                self.tiles[(i, j)] = Tile(master)
                self.tiles[(i, j)].grid(column = i, row = j+1)
        self.width = width
        self.height = height
        self.start_button = Button(self, text='start', command=self.start)
        self.start_button.grid(row=1, column=1, columnspan=2)
        self.time = time
        self.stop()

        
    def update_tile(self, x, y):
        '''GameOfLife.update_tile(x, y)
        creates a list to pass to the Tile.change_state method'''
        neighbour_tiles = []
        for i in range(x-1, x+2): 
            for j in range(y-1, y+2):
                if self.width>i and i>-1 and self.height>j and j>-1:
                    neighbour_tiles.append(self.tiles[(i, j)])
        self.tiles[(x, y)].change_state(neighbour_tiles)

    def advance_time(self):
        '''GameOfLife.advance_time()
        changes time by 1 step by updating each tile'''
        if not self.running:
            return
        for i in self.tiles:
            self.tiles[i].update_display()
        sleep(self.time)
        for i in range(self.width):
            for j in range(self.height):
                self.update_tile(i, j)
        self.advance_time() #infinite recursion
        
    def start(self):
        self.start_button['command'] = self.stop
        self.running = True
        thread1 = threading.Thread(target=self.advance_time)
        thread1.start()
        for i in self.tiles:
            self.tiles[i].un_bind()
            
    def stop(self):
        self.running = False
        self.start_button['command'] = self.start
        for i in self.tiles:
            self.tiles[i].re_bind()
    

root = Tk()
g = GameOfLife(root, 25, 25, 0.1)
root.mainloop()
