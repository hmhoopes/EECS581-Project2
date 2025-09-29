import numpy as np
from constants import *
import pygame
from pygame.locals import * #for sound
from pygame import mixer #for sound
from utility_functions import *


def generate_board(size, num_mines):
    """
    Generate board array and place mines with adjacent counts.
    Args:
        size (int): Board size
        num_mines (int): Number of mines
    Returns:
        np.ndarray: Board array (-1 for mine, 0+ for adjacent count)
    """
    board = np.zeros((size, size), dtype=int)
    mines = np.random.choice(size * size, num_mines, replace=False)
    for idx in mines:
        x, y = divmod(idx, size)   # get x y from just index. basically division with a remainder
        board[x, y] = -1  # Place mine
        # Increment adjacent mine counts
        for i in range(max(0, x - 1), min(size, x + 2)):
            for j in range(max(0, y - 1), min(size, y + 2)):
                if board[i, j] != -1:
                    # Add to adjacent cell's mine count
                    board[i, j] += 1
    return board

def play_music(music_file, volume = 0.1):
    loop = True
    mixer.music.pause()
    mixer.music.load(music_file)
    mixer.music.set_volume(volume)
    mixer.music.play(-1 if loop else 0)

def reveal(board, revealed, x, y):
    """
    Reveal a cell recursively if it is empty.
    Args:
        board: Board array
        revealed: Revealed state array
        x, y: Cell coordinates (not actual mouse coordinates)
    """
    if revealed[x, y] or board[x, y] == -1:
        return
    revealed[x, y] = True

    # recursively reveal if empty cell (No adjacent mines)
    if board[x, y] == 0:
        # Recursively reveal adjacent empty cells
        for i in range(max(0, x - 1), min(GRID_SIZE, x + 2)):
            for j in range(max(0, y - 1), min(GRID_SIZE, y + 2)):
                if not revealed[i, j]:
                    # Reveal neighbor if not already revealed
                    reveal(board, revealed, i, j)

def flag(board, revealed, flagged, x, y):
    """
    Place or remove a flag on a cell.
    Args:
        board: Board array
        revealed: Revealed state array
        flagged: Flagged state array
        x, y: Cell coordinates (not actual mouse coordinates)
    """
    if revealed[x, y]:
        return
    # Toggle flag state for this cell
    flagged[x, y] = not flagged[x, y]

def draw_board(surface, board, revealed, flagged, sprites, fonts, status_text, num_mines, flag_count, restart_btn, quit_btn):
    """
    Draw all cells, flags, mines, numbers, grid lines, labels, and UI elements.
    Args:
        surface: Pygame surface
        board: Board array
        revealed: Revealed state array
        flagged: Flagged state array
        sprites: Sprite dictionary
        fonts: Font dictionary
        status_text: Status string
        num_mines: Number of mines
        flag_count: Number of flags placed
        restart_btn, quit_btn: Button objects
    """
    surface.fill(LIGHT_GRAY)
    # Draw mine/flag info
    rem_text = fonts['big'].render(f"Mines: {num_mines}", True, BLACK)
    remain_flags_text = fonts['small'].render(f"Flags left: {num_mines - flag_count}", True, BLACK)
    surface.blit(rem_text, (20, WINDOW_HEIGHT - 90))
    surface.blit(remain_flags_text, (20, WINDOW_HEIGHT - 60))
    # Draw status
    status_render = fonts['big'].render(status_text, True, RED if "Game Over" in status_text else (GREEN if status_text == "Victory" else BLACK))
    surface.blit(status_render, (MARGIN_LEFT + BOARD_PIXELS//2 - status_render.get_width()//2, 20))
    # Draw controls hint
    hint = fonts['small'].render("Left-click: uncover  |  Right-click: flag  |  R: restart", True, BLACK)
    surface.blit(hint, (MARGIN_LEFT, WINDOW_HEIGHT - 30))

    # Draw each cell
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # grid rectangles
            rect = pygame.Rect(MARGIN_LEFT + y * CELL_SIZE, MARGIN_TOP + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[x, y]:
                # Reveal cell
                surface.blit(pygame.transform.scale(sprites['clicked'], (CELL_SIZE, CELL_SIZE)), rect)
                if board[x, y] == -1:
                    surface.blit(pygame.transform.scale(sprites['mineClicked'], (CELL_SIZE, CELL_SIZE)), rect)
                elif board[x, y] > 0:
                    surface.blit(pygame.transform.scale(sprites[f'grid{board[x,y]}'], (CELL_SIZE, CELL_SIZE)), rect)
            elif flagged[x, y]:
                # Draw flag
                surface.blit(pygame.transform.scale(sprites['flag'], (CELL_SIZE, CELL_SIZE)), rect)
            else:
                # Draw unrevealed cell
                surface.blit(pygame.transform.scale(sprites['basic'], (CELL_SIZE, CELL_SIZE)), rect)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)
            # Draw grid border for each cell
    draw_labels(surface, fonts)
    restart_btn.draw(surface)
    quit_btn.draw(surface)

def restart_game(num_mines):
    """
    Initialize a new game state.
    Args:
        num_mines (int): Number of mines
    Returns:
        tuple: (board, revealed, flagged, start, game_over)
    """
    board = generate_board(GRID_SIZE, num_mines)
    
    # Initialize arrays for revealed and flagged cells
    revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    flagged = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    start = True  # Indicates first click
    game_over = False
    # Return all game state arrays and flags
    return board, revealed, flagged, start, game_over