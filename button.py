import pygame
#from effects import EffectManager
from constants import *
pygame.init()
button_click_sound = pygame.mixer.Sound(SOUND_BUTTON_CLICK)

# ---------- Button Helper ----------
############################################################
# Button Helper Class
############################################################
class Button:
    """
    UI Button for menu and game controls.
    Args:
        rect (tuple): Button rectangle (x, y, w, h)
        text (str): Button label
        font (pygame.font.Font): Font object
        color, hover_color, text_color: Color settings
    """
    def __init__(self, rect, text, font, color=GRAY, hover_color=DARK_GRAY, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        """Draw button with hover effect."""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        # Change color if mouse is hovering
        pygame.draw.rect(surface, self.hover_color if is_hover else self.color, self.rect, border_radius=6)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        # Center the text on the button
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Return True if button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                button_click_sound.play()
                return True
        return False