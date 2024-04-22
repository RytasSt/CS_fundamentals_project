import pygame
from constants import *
from score import Highscore
from buttons import Button

class Gameover:
    """Represents gameover state/screen."""
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.back_button = Button(SCREEN_WIDTH // 2, 600, 200, 70, display, "Back")

    def run_level(self):
        """Starts off the state."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        text_info = font.render("Your castle has been destroyed!", True, WHITE)
        highscore = Highscore()
        highscore.get_last_line()
        score = highscore.extract_score()

        text_score = font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(text_info, (SCREEN_WIDTH // 2 - text_info.get_width() // 2, SCREEN_HEIGHT // 2 - text_info.get_height() // 2))
        self.screen.blit(text_score, (SCREEN_WIDTH // 2 - text_info.get_width() // 2, 50))
        
        if self.back_button.draw():
            self.gameStateManager.set_state('start_menu')

        