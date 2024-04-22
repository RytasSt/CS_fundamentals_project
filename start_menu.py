import pygame
from constants import *
from buttons import Button
import sys

class Start_menu:
    """Represents start menu state/screen."""
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.start_button = Button(300, SCREEN_HEIGHT // 2, 200, 70, display, "Start")
        self.exit_button = Button(600, SCREEN_HEIGHT // 2, 200, 70, display, "Exit")
        self.scores_button = Button(900, SCREEN_HEIGHT // 2, 200, 70, display, "Scores")

    def run_level(self):
        """Starts off the state."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Main menu", True, (255, 255, 255))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

        if self.start_button.draw():
            self.gameStateManager.set_state('level')
        if self.exit_button.draw():
            pygame.quit()
            sys.exit()
        if self.scores_button.draw():
            self.gameStateManager.set_state('results')