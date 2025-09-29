"""
product_2.py - Minesweeper Game Implementation

Module: product_2
Description: Implements a graphical Minesweeper game using Pygame. Handles UI, game logic, and user interaction.
Inputs: User mouse/keyboard events, configuration constants
Outputs: Graphical game window, game state changes
Authors: Riley England, Jackson Yanek, Evan Chigweshe, Manu Redd, Cole Cooper
Creation Date: September 3rd-21st, 2025
External Sources: Generative AI, Pygame documentation, NumPy documentation
Originality: Original with the aid of generative AI
"""

import pygame  # Pygame for graphics and UI
import numpy as np  # NumPy for board state management
import sys  # System exit
from constants import *
from button import Button
from utility_functions import *
from board_functions import *
from ai import AIEngine
from time import sleep


def main():
    """
    Main entry point for Minesweeper game. Handles initialization, menu, game loop, and user input.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("EECS581 Project 1:Minesweeper")
    clock = pygame.time.Clock()

    # Sound
    play_music(START_MUSIC_1) #loads in start menu music

    # Initialize fonts
    small = pygame.font.Font(FONT_NAME, 22)
    big = pygame.font.Font(FONT_NAME, 36)
    fonts = {'small': small, 'big': big}

    # Load sprite images
    sprites = load_sprites()

    # Main menu buttons
    play_button = Button((WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 60, 200, 50), "Play Game", big)
    quit_button = Button((WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 10, 200, 50), "Quit", big)

    # Show menu loop
    in_menu = True
    while in_menu:
        screen.fill(LIGHT_GRAY)
        title_text = big.render("Minesweeper", True, BLUE)
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100))
        play_button.draw(screen)
        quit_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play_button.is_clicked(event):
                in_menu = False
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)

    # Ask for number of mines and initialize game
    mines, difficulty, mode = initialize_game(screen, clock, fonts)
    pygame.event.clear()
    mines = clamp_mines(mines)
    board, revealed, flagged, start, game_over = restart_game(mines)
    status = "Playing"
    ignore_next_click = True  # Skip leftover click from menu

    # Bottom buttons
    button_width, button_height = 100, 40
    spacing = 20
    total_width = 2 * button_width + spacing
    start_x = MARGIN_LEFT + (BOARD_PIXELS - total_width) // 2
    button_y = MARGIN_TOP + BOARD_PIXELS + 50
    restart_btn = Button((start_x, button_y, button_width, button_height), "Restart", small)
    quit_btn = Button((start_x + button_width + spacing, button_y, button_width, button_height), "Quit", small)

    turn = 0 # turn number, so that we can see if it is AI's turn or players turn
    ai = AIEngine(difficulty)

    running = True
    while running:
        flag_count = np.sum(flagged)
        # if it is AI's turn, ai make move. else check for player events
        if (mode == AIMode.Solver or (mode == AIMode.Alternate and turn % 2 != 0)) and not game_over:
            sleep(.25) # sleep for a bit just so ai doesnt go immediately after player
            # get ai's move
            ai_x, ai_y = ai.make_move(board=board, revealed=revealed)
            # copied from their code, just checks if x, y is mine or not and then acts accordingly
            if board[ai_x, ai_y] == -1:
                play_music(LOSE_MUSIC) #loads in lose music

                # Hit a mine -> game over
                revealed[:, :] = True
                status = "Game Over"
                game_over = True
            else:
                reveal(board, revealed, ai_x, ai_y)
            turn += 1 # update turn number

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Restart / Quit buttons
            if restart_btn.is_clicked(event):
                play_music(START_MUSIC_1)
                mines, difficulty, mode = initialize_game(screen, clock, fonts)
                ai.set_difficulty(difficulty)
                pygame.event.clear()
                mines = clamp_mines(mines)
                board, revealed, flagged, start, game_over = restart_game(mines)
                status = "Playing"
                ignore_next_click = True
            if quit_btn.is_clicked(event):
                running = False
            # Restart with R key
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mines, difficulty, mode = initialize_game(screen, clock, fonts)
                ai.set_difficulty(difficulty)
                pygame.event.clear()
                mines = clamp_mines(mines)
                board, revealed, flagged, start, game_over = restart_game(mines)
                status = "Playing"
                ignore_next_click = True
            # Game input
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and (mode == AIMode.Off or (mode == AIMode.Alternate and turn % 2 != 1)):
                    if ignore_next_click:
                        ignore_next_click = False
                        continue  # Skip leftover click from menu
                    mx, my = pygame.mouse.get_pos()
                    x = (my - MARGIN_TOP) // CELL_SIZE
                    y = (mx - MARGIN_LEFT) // CELL_SIZE
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if event.button == 1:  # Left-click
                            if start:
                                # Ensure first click is not a mine
                                while board[x, y] == -1:
                                    board = generate_board(GRID_SIZE, mines)
                                reveal(board, revealed, x, y)
                                start = False
                            else:
                                if board[x, y] == -1:
                                    play_music(LOSE_MUSIC) #loads in lose music

                                    # Hit a mine -> game over
                                    revealed[:, :] = True
                                    status = "Game Over"
                                    game_over = True
                                else:
                                    reveal(board, revealed, x, y)
                            turn += 1 # update turn number
                        elif event.button == 3:  # Right-click to flag
                            if not revealed[x, y]:
                                flag(board, revealed, flagged, x, y)
        # Check for victory
        if not game_over and np.all(revealed | (board == -1)):
            play_music(WIN_MUSIC) #loads in win music
            # All non-mine cells revealed: player wins
            status = "Victory"
            game_over = True

        draw_board(screen, board, revealed, flagged, sprites, fonts, status, mines, flag_count, restart_btn, quit_btn)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Run the game
main()

