import pygame
import sys
from game_state_manager import GameStateManager
import requests

from level import Level
from gameover import Gameover
from start_menu import Start_menu
from results import Results
from constants import *


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    while True:
        try:
            r = requests.get('https://random-word-api.vercel.app/api?words=200')
            random_words = r.json()
            words_under_n_letters = []
            for word in random_words:
                if len(word) < 12:
                    words_under_n_letters.append(word)
            break
        except requests.exceptions.Timeout:
            print("Retrying API request...")
        except Exception as e:
            raise(e)

    game_state_manager = GameStateManager('start_menu')
    level = Level(screen, game_state_manager, words_under_n_letters)
    start_menu = Start_menu(screen, game_state_manager)
    gameover = Gameover(screen, game_state_manager)
    results = Results(screen, game_state_manager)

    states = {'start_menu': start_menu, 'level': level, "gameover": gameover, "results": results}

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