from tkinter import *
from time import sleep
import threading

class LifeBoard(Canvas):
    def __init__(self, master, size, buffer):
        '''LifeBoard(size, buffer) -> new LifeBoard
        where size is both the width and height of the board
        and buffer is the distance out from the board that tiles are tracked'''
        Canvas.__init__(self, master, width=size*10, height=size*10)
        self.size = size
        self.buffer = buffer
        self.current_tiles = {(3, 3), (3, 4), (3, 5)} #a set of tuples of positions
        self.next_tiles = set()
        self.neighbours = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        self.tile_images = [] 
        
    def update(self):
        '''LifeBoard.update()
        updates the board, clears all tiles and adds new ones'''
        tested = set()
        for i, j in self.current_tiles:
            if (i, j) not in tested:
                tested.add((i, j))
                if self.test_tile(i, j):
                    self.next_tiles.add((i, j))
                else:
                    self.next_tiles.discard((i, j))
            for a, b in self.neighbours:
                if (a+i, b+j) not in tested:
                    tested.add((a+i, b+j))
                    if self.test_tile(a+i, b+j):
                        self.next_tiles.add((a+i, b+j))
                    else:
                        self.next_tiles.discard((a+i, b+j))
        self.current_tiles = self.next_tiles.copy()
        self.update_display()
        
    def test_tile(self, x, y):
        '''LifeBoard.test_tile(x, y) -> boolean
        given a position, using the current tiles,
        check whether during the next run it will be highlighted'''
        total = 0
        for i, j in self.neighbours:
            if (i+x, j+y) in self.current_tiles:
                total += 1
        if total==2:
            return (x, y) in self.current_tiles
        elif total==3:
            return True
        else:
            return False
        
    def update_display(self):
        '''LifeBoard.update_display()
        updates all of the tiles based off of the new current_tiles set'''
        for i in self.tile_images:
            self.delete(i)
        for a, b in self.current_tiles:
            self.tile_images.append(self.create_rectangle(10*a, 10*b, 10*a+10, 10*b+10))
    

class LifeFrame(Frame):
    def __init__(self, master):
        '''LifeFrame(master) -> new LifeFrame
        where master is a Tk object'''
        Frame.__init__(self, master)
        self.grid()
        self.board = LifeBoard(master, 10, 20)
        self.board.grid()
        self.time = 50
        self.loop()
        
    def loop(self):
        '''LifeFrame.loop()
        start the gameplay loop'''
        self.board.update()
        self.after(self.time, self.loop)
        
root = Tk()
l = LifeFrame(root)
root.mainloop()
