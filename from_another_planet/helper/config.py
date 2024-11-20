import random
import math

import pygame
from pygame.locals import *

from from_another_planet import *


def text(content, x, y, font=font, sm_font=sm_font, color=color, small=False):
    if small:
        text = sm_font.render(content, True, color)
        window.blit(text, (x, y))
    else: 
        text = font.render(content, True, color)
        window.blit(text, (x, y))


def hide_cursor():
    pygame.mouse.set_visible(False)

def show_cursor():
    pygame.mouse.set_visible(False)
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(cursor, pos)

def change_cursor():
    pygame.mouse.set_visible(False)
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(crosshair, pos)

def teleport_cursor():
    pygame.mouse.set_visible(False)
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(tp_cursor, pos)


def change_level(game_vars):
    game_vars.lvl += 1
    game_vars.NUM_ALIENS += 1
    game_vars.NUM_BLUE_ALIENS += 1
    
    MAX_SHOOTING_ALIENS_LVL_3 = 4
    MAX_SHOOTING_ALIENS_LVL_5 = 8
    MAX_BLUE_ALIENS = 5
    MAX_BIG_ALIENS = 10

    if game_vars.lvl > 8:
        game_vars.NUM_SHOOTING_ALIENS += 2
        game_vars.NUM_BLUE_ALIENS += 2
        game_vars.NUM_BIG_ALIENS += 2
    elif game_vars.lvl > 3:
        game_vars.NUM_SHOOTING_ALIENS += 1

    if game_vars.lvl > 4 and game_vars.NUM_SHOOTING_ALIENS > MAX_SHOOTING_ALIENS_LVL_5:
        game_vars.NUM_SHOOTING_ALIENS = MAX_SHOOTING_ALIENS_LVL_5
    elif game_vars.lvl > 3 and game_vars.NUM_SHOOTING_ALIENS > MAX_SHOOTING_ALIENS_LVL_3:
        game_vars.NUM_SHOOTING_ALIENS = MAX_SHOOTING_ALIENS_LVL_3

    if game_vars.lvl > 4 and game_vars.NUM_BLUE_ALIENS > MAX_BLUE_ALIENS:
         game_vars.NUM_BLUE_ALIENS = MAX_BLUE_ALIENS
    
    if game_vars.lvl > 4 and game_vars.NUM_BIG_ALIENS > MAX_BIG_ALIENS:
        game_vars.NUM_BIG_ALIENS = MAX_BIG_ALIENS


def reduce_life_edge(player, alien_type, alien_list):
    if player.lives > 0:
        if alien_type.rect.x + alien_type.image.get_width() < 64:
            player.lives -= 1
            alien_list.remove(alien_type)


def add_alien(alien_type, sprite, num, alien_list):
    for _ in range(num):
        valid = False
        while not valid:
            x = (random.randint(window.get_width()+200, window.get_width()+400))
            y = (random.randint(100, window.get_height()-120))
            valid = True
            for alien in alien_list:
                if abs(x - alien.rect.x) < 50 and abs(y - alien.rect.y) < 50:
                    valid = False
                    break
        alien = alien_type(sprite, x, y)
        alien_list.append(alien)

def add_rocks(num, rock_class, sprites, rock_list, min_speed, max_speed):
    for _ in range(num):
        x = random.choice([random.randint(-500, -100), 
                           random.randint(window.get_width() + 100, window.get_width() + 500)])
        y = random.choice([random.randint(window.get_height() + 100, window.get_height() + 500),
                           random.randint(-500, -100)])
        rock = rock_class(sprites, x, y, random.randint(min_speed, max_speed))
        rock_list.append(rock)


def proximity_sound(player, item, channel, sound, proximity_range=500):
    player_distance = abs(item.rect.x - player.rect.x)
    
    if player_distance < proximity_range:
        vol = max(0.05, min(2.0, 2.0 - (player_distance / proximity_range)))
        channel.set_volume(vol)
        if not channel.get_busy():
            channel.play(sound, fade_ms=1000)
    else:
        if channel.get_busy():
            channel.fadeout(1000)