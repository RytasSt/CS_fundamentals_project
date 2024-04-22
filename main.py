import pygame
import sys
from game_state_manager import GameStateManager
import requests


from level import Level
# from menu import Menu
from gameover import Gameover
from start_menu import Start_menu



pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    r = requests.get('https://random-word-api.vercel.app/api?words=100')
    random_words = r.json()

    game_state_manager = GameStateManager('start_menu')

    level = Level(screen, game_state_manager, random_words)
    start_menu = Start_menu(screen, game_state_manager)
    gameover = Gameover(screen, game_state_manager)

    states = {'start_menu': start_menu, 'level': level, "gameover": gameover}


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        states[game_state_manager.get_state()].run_level()
        pygame.display.update()


if __name__ == "__main__":
    main()