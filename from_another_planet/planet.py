import random
import math

import pygame

from from_another_planet import G


class Planet:
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        #self.image = random.choice(planet_sprites)
        #self.tmp_image = self.image
        self.circle = (x, y)
        self.speed = speed
        self.angle = 10
        self.mass = 80
        self.remove = False

    def update(self, window):
        pass
        # self.tmp_image = pygame.transform.rotate(self.image, self.angle)
        # self.rect = self.tmp_image.get_rect(center=self.rect.center)
        # self.angle += 1 % 360

        # self.rect.x += self.speed * self.directionx
        # self.rect.y += self.speed * self.directiony

    def gravity(self, subject):
        distance_subject_x = self.circle[0] - subject.rect.centerx
        distance_subject_y = self.circle[1] - subject.rect.centery
        distance_subject = math.sqrt(distance_subject_x**2 + distance_subject_y**2)

        if distance_subject == 0:
            return 0, 0
        
        norm_subject_x = distance_subject_x / distance_subject
        norm_subject_y = distance_subject_y / distance_subject
        gravity = G*(self.mass)*subject.mass / distance_subject**2
        gravity_x = gravity * norm_subject_x
        gravity_y = gravity * norm_subject_y

        return gravity_x, gravity_y

    def collide(self, game_vars, laser):
        pass
        # if pygame.Rect.colliderect(self.rect, laser.rect):
        #     pass

        # for bullet in pygame.sprite.spritecollide(self, game_vars.bulletList, False):
        #     game_vars.bulletList.remove(bullet)

    def show(self, window, shake_offset):
        pygame.draw.circle(window, (255, 255, 255), (self.circle[0], self.circle[1]), radius=100, width=2)
        #window.blit(self.tmp_image, (self.rect.x + shake_offset[0], self.rect.y + shake_offset[1]))
