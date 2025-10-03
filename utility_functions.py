"""
Minesweeper Utility Functions

Module Name: utility_functions.py
Description: Stores miscellaneous functions
             

Inputs/Output: 
    - Many to different functions:
       - clamp_mines(n: int) -> int
       - initialize_game(screen, clock, fonts) -> None, initializes buttons and checks for user to click buttons
       - load_sprites() -> sprites, returns dictionary of sprites
       - draw_labels(surface, fonts) -> None, Draw column letters (A-J) and row numbers (1-10) on the board

External Sources: 
    - Pygame library
    - Sprites from sprites/

Author: Team 8 & Team 17
Creation Date: 9/24/2025
"""
import pygame
from constants import *
from button import Button
from slider import Slider
import sys

############################################################
# Utility Functions
############################################################
def clamp_mines(n: int) -> int:
    """
    Clamp mine number to allowed range (10-20).
    Args:
        n (int): Desired mine count
    Returns:
        int: Clamped mine count
    """
    # Use max/min to ensure mine count stays in bounds
    return max(10, min(20, n))

def initialize_game(screen, clock, fonts):
    """
    Allow user to choose mine count and AI mode before starting game using a slider UI.
    Args:
        screen: Pygame display surface
        clock: Pygame clock
        fonts: Font dictionary
    Returns:
        int: Selected mine count
        AIDifficulty: selected AIDifficulty
        AIMode: selected AIMode
    """
    difficulty = AIDifficulty.Easy
    mode = AIMode.Off

    slider = Slider(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 150, 300, 10, 20, 10, fonts['big'])
    confirm_btn = Button((WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 100, 160, 50), "Confirm", fonts['big'])
    
    ai_easy_btn = Button((WINDOW_WIDTH // 4 - 120, WINDOW_HEIGHT // 2, 160, 50), "Easy", fonts['big'])
    ai_medium_btn = Button((WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2, 160, 50), "Medium", fonts['big'])
    ai_hard_btn = Button(((WINDOW_WIDTH * 3) // 4 - 40, WINDOW_HEIGHT // 2, 160, 50), "Hard", fonts['big'])

    ai_off_btn = Button((WINDOW_WIDTH // 4 - 120, WINDOW_HEIGHT // 2 + 100, 160, 50), "Off", fonts['big'])
    ai_alternate_btn = Button((WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 100, 160, 50), "Alternate", fonts['big'])
    ai_solve_btn = Button(((WINDOW_WIDTH * 3) // 4 - 40, WINDOW_HEIGHT // 2 + 100, 160, 50), "Solve", fonts['big'])

    while True:
        screen.fill(LIGHT_GRAY)
        title = fonts['big'].render("Choose Mine Count", True, BLUE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 120))

        ai_diff_text = "Off"
        match (difficulty):
            case AIDifficulty.Easy:
                ai_diff_text = "Easy"         
            case AIDifficulty.Medium:
                ai_diff_text = "Medium"
            case AIDifficulty.Hard:
                ai_diff_text = "Hard"
        ai_mode_text = "Alternate"
        match (mode):
            case AIMode.Off:
                ai_diff_text += " (will not run currently)"
                ai_mode_text = "Off"
            case AIMode.Solver:
                ai_mode_text = "Solve"
        ai_diff = fonts['big'].render("AI Difficulty: " + ai_diff_text, True, BLUE)
        ai_mode = fonts['big'].render("AI Mode: " + ai_mode_text, True, BLUE)
        screen.blit(ai_diff, (WINDOW_WIDTH // 2 - ai_diff.get_width() // 2, WINDOW_HEIGHT // 2 - 30))
        screen.blit(ai_mode, (WINDOW_WIDTH // 2 - ai_mode.get_width() // 2, WINDOW_HEIGHT // 2 + 70))

        slider.draw(screen)
        confirm_btn.draw(screen)
        ai_easy_btn.draw(screen)
        ai_medium_btn.draw(screen)
        ai_hard_btn.draw(screen)
        ai_off_btn.draw(screen)
        ai_alternate_btn.draw(screen)
        ai_solve_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            slider.handle_event(event)
            if confirm_btn.is_clicked(event):
                # Return the selected mine count when confirmed
                return slider.value, difficulty, mode
            if ai_easy_btn.is_clicked(event):
                difficulty = AIDifficulty.Easy
            if ai_medium_btn.is_clicked(event):
                difficulty = AIDifficulty.Medium
            if ai_hard_btn.is_clicked(event):
                difficulty = AIDifficulty.Hard
            if ai_off_btn.is_clicked(event):
                mode = AIMode.Off
            if ai_alternate_btn.is_clicked(event):
                mode = AIMode.Alternate                
            if ai_solve_btn.is_clicked(event):
                mode = AIMode.Solver

        pygame.display.flip()
        clock.tick(FPS)

def load_sprites():
    """
    Load all game sprite images from the sprites/ directory.
    Returns:
        dict: Sprite surfaces keyed by name
    """
    sprites = {}
    sprites['you_loose'] = pygame.image.load("sprites/you_loose.png")
    sprites['you_win'] = pygame.image.load("sprites/you_win.png")
    sprites['clicked'] = pygame.image.load("sprites/clicked.png")
    sprites['flag'] = pygame.image.load("sprites/flag.png")
    sprites['basic'] = pygame.image.load("sprites/basic.png")
    # Load numbered grid sprites
    for i in range(1, 9):
        sprites[f'grid{i}'] = pygame.image.load(f"sprites/grid_{i}.png")
    sprites['mine'] = pygame.image.load("sprites/bomb.png")
    sprites['mineClicked'] = pygame.image.load("sprites/bomb_clicked.png")
    # Return all loaded sprites as a dictionary
    return sprites


def draw_labels(surface, fonts):
    """
    Draw column letters (A-J) and row numbers (1-10) on the board.
    Args:
        surface: Pygame surface
        fonts: Font dictionary
    """
    col_labels = [chr(ord('A') + i) for i in range(GRID_SIZE)]
    for i, c in enumerate(col_labels):
        text = fonts['small'].render(c, True, BLACK)
        surface.blit(text, (MARGIN_LEFT + i * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2, MARGIN_TOP + GRID_SIZE * CELL_SIZE + 5))
    for i in range(GRID_SIZE):
        text = fonts['small'].render(str(i+1), True, BLACK)
        # Draw row number label to the left of each row
        surface.blit(text, (MARGIN_LEFT - 25, MARGIN_TOP + i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2))