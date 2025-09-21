import pygame
import numpy as np
import sys

# ---------- Configuration ----------
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN_LEFT = 80
MARGIN_TOP = 60
WINDOW_PADDING = 20
FONT_NAME = None
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
LIGHT_GRAY = (240, 240, 240)
RED = (200, 40, 40)
GREEN = (40, 160, 40)
BLUE = (30, 60, 220)

# Game-specific colors
BG_COLOR = (200, 200, 200)
GRID_COLOR = (100, 100, 100)  # Color of grid lines
REVEALED_COLOR = (220, 220, 220)  # Color for revealed cells
MINE_COLOR = (20, 20, 20)
TEXT_COLOR = (0, 0, 0)
FLAG_COLOR = (255, 0, 0)

# Derived sizes
BOARD_PIXELS = GRID_SIZE * CELL_SIZE
WINDOW_WIDTH = MARGIN_LEFT + BOARD_PIXELS + WINDOW_PADDING + 100
WINDOW_HEIGHT = MARGIN_TOP + BOARD_PIXELS + WINDOW_PADDING + 200

# ---------- Clamp ----------
def clamp_mines(n: int) -> int:
    # Clamp mine number to allowed range
    return max(10, min(20, n))

# ---------- Button Helper ----------
class Button:
    def __init__(self, rect, text, font, color=GRAY, hover_color=DARK_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(surface, self.hover_color if is_hover else self.color, self.rect, border_radius=6)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # Return True if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# ---------- Slider Helper ----------
class Slider:
    def __init__(self, x, y, w, min_val, max_val, start_val, font):
        self.rect = pygame.Rect(x, y, w, 6)
        self.knob_x = x + int((start_val - min_val) / (max_val - min_val) * w)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.font = font
        self.dragging = False

    def handle_event(self, event):
        # Handle mouse and keyboard input for slider
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.knob_x) < 15 and abs(event.pos[1] - self.rect.centery) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            ratio = (self.knob_x - self.rect.left) / self.rect.width
            self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.value = max(self.min_val, self.value - 1)
            elif event.key == pygame.K_RIGHT:
                self.value = min(self.max_val, self.value + 1)
            self.knob_x = self.rect.left + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)

    def draw(self, surface):
        # Draw slider track and knob
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.circle(surface, BLUE, (self.knob_x, self.rect.centery), 12)
        val_surf = self.font.render(f"{self.value}", True, BLACK)
        surface.blit(val_surf, (self.rect.centerx - val_surf.get_width() // 2, self.rect.top - 35))

# ---------- Ask for mine count with slider ----------
def ask_mine_count(screen, clock, fonts):
    # Allow user to choose mine count before starting game
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
                return slider.value

        pygame.display.flip()
        clock.tick(FPS)

# ---------- Load Sprites ----------
def load_sprites():
    # Load all game sprite images
    sprites = {}
    sprites['clicked'] = pygame.image.load("sprites/clicked.png")
    sprites['flag'] = pygame.image.load("sprites/flag.png")
    sprites['basic'] = pygame.image.load("sprites/basic.png")
    for i in range(1, 9):
        sprites[f'grid{i}'] = pygame.image.load(f"sprites/grid_{i}.png")
    sprites['mine'] = pygame.image.load("sprites/bomb.png")
    sprites['mineClicked'] = pygame.image.load("sprites/bomb_clicked.png")
    return sprites

# ---------- Game Logic ----------
def generate_board(size, num_mines):
    # Generate board array and place mines with adjacent counts
    board = np.zeros((size, size), dtype=int)
    mines = np.random.choice(size * size, num_mines, replace=False)
    for idx in mines:
        x, y = divmod(idx, size)
        board[x, y] = -1  # Place mine
        for i in range(max(0, x - 1), min(size, x + 2)):
            for j in range(max(0, y - 1), min(size, y + 2)):
                if board[i, j] != -1:
                    board[i, j] += 1  # Increment adjacent mine count
    return board

def restart_game(num_mines):
    # Initialize a new game state
    board = generate_board(GRID_SIZE, num_mines)
    revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    flagged = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    start = True  # Indicates first click
    game_over = False
    return board, revealed, flagged, start, game_over

def reveal(board, revealed, x, y):
    # Reveal a cell recursively if it is empty
    if revealed[x, y] or board[x, y] == -1:
        return
    revealed[x, y] = True
    if board[x, y] == 0:
        for i in range(max(0, x - 1), min(GRID_SIZE, x + 2)):
            for j in range(max(0, y - 1), min(GRID_SIZE, y + 2)):
                if not revealed[i, j]:
                    reveal(board, revealed, i, j)

def flag(board, revealed, flagged, x, y):
    # Place or remove a flag on a cell
    if revealed[x, y]:
        return
    flagged[x, y] = not flagged[x, y]

# ---------- Draw Column/Row Labels ----------
def draw_labels(surface, fonts):
    # Draw column letters (A-J) and row numbers (1-10)
    col_labels = [chr(ord('A') + i) for i in range(GRID_SIZE)]
    for i, c in enumerate(col_labels):
        text = fonts['small'].render(c, True, BLACK)
        surface.blit(text, (MARGIN_LEFT + i * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2, MARGIN_TOP + GRID_SIZE * CELL_SIZE + 5))
    for i in range(GRID_SIZE):
        text = fonts['small'].render(str(i+1), True, BLACK)
        surface.blit(text, (MARGIN_LEFT - 25, MARGIN_TOP + i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2))

# ---------- Draw Board ----------
def draw_board(surface, board, revealed, flagged, sprites, fonts, status_text, num_mines, flag_count, restart_btn, quit_btn):
    # Draw all cells, flags, mines, numbers, grid lines, labels, and UI elements
    surface.fill(LIGHT_GRAY)
    rem_text = fonts['big'].render(f"Mines: {num_mines}", True, BLACK)
    remain_flags_text = fonts['small'].render(f"Flags left: {num_mines - flag_count}", True, BLACK)
    surface.blit(rem_text, (20, WINDOW_HEIGHT - 90))
    surface.blit(remain_flags_text, (20, WINDOW_HEIGHT - 60))
    status_render = fonts['big'].render(status_text, True, RED if "Game Over" in status_text else (GREEN if status_text == "Victory" else BLACK))
    surface.blit(status_render, (MARGIN_LEFT + BOARD_PIXELS//2 - status_render.get_width()//2, 20))
    hint = fonts['small'].render("Left-click: uncover  |  Right-click: flag  |  R: restart", True, BLACK)
    surface.blit(hint, (MARGIN_LEFT, WINDOW_HEIGHT - 30))

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
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
    draw_labels(surface, fonts)
    restart_btn.draw(surface)
    quit_btn.draw(surface)

# ---------- Main ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("EECS581 Project 1:Minesweeper")
    clock = pygame.time.Clock()

    # Initialize fonts
    small = pygame.font.Font(FONT_NAME, 22)
    big = pygame.font.Font(FONT_NAME, 36)
    fonts = {'small': small, 'big': big}

    # Load sprite images
    sprites = load_sprites()

    # Main menu buttons
    play_button = Button((WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 60, 200, 50), "Play Game", big)
    quit_button = Button((WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 10, 200, 50), "Quit", big)

    # Show menu
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
    mines = ask_mine_count(screen, clock, fonts)
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

    running = True
    while running:
        flag_count = np.sum(flagged)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Restart / Quit buttons
            if restart_btn.is_clicked(event):
                mines = ask_mine_count(screen, clock, fonts)
                pygame.event.clear()
                mines = clamp_mines(mines)
                board, revealed, flagged, start, game_over = restart_game(mines)
                status = "Playing"
                ignore_next_click = True
            if quit_btn.is_clicked(event):
                running = False

            # Restart with R key
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mines = ask_mine_count(screen, clock, fonts)
                pygame.event.clear()
                mines = clamp_mines(mines)
                board, revealed, flagged, start, game_over = restart_game(mines)
                status = "Playing"
                ignore_next_click = True

            # Game input
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                                    # Hit a mine -> game over
                                    revealed[:, :] = True
                                    status = "Game Over"
                                    game_over = True
                                else:
                                    reveal(board, revealed, x, y)
                        elif event.button == 3:  # Right-click to flag
                            if not revealed[x, y]:
                                flag(board, revealed, flagged, x, y)

        # Check for victory
        if not game_over and np.all(revealed | (board == -1)):
            status = "Victory"
            game_over = True

        draw_board(screen, board, revealed, flagged, sprites, fonts, status, mines, flag_count, restart_btn, quit_btn)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()
