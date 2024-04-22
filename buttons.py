import pygame
from constants import *

class Button:
    def __init__(self, x, y, width, height, screen, button_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.button_text = button_text
        self.pressed = False

    def draw(self):
        action = False

        font = pygame.font.SysFont(None, 52)
        text = font.render(self.button_text, True, WHITE)
        start_button = pygame.draw.rect(self.screen, "darkorange", (self.x, self.y, self.width, self.height))
        self.screen.blit(text, (self.x + 10, self.y + 15))

        pos = pygame.mouse.get_pos()

        if start_button.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False

        return action


