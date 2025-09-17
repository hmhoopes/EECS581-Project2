import pygame
import numpy as np
import sys

# Game settings
GRID_SIZE = 10
CELL_SIZE = 40
NUM_MINES = 10
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE + 60
GAME_WIDTH = WIDTH 
GAME_HEIGHT = WIDTH 

# Colors
BG_COLOR = (200, 200, 200)
GRID_COLOR = (100, 100, 100)
REVEALED_COLOR = (220, 220, 220)
MINE_COLOR = (20, 20, 20)
TEXT_COLOR = (0, 0, 0)
FLAG_COLOR = (255, 0, 0)

#Init pygame
pygame.init()
FONT = pygame.font.SysFont(None, 32)

# Load sprites
sprite_clicked = pygame.image.load("sprites/clicked.png")
sprite_flag = pygame.image.load("sprites/flag.png")
sprite_basic = pygame.image.load("sprites/basic.png")
sprite_grid1 = pygame.image.load("sprites/grid_1.png")
sprite_grid2 = pygame.image.load("sprites/grid_2.png")
sprite_grid3 = pygame.image.load("sprites/grid_3.png")
sprite_grid4 = pygame.image.load("sprites/grid_4.png")
sprite_grid5 = pygame.image.load("sprites/grid_5.png")
sprite_grid6 = pygame.image.load("sprites/grid_6.png")
sprite_grid7 = pygame.image.load("sprites/grid_7.png")
sprite_grid8 = pygame.image.load("sprites/grid_8.png")
sprite_grid7 = pygame.image.load("sprites/grid_7.png")
sprite_mine = pygame.image.load("sprites/bomb.png")
sprite_mineClicked = pygame.image.load("sprites/bomb_clicked.png")

#Generate board
def generate_board(size, num_mines):
    #start with 0 grid (occupancy grid for mines)
    board = np.zeros((size, size), dtype=int)
    
    #random indices for mines
    mines = np.random.choice(size*size, num_mines, replace=False)

    #iterate through mines and place a mine in each index
    for idx in mines:
        #get x y from just index. basically division with a remainder
        x, y = divmod(idx, size)
        
        #place mine
        board[x, y] = -1

        #adjacent mine counter
        for i in range(max(0, x-1), min(size, x+2)):
            for j in range(max(0, y-1), min(size, y+2)):
                if board[i, j] != -1:
                    board[i, j] += 1 #add when its an empty cell
    return board

def restart_game():
    """Initialize a new game state"""
    # Generate new board with mines
    board = generate_board(GRID_SIZE, NUM_MINES)
    # Initialize arrays for revealed and flagged cells
    revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    flagged = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    # Set initial game states
    start = True
    game_over = False
    return board, revealed, flagged, start, game_over

def reveal(board, revealed, x, y):
    #set x y to revealed if not already revealed or a mine
    if revealed[x, y] or board[x, y] == -1:
        return
    revealed[x, y] = True

    #recursively reveal if empty cell (No adjacent mines)
    if board[x, y] == 0:
        for i in range(max(0, x-1), min(GRID_SIZE, x+2)):
            for j in range(max(0, y-1), min(GRID_SIZE, y+2)):
                if not revealed[i, j]:
                    reveal(board, revealed, i, j)

def flag(board, revealed, flagged, x, y):
    #flag cell if not revealed
    if revealed[x, y]:
        return
    if flagged[x, y]:
        #remove flag
        flagged[x, y] = False
    else:
        #set flag
        flagged[x, y] = True

def draw_board(screen, board, revealed, flagged):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            #grid rectangles
            rect = pygame.Rect(y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[x, y]:
                #reveal the cell
                screen.blit(pygame.transform.scale(sprite_clicked, (CELL_SIZE, CELL_SIZE)), rect)
                
                #if mine
                if board[x, y] == -1:
                    # different if clicked mine
                    if np.any(revealed & (board == -1)) and revealed[x, y]:
                        screen.blit(pygame.transform.scale(sprite_mineClicked, (CELL_SIZE, CELL_SIZE)), rect)
                    else:
                        screen.blit(pygame.transform.scale(sprite_mine, (CELL_SIZE, CELL_SIZE)), rect)
                # if adjacent
                elif board[x, y] > 0:
                    num_sprite = {        # dictionary to map numbers to sprites with bomb numbers
                        1: sprite_grid1, 
                        2: sprite_grid2, 
                        3: sprite_grid3, 
                        4: sprite_grid4, 
                        5: sprite_grid5, 
                        6: sprite_grid6, 
                        7: sprite_grid7, 
                        8: sprite_grid8, 
                    } [board[x, y]]
                    # Display number sprite for adjacent mines
                    screen.blit(pygame.transform.scale(num_sprite, (CELL_SIZE, CELL_SIZE)), rect)
                else: 
                    # Display empty revealed cell
                    screen.blit(pygame.transform.scale(sprite_clicked, (CELL_SIZE, CELL_SIZE)), rect)
            elif flagged[x,y] and not(revealed[x,y]):
                # Display flag on unrevealed cell
                screen.blit(pygame.transform.scale(sprite_flag, (CELL_SIZE, CELL_SIZE)), rect)
            else:
                # Display basic unrevealed cell
                screen.blit(pygame.transform.scale(sprite_basic, (CELL_SIZE, CELL_SIZE)), rect)
            # Draw grid lines
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def game_status(window, status):
    if status == 0:
        text = FONT.render("Current Status: Playing", True, (0, 0, 0))
        window.blit(text, (10, 420))
        pygame.display.flip()
    elif status == -1:
        text = FONT.render("Current Status: Game Over", True, (0, 0, 0))
        window.blit(text, (10, 420))
        pygame.display.flip()
    elif status == 1:
        text = FONT.render("Current Status: You Win!", True, (0, 0, 0))
        window.blit(text, (10, 420))
        pygame.display.flip()
        
def main():
    #create the screen & add caption
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    
    pygame.display.set_caption("EECS581 Project 1: Minesweeper")

    #Get board
    board = generate_board(GRID_SIZE, NUM_MINES)
    revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    flagged = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    running = True
    start = True

    #Game loop
    while running:
        window.fill(BG_COLOR)
        screen.fill(BG_COLOR)
        draw_board(screen, board, revealed, flagged)
        game_status(window, 0)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # Restart functionality (press "r" to restart game)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board, revealed, flagged, start, game_over = restart_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start:
                mx, my = pygame.mouse.get_pos() # mouse x, y
                x, y = my // CELL_SIZE, mx // CELL_SIZE #get cell from mouse position
                if not revealed[x, y] and not flagged[x,y]: # Flagged check added
                    while board[x, y] == -1:
                        board = generate_board(GRID_SIZE, NUM_MINES)
                    reveal(board, revealed, x, y) #reveal that x y
                    start = False
                else:
                    reveal(board, revealed, x, y) #reveal that x y
                    start = False
            #check for mouse click for revealing
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos() # mouse x, y
                x, y = my // CELL_SIZE, mx // CELL_SIZE #get cell from mouse position
                if not revealed[x, y] and not flagged[x,y]: # Flagged check added
                    if board[x, y] == -1:
                        revealed[:, :] = True  # Reveal all on mine hit
                        game_status(window, -1)
                    else:
                        reveal(board, revealed, x, y) #reveal that x y
            
            #flag
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = pygame.mouse.get_pos() # mouse x, y
                x, y = my // CELL_SIZE, mx // CELL_SIZE #get cell from mouse position
                if not(revealed[x,y]):
                    flag(board, revealed, flagged, x, y) #flag/unflag that x y

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
