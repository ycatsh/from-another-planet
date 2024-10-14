import random

import pygame

from from_another_planet import laser_channel, laser_sound
from from_another_planet.helper.config import proximity_sound


class Laser:
    def __init__(self, laser_sprite, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 2
        self.speedy = 2
        self.directiony = random.choice([1, -1])

    def update(self, vars):
        slowdown = random.randint(1, 4)
        self.speedx += vars.lvl / 8
        self.speedy += vars.lvl / 12

        if self.speedx > 12 or self.speedy > 12:
            if slowdown == 1:
                self.speedx = 6
                self.speedy = 6

    def moveLR(self, window, player):
        self.rect.x += self.speedx
        if self.rect.top < 10:
            self.directiony = 1
        if self.rect.bottom > window.get_height()-10:
            self.directiony = -1
        self.rect.y += self.speedy * self.directiony
        proximity_sound(player, self, laser_channel, laser_sound, proximity_range=700)

    def reset(self):
        self.rect.x = (self.rect.x * -1) + self.speedx

    def show(self, window, shake_offset):
        window.blit(self.image, (self.rect.x + shake_offset[0], self.rect.y + shake_offset[1]))
