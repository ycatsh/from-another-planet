import math

import pygame


class Bullet:
    def __init__(self, bullet_sprite, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = dx
        self.dy = dy

    def update(self):        
        self.rect.x += self.dx
        self.rect.y += self.dy

    def rotate(self, angle):
        self.rotated_image = pygame.transform.rotate(self.image, -math.degrees(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def show(self, window):
        window.blit(self.rotated_image, (self.rect.x, self.rect.y))


class AlienBullet:
    def __init__(self, alien_bullet_sprite, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_bullet_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = dx
        self.dy = dy

    def update(self, player, game_vars):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if pygame.Rect.colliderect(self.rect, player.rect):
            game_vars.alien_bulletList.remove(self)
            player.lives -= 1
            if player.lives <= 0:
                game_vars.cause_of_death = "Killed by alien shots"

    def show(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Shell(Bullet):
    def __init__(self, bullet_sprite, x, y, dx, dy, angle):
        super().__init__(bullet_sprite, x, y, dx, dy)
        self.angle = angle