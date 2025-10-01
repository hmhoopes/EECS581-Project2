import pygame
from constants import *
from enum import Enum
import numpy as np
import random
from board_functions import reveal

class AIEngine:
    def __init__(self, difficulty: AIDifficulty):
        """
        AIEngine class to store methods and attributes 
        Args:
            difficulty (AIDifficulty): difficulty mode of ai, either AIDifficulty.Easy, AIDifficulty.Medium, or AIDifficulty.Hard
        """
        self.difficulty: AIDifficulty = difficulty
    
    def set_difficulty(self, difficulty: AIDifficulty):
        self.difficulty = difficulty
    
    def make_move(self, board: np.ndarray, revealed: np.ndarray):
        """
        Function that makes a move on the board
        Args:
            board (np.ndarray): The minesweeper board (their implementation is board is calculated when game is started 
                                and uses -1 to represent mines, 0 to represent blank squares, and integers to 
                                represent how many adjacent mines a square has)

            revealed (np.ndarray): An array of bools that represents squares on the board that have been revealed.
                                    Their implementation is a square is True if revealed or False if not.
        """
        match self.difficulty:
            case AIDifficulty.Easy:
                return self._make_easy_move(board, revealed)

            case AIDifficulty.Medium:
                return self._make_medium_move(board, revealed)

            case AIDifficulty.Hard:
                return self._make_hard_move(board)

    def _make_easy_move(self, board: np.ndarray, revealed: np.ndarray):
        # get indices where revealed==false, those are squares ai can choose
        unrevealed_indices = np.where(revealed == False)
        row_indices, col_indices = unrevealed_indices # unpack to get indiv row and col indices
        # zip row and col indices together to get list of coord pairs of unrevealed squares
        unrevealed_coords = list(zip(row_indices, col_indices))
        # make random choice for which square to reveal
        ai_coord_choice = random.choice(unrevealed_coords)
        x, y = ai_coord_choice
        # return ai's x and y cell choice
        return x, y




    def _make_medium_move(self, board: np.ndarray, revealed: np.ndarray):
        safe_move = self._find_safe_move(board, revealed)
        if safe_move:
            return safe_move

        unrevealed_indices = np.where(revealed == False)
        unrevealed_coords = list(zip(*unrevealed_indices))
        x, y = random.choice(unrevealed_coords)
        return x, y

    def _find_safe_move(self, board: np.ndarray, revealed: np.ndarray):
        size = board.shape[0]

        low_probability = float('inf')
        low_probability_indicie = None

        for x in range(size):
            for y in range(size):
                if revealed[x, y]:
                    continue

                max_probability = 0

                for i in range(max(0, x - 1), min(size, x + 2)):
                    for j in range(max(0, y - 1), min(size, y + 2)):
                        if not revealed[i, j] or board[i, j] <= 0:
                            continue

                        unrevealed_count = 0
                        for ii in range(max(0, i - 1), min(size, i + 2)):
                            for jj in range(max(0, j - 1), min(size, j + 2)):
                                if not revealed[ii, jj]:
                                    unrevealed_count += 1

                        if unrevealed_count > 0:
                            probability = board[i, j] / unrevealed_count
                            max_probability = max(max_probability, probability)

                if max_probability == 0:
                    return (x, y)

                if max_probability > 0 and max_probability < low_probability:
                    low_probability = max_probability
                    low_probability_indicie = (x, y)

        return low_probability_indicie

    def _make_hard_move(self, board: np.ndarray, revealed: np.ndarray):
        unrevealed_indices = np.where(revealed == False)
        unrevealed_coords = list(zip(*unrevealed_indices))

        safe_coords = [(x, y) for x, y in unrevealed_coords if board[x, y] != -1]

        if safe_coords:
            x, y = random.choice(safe_coords)
            return x, y

        x, y = random.choice(unrevealed_coords)
        return x, y