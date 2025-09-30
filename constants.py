from enum import Enum
############################################################
# Configuration Constants
############################################################
GRID_SIZE = 10  # Number of rows/columns
CELL_SIZE = 40  # Pixel size of each cell
MARGIN_LEFT = 80  # Left margin for board
MARGIN_TOP = 60  # Top margin for board
WINDOW_PADDING = 20  # Padding around window
FONT_NAME = None  # Default font
FPS = 60  # Frames per second

############################################################
# AI Modes
############################################################
class AIDifficulty(Enum):
    Easy = 1
    Medium = 2
    Hard = 3

class AIMode(Enum):
    Off = 1
    Alternate = 2
    Solver = 3

############################################################
# Sound files
# converted mp3 to ogg since pygame has a harder time loading mp3
############################################################
START_MUSIC_1 = 'sounds/ssbm_opening_theme.ogg'         # temp patch to allow running on linux
START_MUSIC_2 = 'sounds/kirby_adventure_nes.ogg'        # temp patch to allow running on linux
START_MUSIC_3 = 'sounds/c418_minecraft.ogg'             # temp patch to allow running on linux
LOSE_MUSIC = 'sounds/womp_womp_womp.ogg'                # temp patch to allow running on linux
WIN_MUSIC = 'sounds/yoshi_happy_song.ogg'               # temp patch to allow running on linux

############################################################
#sound effects
#converted mp3 to wav so it would work with pygame
############################################################
SOUND_MINE_REVEAL = 'sounds/explosion.wav'              # temp patch to
SOUND_FLAG_PLACE = 'sounds/flag_remove.wav'              # temp patch to allow running on linux
SOUND_FLAG_REMOVE = 'sounds/flag_place.wav'            # temp patch to allow running
SOUND_CELL_REVEAL = 'sounds/reveal.wav'                 # temp patch to allow running on linux
SOUND_BUTTON_CLICK = 'sounds/button-click.wav'          # temp patch to allow running on


# Colors
############################################################
# Color Definitions
############################################################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
LIGHT_GRAY = (240, 240, 240)
RED = (200, 40, 40)
GREEN = (40, 160, 40)
BLUE = (30, 60, 220)

# Game-specific colors
############################################################
# Game-specific Color Definitions
############################################################
BG_COLOR = (200, 200, 200)
GRID_COLOR = (100, 100, 100)  # Color of grid lines
REVEALED_COLOR = (220, 220, 220)  # Color for revealed cells
MINE_COLOR = (20, 20, 20)
TEXT_COLOR = (0, 0, 0)
FLAG_COLOR = (255, 0, 0)

# Derived sizes
############################################################
# Derived Size Calculations
############################################################
BOARD_PIXELS = GRID_SIZE * CELL_SIZE
WINDOW_WIDTH = MARGIN_LEFT + BOARD_PIXELS + WINDOW_PADDING + 100
WINDOW_HEIGHT = MARGIN_TOP + BOARD_PIXELS + WINDOW_PADDING + 200