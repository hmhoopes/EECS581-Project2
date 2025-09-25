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


def ask_mine_count(screen, clock, fonts):
    """
    Allow user to choose mine count before starting game using a slider UI.
    Args:
        screen: Pygame display surface
        clock: Pygame clock
        fonts: Font dictionary
    Returns:
        int: Selected mine count
    """
    slider = Slider(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2, 300, 10, 20, 10, fonts['big'])
    confirm_btn = Button((WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 80, 160, 50), "Confirm", fonts['big'])

    while True:
        screen.fill(LIGHT_GRAY)
        title = fonts['big'].render("Choose Mine Count", True, BLUE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 120))

        slider.draw(screen)
        confirm_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            slider.handle_event(event)
            if confirm_btn.is_clicked(event):
                # Return the selected mine count when confirmed
                return slider.value

        pygame.display.flip()
        clock.tick(FPS)

def load_sprites():
    """
    Load all game sprite images from the sprites/ directory.
    Returns:
        dict: Sprite surfaces keyed by name
    """
    sprites = {}
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