from tkinter import *
from time import sleep
import threading

class LifeBoard(Canvas):
    def __init__(self, master, size, buffer):
        '''LifeBoard(size, buffer) -> new LifeBoard
        where size is both the width and height of the board
        and buffer is the distance out from the board that tiles are tracked'''
        Canvas.__init__(self, master, bg="grey", width=size*10, height=size*10)
        self.size = size
        self.buffer = buffer
        self.current_tiles = {(25,25), (26,25), (27,25), (27,24), (24, 24), (25, 23)}
        self.next_tiles = set()
        self.neighbours = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        self.tile_images = []
        self.bind('<Button-1>', self.click)
        
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
        if x<0 or x>self.size or y<0 or y>self.size:
            return False
        
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
            self.tile_images.append(self.create_rectangle(10*a, 10*b, 10*a+10, 10*b+10, fill="yellow", outline="yellow"))
    def click(self, event):
        '''LifeBoard.click()
        handler method for clicks'''
        print("click")
        if (event.x//10, event.y//10) in self.current_tiles:
            self.current_tiles.discard((event.x//10, event.y//10))
        else:
            self.current_tiles.add((event.x//10, event.y//10))
        self.update_display()
    
class LifeFrame(Frame):
    def __init__(self, master, size, time_step):
        '''LifeFrame(master) -> new LifeFrame
        where master is a Tk object'''
        Frame.__init__(self, master)
        self.grid()
        self.board = LifeBoard(master, size, 20)
        self.board.grid()
        self.time = time_step
        self.looping = False
        self.stop_start_button = Button(master, text="start", command=self.start)
        self.stop_start_button.grid()
        
    def loop(self):
        '''LifeFrame.loop()
        start the gameplay loop'''
        if self.looping:
            self.board.update()
            self.after(self.time, self.loop)
    def start(self):
        '''LifeFrame.start()
        starts the mainloop of the game of life'''
        if self.looping == False:
            self.stop_start_button["text"] = "stop"
            self.stop_start_button["command"] = self.stop
            self.looping = True
            self.loop()
    def stop(self):
        '''LifeFrame.stop()
        stops the mainloop of the game of life'''
        self.looping = False
        self.stop_start_button["text"] = "start"
        self.stop_start_button["command"] = self.start
        
root = Tk()
l = LifeFrame(root, 50, 10)
root.mainloop()
