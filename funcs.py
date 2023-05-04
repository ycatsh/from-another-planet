import pygame
from pygame.locals import *
from assets import *
import random
import math


def text(content, x, y, font=font, sm_font=sm_font, color=color, small=False):
    if small:
        text = sm_font.render(content, True, color)
        window.blit(text, (x, y))
    else: 
        text = font.render(content, True, color)
        window.blit(text, (x, y))


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


def add_alien(alien_type, num, alien_list):
    for _ in range(num):
        min_pos=(random.randint(window.get_width()+200, window.get_width()+400))
        max_pos=(random.randint(100, window.get_height()-120))
        alien = alien_type(min_pos, max_pos)
        alien_list.append(alien)

def add_rocks(rock_class, rock_list):
    for _ in range(4):
        x = random.choice([random.randint(-window.get_width()+200, -window.get_width()+800), random.randint(window.get_width()+200, window.get_width()+800)])
        y = random.choice([random.randint(window.get_height()+200, window.get_height()+800), random.randint(-window.get_height()+200, -window.get_height()+800)])
        rock = rock_class(x, y, random.randint(1, 3))
        rock_list.append(rock)


def bullet_check(bullet_list):
    if not len(bullet_list) == 0:
        bullet_list[:] = [bullet for bullet in bullet_list if bullet.rect.x >= 0 and bullet.rect.x <= window.get_width() and bullet.rect.y >= 60 and bullet.rect.y <= window.get_height()-60]


def shoot(bullet_class, player, alien, bullet_list, enemy=False):
    if enemy:   
        freq = random.randint(50, 175)
        pX, pY = player.rect.x, player.rect.y

        distanceX = pX - alien.rect.x
        distanceY = pY - alien.rect.y
        angle = math.atan2(distanceY, distanceX)
        speedX = int(10 * math.cos(angle))
        speedY = int(10 * math.sin(angle))

        if alien.rate == 0:
            alien.rate = freq
            bullet_list.append(bullet_class(alien.rect.centerx, alien.rect.centery, speedX, speedY))
    else:
        sX, sY = pygame.mouse.get_pos()

        distanceX = sX - player.rect.x
        distanceY = sY - player.rect.y
        angle = math.atan2(distanceY, distanceX)
        speedX = int(16 * math.cos(angle))
        speedY = int(16 * math.sin(angle))

        if player.rate == 0:
            player.rate = 20
            bullet_list.append(bullet_class(player.rect.centerx, player.rect.centery, speedX, speedY))
