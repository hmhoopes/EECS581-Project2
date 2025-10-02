# Minesweeper Extension Architecture

## System Overview

This extension of Team 8's Minesweeper game adds sounds, an AI solver mode, and a turn-based player vs AI mode. 
The system is separated into modules containing the AIEngine class, board functions, utility functions, and other miscellaneous items.

### Technology Stack
- **Python 3.x** - Core language
- **Pygame** - Graphics and input handling
- **Numpy** - Board state management

## Key Components

### 1. Main function and program entrypoint (`product_2.py`)
**Responsibility**: Initialize necessary variables, run menu and game loops, handle user input

- Initializes pygame and other variables: the display, clock, fonts, sprites
- Runs menu loop that renders menu and buttons; handles user input
- Based on user input, initializes the AI and board components
- Runs main game loop that displays board, handles user input, makes AI turn if necessary, and handles win and lose conditions

### 2. AI Engine (`ai.py`)
**Responsibility**: Store AI state and handle AI moves

- Easy difficulty chooses a random unrevealed cell.
- Medium difficulty chooses the unrevealed cell with the lowest probability of containing a mine
- Hard difficulty randomly chooses an unrevealed cell that is guaranteed to have no mine.

The class is initialized by passing in the difficulty level in as an argument at initialization.
The AI makes a move by calling the function corresponding to the difficulty level set. 

```python
class AIEngine:
    def make_move(self, board: np.ndarray, revealed: np.ndarray):
        """
        Function that makes a move on the board
        Args:
            board (np.ndarray): The minesweeper board.
            revealed (np.ndarray): An array of bools that represents squares on the board that have been revealed.
        """
        match self.difficulty:
            case AIDifficulty.Easy:
                return self._make_easy_move(board, revealed)

            case AIDifficulty.Medium:
                return self._make_medium_move(board, revealed)

            case AIDifficulty.Hard:
                return self._make_hard_move(board, revealed)
```

### 3. Board functions (`board_functions.py`)
**Purpose**: Store functions related to board use.

Functions:
- `generate_board(size, num_mines)`: Generate board array and place mines with adjacent counts.
- `play_music(music_file, volume = 0.1)`: Load in and play music specified in `music_file`
- `reveal(board, revealed, x, y)`: Reveal a cell recursively if it is empty.
- `flag(board, revealed, flagged, x, y)`: Place or remove a flag on a cell.
- `draw_board(surface, board, revealed, flagged, sprites, fonts, status_text, num_mines, flag_count, restart_btn, quit_btn)`: Draw all cells, flags, mines, numbers, grid lines, labels, and UI elements.
- `restart_game(num_mines)`: Initialize a new game state.

### 4. Utility functions (`utility_functions.py`)
**Purpose**: Store miscellaneous functions.

Functions:
- `def clamp_mines(n: int)`: Clamp mine number to allowed range (10-20).
- `initialize_game(screen, clock, fonts)`: Allow user to choose mine count and AI mode before starting game using a slider UI.
- `load_sprites()`: Load all game sprite images from the sprites/ directory.
- `draw_labels(surface, fonts)`: Draw column letters (A-J) and row numbers (1-10) on the board.

### 5. Button Class (`button.py`)
**Purpose**: Provides class for button functionality.

- Contains function that draws itself
- Contains function that returns `true` if it is clicked

### 6. Slider Class (`slider.py`)
**Purpose**: Provides class for slider functionality(slider used when choosing number of mines).

- Contains function to draw itself
- Contains function to handle user manipulation of slider

### 7. Constants File (`constants.py`)
**Purpose**: Store constants to be used throughout the program.

- Stores screen width and height variables
- Stores color variables
- Stores board size variables
- Stores file paths for sounds
- Stores enums that represent AIDifficulty and AIMode:

## Key Data Structures:
### AIDifficulty and AIMode Enums:
```python
class AIDifficulty(Enum):
    Easy = 1
    Medium = 2
    Hard = 3

class AIMode(Enum):
    Off = 1
    Alternate = 2
    Solver = 3
```
### Slider class core data:
```python
class Slider:
    self.rect = pygame.Rect(x, y, w, 6)
    self.knob_x = x + int((start_val - min_val) / (max_val - min_val) * w)
    self.min_val = min_val
    self.max_val = max_val
    self.value = start_val
    self.font = font
    self.dragging = False
```
### Button class core data:
```python
class Button:
    self.rect = pygame.Rect(rect)
    self.text = text
    self.font = font
    self.color = color
    self.hover_color = hover_color
    self.text_color = text_color
```

## Project Structure
```
EECS 581 - Project 2
├── ai.py               # AIEngine 
├── board_functions.py  # Miscellaneous board functions
├── button.py           # Button class
├── constants.py        # All constants
├── new-docs/           # Our team docs
├── old-team-docs/      # Previous team docs
├── product_2.py        # Main entry point
├── readme.md           # Previous team readme
├── requirements.txt
├── slider.py           # Slider class
├── sounds/
│   ├── [game sounds]
├── sprites/
│   ├── [game sprites]
└── utility_functions.py
```