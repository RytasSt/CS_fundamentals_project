import pygame
from constants import *
from buttons import Button
import sys
from score import Highscore

class Results:
    def __init__(self, display, gameStateManager):
        self.screen = display
        self.gameStateManager = gameStateManager
        self.back_button = Button(SCREEN_WIDTH // 2, 600, 200, 70, display, "Back")

    def run_level(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Highscore list", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

        font_score = pygame.font.SysFont(None, 16)
        highscore = Highscore()
        score_list = highscore.get_last_scores(10)
        
        for i, score in enumerate(score_list):
            text_score = font_score.render(score[:-1], True, WHITE)
            self.screen.blit(text_score, (250, 120 + (i * 50)))

        if self.back_button.draw():
            self.gameStateManager.set_state('start_menu')
