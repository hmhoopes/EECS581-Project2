"""
Minesweeper Slider Module

Module Name: slider.py
Description: Defines Slider class for Minesweeper UI. Includes functions for
             drawing and handling sliding event.

Inputs:
    - Slider x, y, width, min_val, max_val, start_val, and font
    - User click positions checked against slider hitbox

Outputs:
    - Slider class that provides attributes for rendering and interaction

External Sources:
    - Pygame library for rendering and handling user events

Author: Team 8
Creation Date: 9/24/2025
"""
import pygame
from constants import *

# ---------- Slider Helper ----------
############################################################
# Slider Helper Class
############################################################
class Slider:
    """
    UI Slider for selecting mine count.
    Args:
        x, y (int): Position
        w (int): Width
        min_val, max_val, start_val (int): Value range
        font (pygame.font.Font): Font object
    """
    def __init__(self, x, y, w, min_val, max_val, start_val, font):
        self.rect = pygame.Rect(x, y, w, 6)
        self.knob_x = x + int((start_val - min_val) / (max_val - min_val) * w)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.font = font
        self.dragging = False

    def handle_event(self, event):
        """Handle mouse and keyboard input for slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.knob_x) < 15 and abs(event.pos[1] - self.rect.centery) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Move knob horizontally within slider bounds
            self.knob_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            ratio = (self.knob_x - self.rect.left) / self.rect.width
            # Update value based on knob position
            self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Decrease value with left arrow
                self.value = max(self.min_val, self.value - 1)
            elif event.key == pygame.K_RIGHT:
                # Increase value with right arrow
                self.value = min(self.max_val, self.value + 1)
            # Move knob to match new value
            self.knob_x = self.rect.left + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)

    def draw(self, surface):
        """Draw slider track and knob."""
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.circle(surface, BLUE, (self.knob_x, self.rect.centery), 12)
        val_surf = self.font.render(f"{self.value}", True, BLACK)
        surface.blit(val_surf, (self.rect.centerx - val_surf.get_width() // 2, self.rect.top - 35))