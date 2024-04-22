import pygame
from constants import *
from buttons import Button
import sys

class Start_menu:
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.start_button = Button(300, SCREEN_HEIGHT // 2, 200, 70, display, "Start")
        self.exit_button = Button(600, SCREEN_HEIGHT // 2, 200, 70, display, "Exit")
        self.results_button = Button(900, SCREEN_HEIGHT // 2, 200, 70, display, "High score")

    def run_level(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Main menu", True, (255, 255, 255))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

        if self.start_button.draw():
            self.gameStateManager.set_state('level')
        if self.exit_button.draw():
            pygame.quit()
            sys.exit()
        if self.results_button.draw():
            print("results")


        