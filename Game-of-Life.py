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
        self.state = False # a boolean to represent whether a tile is alive
        self.return_state = False # the state that the tile will return
        
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

    def set_state(self):
        '''Tile.set_state(event)
        handler method for game initiation'''
        self.state = self.state ^ True # toggles state
    def update_tile(self):
        '''Tile.update_tile()
        ses the return staet to the state, and returns the state'''
        self.return_state = self.state
        return self.state
    
class TileContainer(Canvas):
    '''a canvas to display and get inputs for the tile class'''
    def __init__(self, master, width, height, tile_size, time):
        self.tile_size = tile_size
        self.width = width
        self.height = height
        Canvas.__init__(self, master, width=self.width*self.tile_size, \
                        height=self.height*self.tile_size)
        self.running = False
        self.tiles = {} # a dict to hold each tile and it's position
        for i in range(width):
            for j in range(height):
                self.tiles[(i, j)] = Tile(master)
        self.bind('<Button-1>', self.click)
        self.time = time

    def update_tile(self, x, y):
        '''TileContainer.update_tile(x, y)
        creates a list to pass to the Tile.change_state method'''
        neighbour_tiles = []
        for i in range(x-1, x+2): 
            for j in range(y-1, y+2):
                if self.width>i and i>-1 and self.height>j and j>-1:
                    neighbour_tiles.append(self.tiles[(i, j)])
        self.tiles[(x, y)].change_state(neighbour_tiles)
        

    def advance_time(self):
        '''TileContainer.advance_time()
        changes time by 1 step by updating each tile'''
        if not self.running:
            return
        self.update_display()
        sleep(self.time)
        for i in range(self.width):
            for j in range(self.height):
                self.update_tile(i, j)
        self.advance_time() #infinite recursion
        
    def click(self, event):
        '''a handler method for clicking the canvas'''
        self.tiles[(event.x//self.tile_size, event.y//self.tile_size)].set_state()
        self.update_display()

    def update_display(self):
        '''a method called to update all of the tiles'''
        self.delete('all')
        for i in self.tiles:
            self.tiles[i].update_tile()
            if self.tiles[i].get_state():
                self.create_rectangle(i[0]*self.tile_size, i[1]*self.tile_size, \
                                      (i[0]+1)*self.tile_size, \
                                 (i[1]+1)*self.tile_size, fill='black')
    def set_running(self, boolean):
        '''TileContainer.set_running()
        changes whether or not the game of life is running'''
        self.running = boolean
                

class GameOfLife(Frame):
    '''frame for the game of life'''
    def __init__(self, master, width, height, time, tile_size):
        '''GameOfLife(master, name) -> GameOfLife
        create a new game of life
        width and height are both measured in tiles'''
        # set up Frame object
        Frame.__init__(self, master)
        self.grid() 
        self.start_button = Button(self, text='start', command=self.start)
        self.start_button.grid(row=1, column=1, columnspan=2)
        self.container = TileContainer(self, width, height, tile_size, time)
        self.container.grid(row=2, column=2)
        self.stop()
        
    def start(self):
        self.start_button['command'] = self.stop
        self.start_button['text'] = 'STOP'
        self.container.set_running(True)
        thread1 = threading.Thread(target=self.container.advance_time)
        thread1.start()

            
    def stop(self):
        self.container.set_running(False)
        self.start_button['command'] = self.start
        self.start_button['text'] = 'START'

root = Tk()
g = GameOfLife(root, 80, 80, 0.1, 10)
root.mainloop()
