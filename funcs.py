import random
import math

import pygame
from pygame.locals import *

from assets import *


def text(content, x, y, font=font, sm_font=sm_font, color=color, small=False):
    if small:
        text = sm_font.render(content, True, color)
        window.blit(text, (x, y))
    else: 
        text = font.render(content, True, color)
        window.blit(text, (x, y))

def hide_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))


def show_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(cursor, pos)


def change_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(crosshair, pos)


def teleport_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(tp_cursor, pos)


def change_level(game_variables):
    game_variables.lvl += 1
    game_variables.NUM_ALIENS += 1
    game_variables.NUM_BLUE_ALIENS += 1

    if game_variables.lvl > 2:
        game_variables.NUM_SHOOTING_ALIENS += 2
        if game_variables.NUM_SHOOTING_ALIENS > 6:
            game_variables.NUM_SHOOTING_ALIENS = 3

    if game_variables.lvl > 4:
        game_variables.NUM_BIG_ALIENS += 2
        if game_variables.NUM_BIG_ALIENS > 6:
            game_variables.NUM_BIG_ALIENS = 2


def add_alien(alien_type, num, alien_list):
    for _ in range(num):
        min_pos=(random.randint(window.get_width()+200, window.get_width()+400))
        max_pos=(random.randint(100, window.get_height()-120))
        alien = alien_type(min_pos, max_pos)
        alien_list.append(alien)


def add_rocks(num, rock_class, rock_list, min_speed, max_speed):
    for _ in range(num):
        x = random.choice([random.randint(-window.get_width()+200, -window.get_width()+800), random.randint(window.get_width()+200, window.get_width()+800)])
        y = random.choice([random.randint(window.get_height()+200, window.get_height()+800), random.randint(-window.get_height()+200, -window.get_height()+800)])
        rock = rock_class(x, y, random.randint(min_speed, max_speed))
        rock_list.append(rock)


def bullet_check(bullet_list):
    if not len(bullet_list) == 0:
        bullet_list[:] = [bullet for bullet in bullet_list if bullet.rect.x >= 0 and bullet.rect.x <= window.get_width() and bullet.rect.y >= 60 and bullet.rect.y <= window.get_height()-60]


def shoot(bullet_class, player, alien, bullet_list, bullet_type='bullet'):
    
    if bullet_type == 'enemy': 
        freq = random.randint(15, 40)
        pX, pY = player.rect.x, player.rect.y

        distanceX = pX - alien.rect.x
        distanceY = pY - alien.rect.y
        angle = math.atan2(distanceY, distanceX)
        speedX = int(10 * math.cos(angle))
        speedY = int(10 * math.sin(angle))

        if alien.rate == 0:
            alien.rate = freq
            bullet_list.append(bullet_class(alien.rect.centerx, alien.rect.centery, speedX, speedY))

    elif bullet_type == 'bullet':
        sX, sY = pygame.mouse.get_pos()

        distanceX = sX - player.rect.x
        distanceY = sY - player.rect.y
        angle = math.atan2(distanceY, distanceX)

        speedX = int(16 * math.cos(angle))
        speedY = int(16 * math.sin(angle))

        if player.rate == 0:
            player.rate = 15
            bullet = bullet_class(player.rect.centerx, player.rect.centery, speedX, speedY)
            bullet.rotate(angle)
            bullet_list.append(bullet)

    elif bullet_type == 'shotgun':
        sX, sY = pygame.mouse.get_pos()

        distanceX = sX - player.rect.x
        distanceY = sY - player.rect.y
        angle = math.atan2(distanceY, distanceX) + ((7/12)*math.pi/2)


        if player.gun:
            if player.srate == 0:
                player.srate = 300

                for _ in range(7):
                    speedX = int(14 * math.cos(angle))
                    speedY = int(14 * math.sin(angle))

                    shell = bullet_class(player.rect.centerx, player.rect.centery, speedX, speedY, angle)
                    shell.rotate(angle)
                    angle -= 0.3

                    bullet_list.append(shell)
