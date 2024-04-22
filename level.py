import pygame
from pygame.rect import Rect
from pygame.surface import Surface
import requests

import os
import sys
import time
import random
from constants import *
from sprite_sheet import Sprite_sheet
import score

class Level:
    def __init__(self, screen, game_state_manager, random_words):
        self.screen = screen
        self.game_state_manager = game_state_manager
        self.clock = pygame.time.Clock()
        self.score = 0

        self.random_words = random_words
        self.base_font = pygame.font.SysFont("bahnschrift", 32, False, False)
        self.enemy_font = pygame.font.SysFont("arial", 24)

        # Sprites
        self.sprite_sheet_image = pygame.image.load('sprites\enemy.png').convert_alpha()
        self.sprite_sheet = Sprite_sheet(self.sprite_sheet_image)
        self.castle_sheet_image = pygame.image.load(os.path.join('sprites', 'tiles.png')).convert_alpha()
        self.castle_sheet = Sprite_sheet(self.castle_sheet_image)
        self.enemy_list = []
        
        self.castle = Castle(0, 500, 1280, 70, 3)
        self.players_input = Players_input(540, 650, self.screen)
        self.hp_bar = Health_bar(90, 580, 1100, 20, 100)

        self.last_enemy_spawn = pygame.time.get_ticks()
        self.spawn_speed = 4000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.players_input.render_text(self.base_font, self.screen).collidepoint(event.pos):
                    self.players_input.active = True
                else:
                    self.players_input.active = False
            
            if event.type == pygame.KEYDOWN:
                if self.players_input.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        self.players_input.user_text = self.players_input.user_text[:-1]
                    elif len(self.players_input.user_text) < 15:
                        self.players_input.user_text += event.unicode

                    if event.key == pygame.K_RETURN:
                        self.players_input.user_text = self.players_input.user_text[:-1]
                        for enemy in self.enemy_list:
                            if enemy.enemy_text == self.players_input.user_text:
                                enemy.visible = False
                                self.score += 1
                                if len(self.enemy_list) > 10:
                                    self.enemy_list.pop(0)

                        self.players_input.user_text = ""


    def create_enemies(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn >= self.spawn_speed:
            if self.spawn_speed > 2000:
                self.spawn_speed -= 100
            lanes = [
                random.randint(80, 236),
                random.randint(306, 472),
                random.randint(553, 728),
                random.randint(808, 984),
                random.randint(1064, 1200)
            ]
            x = random.choice(lanes)
            enemy_text = f"{random.choices(self.random_words)[0]}"
            enemy = Enemy(x, 0, 1, self.screen, self.sprite_sheet, enemy_text)
            self.enemy_list.append(enemy)
            self.last_enemy_spawn = current_time

    def gameplay_loop(self):
        self.screen.fill(BLACK)
        self.castle.draw_castle(self.screen, self.castle_sheet)
        self.hp_bar.draw(self.screen)

        self.create_enemies()
        for enemy in self.enemy_list:
            enemy_animation_list = enemy.get_animation_list()
            enemy.draw_sprite(enemy_animation_list)
            enemy.move_to_castle()
            enemy.render_enemy_text(self.enemy_font)
            enemy.attack_castle(self.hp_bar)

        self.players_input.render_text(self.base_font, self.screen)
        if self.hp_bar.hp <= 0:
            score.Highscore.save_results(self.score)
            self.game_state_manager.set_state('gameover')

        self.clock.tick(FPS)
        
    # RUN LEVEL 
    def run_level(self):
        self.gameplay_loop()
        self.handle_events()
        

class Castle:
    def __init__(self, x: int, y: int, width: int, height: int, scale: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = scale

    def draw_castle(self, screen, sheet):
        tile_3 = sheet.get_image(self.scale, 16, 16, 3, BLACK)
        for i in range(27):
            screen.blit(tile_3, (self.x + (i * 16 * self.scale), self.y))
            

class Players_input:
    def __init__(self, input_box_x: int, input_box_y: int, screen):
        self.user_text = ""
        self.input_box_x = input_box_x
        self.input_box_y = input_box_y
        self.input_box_width = 150
        self.active = True
        self.box_color = ""

    def render_text(self, font, screen) -> Rect:
        text_surface = font.render(self.user_text, True, WHITE)
        text_width = text_surface.get_width()

        new_box_width = max(150, text_width + 20)
        delta_box_width = new_box_width - self.input_box_width
        self.input_box_width = new_box_width
        self.input_box_x -= delta_box_width // 2

        screen.blit(text_surface, (self.input_box_x + 10, self.input_box_y + 5))
        if self.active == True:
            self.box_color = HONEY
            if len(self.user_text) >= 15:
                self.box_color = "red"
        else:
            self.box_color = SILVER

        return pygame.draw.rect(screen, self.box_color, (self.input_box_x, self.input_box_y, self.input_box_width, 60), 2)
        

class Enemy:
    def __init__(self, x: int, y: int, speed: int, screen: Surface, sprite_sheet, enemy_text):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.speed = speed
        self.enemy_text = enemy_text
        self.visible = True
        self.last_attack_time = 0
        self.screen = screen
        self.cooldown = 0
        self.frame = 0
        self.sprite_sheet = sprite_sheet
        self.frame_death = self.sprite_sheet.get_image(3, self.width, self.height, 3, BLACK)
        self.last_update = pygame.time.get_ticks()


    def get_animation_list(self):
        animation_list = []
        animation_steps = 3
        self.cooldown = 500

        for n in range(animation_steps):
            animation_list.append(self.sprite_sheet.get_image(n, self.width, self.height, 3, BLACK))

        return animation_list

    def draw_sprite(self, animation_list):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(animation_list):
                self.frame = 0

        if self.visible:
            self.screen.blit(animation_list[self.frame], (self.x, self.y))
        else:
            self.screen.blit(self.frame_death, (self.x, self.y))

    def move_to_castle(self) -> None:
        if self.y < 490 and self.visible == True:
            self.y += self.speed 

    def render_enemy_text(self, font) -> None:
        if self.visible:
            text_surface = font.render(self.enemy_text, True, WHITE)
            self.screen.blit(text_surface, (self.x - 15, self.y - 25))

    def attack_castle(self, hp_bar) -> None:
        if self.y >= 490 and hp_bar.hp > 0 and self.visible == True:
            hp_bar.hp -= 20
            self.visible = False


class Health_bar:
    def __init__(self, x: int, y: int, w: int, h: int, max_hp: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface: Surface) -> None:
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))