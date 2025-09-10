import pygame
import numpy as np
import sys

# Game settings
GRID_SIZE = 10
CELL_SIZE = 40
NUM_MINES = 10
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE

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

def reveal(board, revealed, x, y):
    if revealed[x, y] or board[x, y] == -1:
        return
    #set x y to revealed
    revealed[x, y] = True

    #recursively reveal if empty cell (No adjacent mines)
    if board[x, y] == 0:
        for i in range(max(0, x-1), min(GRID_SIZE, x+2)):
            for j in range(max(0, y-1), min(GRID_SIZE, y+2)):
                if not revealed[i, j]:
                    reveal(board, revealed, i, j)

def flag(board, revealed, flagged, x, y):
    if revealed[x, y] or flagged[x,y]:
        return
    #set x y to revealed
    flagged[x, y] = True

def draw_board(screen, board, revealed, flagged):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            #grid rectangles
            rect = pygame.Rect(y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[x, y]:
                #reveal the cell
                pygame.draw.rect(screen, REVEALED_COLOR, rect)
                
                #if mine
                if board[x, y] == -1:
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, CELL_SIZE//3)
                
                # if adjacent
                elif board[x, y] > 0:
                    text = FONT.render(str(board[x, y]), True, TEXT_COLOR)
                    screen.blit(text, text.get_rect(center=rect.center))
            elif flagged[x,y] and not(revealed[x,y]):
                pygame.draw.circle(screen, FLAG_COLOR, rect.center, CELL_SIZE//3)
            else:
                pygame.draw.rect(screen, BG_COLOR, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def main():
    #create the screen & add caption
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EECS581 Project 1: Minesweeper")

    #Get board
    board = generate_board(GRID_SIZE, NUM_MINES)
    revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    flagged = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    running = True

    #Game loop
    while running:
        screen.fill(BG_COLOR)
        draw_board(screen, board, revealed, flagged)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            #check for mouse click for revealing
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos() # mouse x, y
                x, y = my // CELL_SIZE, mx // CELL_SIZE #get cell from mouse position
                if not revealed[x, y]:
                    if board[x, y] == -1:
                        revealed[:, :] = True  # Reveal all on mine hit
                    else:
                        reveal(board, revealed, x, y) #reveal that x y
            
            #flag
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = pygame.mouse.get_pos() # mouse x, y
                x, y = my // CELL_SIZE, mx // CELL_SIZE #get cell from mouse position
                if not flagged[x, y] and not(revealed[x,y]):
                    flag(board, revealed, flagged, x, y) #flag that x y
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()