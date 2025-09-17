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

BG_COLOR = (200, 200, 200)
GRID_COLOR = (100, 100, 100)
REVEALED_COLOR = (220, 220, 220)
MINE_COLOR = (20, 20, 20)
TEXT_COLOR = (0, 0, 0)
FLAG_COLOR = (255, 0, 0)

# Derived sizes
BOARD_PIXELS = GRID_SIZE * CELL_SIZE
WINDOW_WIDTH = MARGIN_LEFT + BOARD_PIXELS + WINDOW_PADDING
WINDOW_HEIGHT = MARGIN_TOP + BOARD_PIXELS + WINDOW_PADDING + 80

# ---------- Clamp ----------
def clamp_mines(n: int) -> int:
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
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(surface, self.hover_color if is_hover else self.color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
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
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.circle(surface, BLUE, (self.knob_x, self.rect.centery), 12)
        val_surf = self.font.render(f"{self.value}", True, BLACK)
        surface.blit(val_surf, (self.rect.centerx - val_surf.get_width() // 2, self.rect.top - 35))

# ---------- Ask for mine count with slider ----------
def ask_mine_count(screen, clock, fonts):
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

# ---------- Game Logic ----------
def generate_board(size, num_mines):

    #start with 0 grid (occupancy grid for mines)
    board = np.zeros((size, size), dtype=int)

    #random indices for mines
    mines = np.random.choice(size * size, num_mines, replace=False)

    #iterate through mines and place a mine in each index
    for idx in mines:

        #get x y from just index. basically division with a remainder
        x, y = divmod(idx, size)

         #place mine
        board[x, y] = -1

        #adjacent mine counter
        for i in range(max(0, x - 1), min(size, x + 2)):
            for j in range(max(0, y - 1), min(size, y + 2)):
                if board[i, j] != -1:
                    board[i, j] += 1 #add when its an empty cell
    return board

def restart_game(num_mines):
    board = generate_board(GRID_SIZE, num_mines)
    revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    flagged = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    start = True
    game_over = False
    return board, revealed, flagged, start, game_over

def reveal(board, revealed, x, y):
    if revealed[x, y] or board[x, y] == -1:
        return
    
    #set x y to revealed
    revealed[x, y] = True

    #recursively reveal if empty cell (No adjacent mines)
    if board[x, y] == 0:
        for i in range(max(0, x - 1), min(GRID_SIZE, x + 2)):
            for j in range(max(0, y - 1), min(GRID_SIZE, y + 2)):
                if not revealed[i, j]:
                    reveal(board, revealed, i, j)

def flag(board, revealed, flagged, x, y):
    if revealed[x, y]:
        #return if cell is revealed
        return
    flagged[x, y] = not flagged[x, y]

def draw_board(surface, board, revealed, flagged, fonts, status_text: str, num_mines, flag_count):
    surface.fill(LIGHT_GRAY)
    font = fonts['small']

    rem_text = fonts['big'].render(f"Mines: {num_mines}", True, BLACK)
    remain_flags_text = font.render(f"Flags left: {num_mines - flag_count}", True, BLACK)
    surface.blit(rem_text, (20, WINDOW_HEIGHT - 70))
    surface.blit(remain_flags_text, (20, WINDOW_HEIGHT - 40))

    status_render = fonts['big'].render(
        status_text,
        True,
        RED if "Loss" in status_text else (GREEN if status_text == "Victory" else BLACK),
    )
    surface.blit(status_render, (MARGIN_LEFT + BOARD_PIXELS - 220, WINDOW_HEIGHT - 60))

    hint = font.render("Left-click: uncover  |  Right-click: flag  |  R: restart", True, BLACK)
    surface.blit(hint, (MARGIN_LEFT, WINDOW_HEIGHT - 30))

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(MARGIN_LEFT + y * CELL_SIZE, MARGIN_TOP + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[x, y]:
                pygame.draw.rect(surface, REVEALED_COLOR, rect)
                if board[x, y] == -1:
                    pygame.draw.circle(surface, MINE_COLOR, rect.center, CELL_SIZE // 3)
                elif board[x, y] > 0:
                    text = fonts['small'].render(str(board[x, y]), True, TEXT_COLOR)
                    surface.blit(text, text.get_rect(center=rect.center))
            elif flagged[x, y]:
                pygame.draw.circle(surface, FLAG_COLOR, rect.center, CELL_SIZE // 3)
            else:
                pygame.draw.rect(surface, BG_COLOR, rect)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

# ---------- Main ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    small = pygame.font.Font(FONT_NAME, 22)
    big = pygame.font.Font(FONT_NAME, 36)
    fonts = {'small': small, 'big': big}

    play_button = Button((WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 60, 200, 50), "Play Game", big)
    quit_button = Button((WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 10, 200, 50), "Quit", big)

    # ---------- Menu ----------
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

    # ---------- Start Game ----------
    mines = ask_mine_count(screen, clock, fonts)
    mines = clamp_mines(mines)
    board, revealed, flagged, start, game_over = restart_game(mines)
    status = "Playing"

    running = True
    while running:
        flag_count = np.sum(flagged)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Restart
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mines = ask_mine_count(screen, clock, fonts)
                mines = clamp_mines(mines)
                board, revealed, flagged, start, game_over = restart_game(mines)
                status = "Playing"

            elif not game_over:
                # Left click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    x = (my - MARGIN_TOP) // CELL_SIZE
                    y = (mx - MARGIN_LEFT) // CELL_SIZE
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if start:
                            while board[x, y] == -1:
                                board = generate_board(GRID_SIZE, mines)
                            reveal(board, revealed, x, y)
                            start = False
                        else:
                            if board[x, y] == -1:
                                revealed[:, :] = True
                                status = "Loss"
                                game_over = True
                            else:
                                reveal(board, revealed, x, y)

                # Right click
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mx, my = pygame.mouse.get_pos()
                    x = (my - MARGIN_TOP) // CELL_SIZE
                    y = (mx - MARGIN_LEFT) // CELL_SIZE
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if not revealed[x, y]:
                            flag(board, revealed, flagged, x, y)

        # Check win
        if not game_over and np.all(revealed | (board == -1)):
            status = "Victory"
            game_over = True

        draw_board(screen, board, revealed, flagged, fonts, status, mines, flag_count)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()
