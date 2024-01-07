# conways-game-of-life
Simulation of Conway's Game of Life created in Python
Leverages Pygame for rendering and user input and NumPy to represent the board with cells

settings.json includes customization options for the game

Controls:
- r: sets all cells on board to dead
- space: pause/unpause the simulation
- lmb: set a given cell to alive
- rmb: set a given cell to dead
- mwheelup: increase delay by 10ms (max 1000ms)
- mwheeldown: decrease delay by 10ms (min 20ms)
