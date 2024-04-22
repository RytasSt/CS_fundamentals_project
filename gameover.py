import pygame
from constants import *

class Gameover:
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager

    def run_level(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Your castle has been destroyed!", True, (255, 255, 255))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        