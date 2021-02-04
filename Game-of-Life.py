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
        self.current_tiles = {} #a set of tuples of positions
        self.next_tiles = {} #a set of tuples of positions
        
    def update(self):
        '''LifeBoard.update()
        updates the board, clears all tiles and adds new ones'''
        pass
    def test_tile(self, x, y):
        '''LifeBoard.test_tile(x, y) -> boolean
        given a position, using the current tiles,
        check whether during the next run it will be highlighted'''
        pass

class LifeFrame(Frame):
    def __init__(self, master):
        '''LifeFrame(master) -> new LifeFrame
        where master is a Tk object'''
        Frame.__init__(self, master)
        self.grid()
        self.board = LifeBoard(master, 10, 20)
        self.board.grid()
    def loop(self):
        '''LifeFrame.loop()
        start the gameplay loop'''

root = Tk()
l = LifeFrame(root)
