import random

import pygame

from assets import window, comet


class Comet:
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = comet
        self.image = pygame.transform.rotate(self.raw_image, 45)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.gravity = 0.2

    def move(self):
        self.speed += self.gravity 

        if self.speed >= 20:
            self.speed = 20

        self.rect.y += self.speed
        self.rect.x -= 0.8*self.speed

    def update(self):
        if self.rect.y >= window.get_height()+100:
            self.rect.x = random.randint(1500, 5000)
            self.rect.y = -random.randint(10, 1000)

            
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
