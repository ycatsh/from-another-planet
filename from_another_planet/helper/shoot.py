import random
import math

import pygame 

from from_another_planet import b, a_b, shotgun_channel, shotgun_sound, alien_shoot_channel, alien_shoot_sound
from from_another_planet.helper.config import proximity_sound


def bullet_check(bullet_list, window):
    if not len(bullet_list) == 0:
        bullet_list[:] = [bullet for bullet in bullet_list if bullet.rect.x >= 0 and bullet.rect.x <= window.get_width() and bullet.rect.y >= 60 and bullet.rect.y <= window.get_height()-60]

def alien_shoot(bullet_class, player, alien, bullet_list):
    freq = random.randint(25, 50)
    distanceX = player.rect.x - alien.rect.x
    distanceY = player.rect.y - alien.rect.y
    angle = math.atan2(distanceY, distanceX)
    speedX = int(10 * math.cos(angle))
    speedY = int(10 * math.sin(angle))

    if alien.rate == 0:
        alien.rate = freq
        alien_shoot_channel.play(alien_shoot_sound)
        proximity_sound(player, alien, alien_shoot_channel, alien_shoot_sound, proximity_range=500)
        bullet_list.append(bullet_class(a_b, alien.rect.centerx, alien.rect.centery, speedX, speedY))


def player_shoot(bullet_class, player, bullet_list, effects):
    mouse_pos = pygame.mouse.get_pos()
    distanceX = mouse_pos[0] - player.rect.x
    distanceY = mouse_pos[1] - player.rect.y
    angle = math.atan2(distanceY, distanceX)
    speedX = int(16 * math.cos(angle))
    speedY = int(16 * math.sin(angle))
    bullet = bullet_class(b, player.rect.centerx, player.rect.centery, speedX, speedY)
    bullet.rotate(angle)
    bullet_list.append(bullet)
    effects.recoil(angle)


def player_shotgun(bullet_class, player, bullet_list, effects):
    mouse_pos = pygame.mouse.get_pos()
    distanceX = mouse_pos[0] - player.rect.x
    distanceY = mouse_pos[1] - player.rect.y
    angle = math.atan2(distanceY, distanceX) + ((7 / 12) * math.pi / 2)

    if player.gun:
        if player.srate == 0:
            player.srate = 300

            for _ in range(14):
                speedX = int(16 * math.cos(angle))
                speedY = int(16 * math.sin(angle))
                shell = bullet_class(b, player.rect.centerx, player.rect.centery, speedX, speedY, angle)
                shell.rotate(angle)
                angle -= 0.2
                bullet_list.append(shell)
                shotgun_channel.play(shotgun_sound)
                effects.recoil(angle, recoil_strength=5)