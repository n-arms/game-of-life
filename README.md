# game-of-life
A python implementation of Conway's game of life, a simulation where there are a number of tiles
arranged in a grid, each tile is in 1 of two states, and tiles evolve over time based off of their neighbours.

The exact rules are as follows:
- Every cell is either living or dead
- A live cell dies if it has less than 2 or more than 3 neighbours
- If a dead cell has exactly 3 neighbours it becomes alive

My specific implementation only tracks tiles that are on screen, and so starting a configuration in a different place will result in different outcomes.
