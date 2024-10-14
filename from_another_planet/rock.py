import random

import pygame

from from_another_planet.helper.animate import RockExplosion
from from_another_planet import rock_sound, burn_channel, burn_sound


class Rock:
    def __init__(self, rock_sprites, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rock_sprites)
        self.tmp_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = 10
        self.lives = 5
        self.directionx = random.choice([1, -1])
        self.directiony = random.choice([1, -1])
        self.exploded = False
        self.remove = False 

    def explode(self, vars):
        if self.lives <= 0 and not self.exploded:
            explosion = RockExplosion(self.rect.centerx, self.rect.centery, 100)
            vars.explosionParticles.append(explosion)
            self.exploded = True
            rock_sound.play()
            self.remove = True

    def update(self, window):
        if self.lives > 0:
            self.tmp_image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.tmp_image.get_rect(center=self.rect.center)
            self.angle += 1 % 360

            if self.rect.right < -random.randint(100, 300):
                self.directionx = 1
            if self.rect.right > window.get_width() + random.randint(100, 300):
                self.directionx = -1
            if self.rect.top < -random.randint(100, 300):
                self.directiony = 1
            if self.rect.bottom > window.get_height() + random.randint(100, 300):
                self.directiony = -1

            self.rect.x += self.speed * self.directionx
            self.rect.y += self.speed * self.directiony

    def collide(self, vars, laser):
        other_rocks = [rock for rock in vars.rockList if rock != self]
        for rock in pygame.sprite.spritecollide(self, other_rocks, False):
            self.lives = 0
            rock.lives = 0
        
        if pygame.Rect.colliderect(self.rect, laser.rect):
            burn_channel.play(burn_sound)
            self.remove = True

        for bullet in pygame.sprite.spritecollide(self, vars.bulletList, False):
            vars.bulletList.remove(bullet)
            self.lives -= 1

        self.explode(vars)

    def show(self, window, shake_offset):
        window.blit(self.tmp_image, (self.rect.x + shake_offset[0], self.rect.y + shake_offset[1]))
