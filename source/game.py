import pygame
import sys
import numpy as np
import json
# load the settings
try:
    with open("settings.json", 'r') as file:
        settings_dict = json.load(file)
except FileNotFoundError:
    print("Error: 'settings.json' not found.")
    sys.exit()
# independent constants
SCREEN_SIZE = settings_dict["SCREEN_SIZE"]
ROWS = settings_dict["ROWS"]
COLS = settings_dict["COLS"]
DELAY_MS = settings_dict["DELAY_MS"]
HIGHLIGHT_SLEEP_MS = settings_dict["HIGHLIGHT_SLEEP_MS"]
# dependent constants
CELL_SIZE = SCREEN_SIZE[0] / COLS, SCREEN_SIZE[1] / ROWS

def initialize_board(rows, cols, density=0.2):
    """Initialize a random board with given density."""
    board = np.random.choice([False, True], size=(rows, cols), p=[1 - density, density])
    return board

def get_neighbors(board, i, j):
    """
    Get the neighbors of a cell.
    Parameters:
    - board: NumPy array representing the Game of Life board
    - 

    Return:
    - board: NumPy array representing the Game of Life board
    - i: int representing row index of the cell in the board
    - j: int representing col index of the cell in the board
    """
    rows, cols = board.shape
    neighbors = [
        board[(i - 1) % rows, (j - 1) % cols],
        board[(i - 1) % rows, j],
        board[(i - 1) % rows, (j + 1) % cols],
        board[i, (j - 1) % cols],
        board[i, (j + 1) % cols],
        board[(i + 1) % rows, (j - 1) % cols],
        board[(i + 1) % rows, j],
        board[(i + 1) % rows, (j + 1) % cols]
    ]
    return neighbors

def update_board(board):
    """
    Update the board based on the rules of Conway's Game of Life.

    Parameters:
    - board: NumPy array representing the Game of Life board

    Return:
    - board: NumPy array representing the Game of Life board
    """
    new_board = np.copy(board)
    rows, cols = board.shape

    for i in range(rows):
        for j in range(cols):
            neighbors = get_neighbors(board, i, j)
            live_neighbors = np.sum(neighbors)

            if board[i, j]:
                # Cell is alive
                if live_neighbors < 2 or live_neighbors > 3:
                    new_board[i, j] = 0  # Dies due to underpopulation or overpopulation
            else:
                # Cell is dead
                if live_neighbors == 3:
                    new_board[i, j] = 1  # Becomes alive due to reproduction

    return new_board

def clear_board():
    return np.full((ROWS, COLS), False, dtype=bool)

def toggle_cell(board, row, col):
    """
    Toggle the state of a cell (alive to dead, dead to alive) in the given board.
    
    Parameters:
    - board: NumPy array representing the Game of Life board
    - row: int representing row index of the cell in the board
    - col: int representing col index of the cell in the board
    """
    rows, cols = board.shape
    i = int(row % rows)
    j = int(col % cols)
    board[i, j] = not board[i, j]

def set_cell(board, row, col, state):
    """
    Set the state of a cell in the given board.

    Parameters:
    - board: NumPy array representing the Game of Life board
    - row: int representing row index of the cell in the board
    - col: int representing col index of the cell in the board
    - state: boolean representing alive (True) or dead (False)
    """
    rows, cols, = board.shape
    i = int(row % rows)
    j = int(col % cols)
    board[i, j] = state

def draw_board(screen, board, alive_color=(255, 255, 255), dead_color=(0, 0, 0)):
    """
    Draw the Game of Life board on the given Pygame screen.

    Parameters:
    - screen: Pygame screen object
    - board: NumPy array representing the Game of Life board
    - cell_size: Size of each cell in pixels
    - alive_color: RGB color tuple for alive cells
    - dead_color: RGB color tuple for dead cells
    """
    rows, cols = board.shape

    for i in range(rows):
        for j in range(cols):
            x = j * CELL_SIZE[0]
            y = i * CELL_SIZE[1]
            if board[i, j]:
                pygame.draw.rect(screen, alive_color, (x, y, CELL_SIZE[0], CELL_SIZE[1]))
            else:
                pygame.draw.rect(screen, dead_color, (x, y, CELL_SIZE[0], CELL_SIZE[1]))

def main():
    

    # initiate pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # create the clock
    clock = pygame.time.Clock()
    last_update_time = pygame.time.get_ticks()
    last_highlight_time = pygame.time.get_ticks()
    last_mouse_pos = pygame.mouse.get_pos()
    # create the baord
    board = initialize_board(ROWS, COLS)

    # game on
    game_on = True

    # create highlight rect
    highlighted_rect = pygame.Rect(-CELL_SIZE[0], -CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1])
    
    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check for keyboard input
            elif event.type == pygame.KEYDOWN:
                # spacebar -> pause the game
                if event.key == pygame.K_SPACE:
                    game_on = not game_on
                # r key -> clear the board
                elif event.key == pygame.K_r:
                    board = clear_board()

        # get mouse position info
        x, y = pygame.mouse.get_pos()
        row = y // CELL_SIZE[1]
        col = x // CELL_SIZE[0]

        # get time info
        current_time = pygame.time.get_ticks()

        # check if the mouse has moved
        if (x, y) != last_mouse_pos:
            last_mouse_pos = (x, y)
            last_highlight_time = current_time
            cell_x = col * CELL_SIZE[0]
            cell_y = row * CELL_SIZE[1]
            highlighted_rect.topleft = (cell_x, cell_y)

        # check mouse button presses
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # 0 corresponds to the left mouse button
            set_cell(board, row, col, True)
        elif mouse_buttons[2]: # 2 corresponds to the right mouse button
            set_cell(board, row, col, False)

        # check if the mouse has been still for HIGHLIGHT_SLEEP_MS
        if current_time - last_highlight_time >= HIGHLIGHT_SLEEP_MS:
            highlighted_rect.topleft = (-CELL_SIZE[0], -CELL_SIZE[1])

        # update the board
        if pygame.time.get_ticks() - last_update_time >= DELAY_MS and game_on:
            board = update_board(board)
            last_update_time = pygame.time.get_ticks()

        # update screen
        draw_board(screen, board)
        pygame.draw.rect(screen, (255, 0, 0), highlighted_rect, 2)


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()