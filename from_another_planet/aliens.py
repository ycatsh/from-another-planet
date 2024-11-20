import random

import pygame

from from_another_planet.helper.shoot import alien_shoot, bullet_check
from from_another_planet.bullet import AlienBullet


class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_sprite, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def check_collisions(self, hit_list, alien_list, game_vars, is_bullet=False):
        collisions = pygame.sprite.spritecollide(self, hit_list, False)
        remove = []
        for other in collisions:
            if is_bullet:
                hit_list.remove(other)
                remove.append(self)
                game_vars.aliensKilled += 1
            else:
                remove.append(self)
        for alien in remove:
            if alien in alien_list:
                alien_list.remove(alien)

    def check_player_collision(self, this_list, game_vars, player):
        if self.rect.colliderect(player.rect):
            this_list.remove(self)
            player.lives -= 1
            if player.lives <= 0:
                game_vars.cause_of_death = "Hit by alien"

    def move(self):
        self.rect.x -= self.speed

    def update(self, player, game_vars):
        self.check_collisions(game_vars.rockList, game_vars.alienList, game_vars, is_bullet=False)
        self.check_collisions(game_vars.bulletList, game_vars.alienList, game_vars, is_bullet=True)
        self.check_player_collision(game_vars.alienList, game_vars, player=player)

    def show(self, window, offset):
        window.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class BlueAlien(Alien):
    def __init__(self, blue_alien_sprite, x, y):
        super().__init__(blue_alien_sprite, x, y)
        self.speed = 3.5

    def move(self):
        self.rect.x -= self.speed

    def update(self, player, game_vars):
        self.check_collisions(game_vars.rockList, game_vars.blue_alienList, game_vars, is_bullet=False)
        self.check_collisions(game_vars.bulletList, game_vars.blue_alienList, game_vars, is_bullet=True)
        self.check_player_collision(game_vars.blue_alienList, game_vars, player=player)

    def show(self, window, offset):
        window.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class BigAlien(Alien):
    def __init__(self, alien_big_sprite, x, y):
        super().__init__(alien_big_sprite[1], x, y)
        self.lives = 2

    def move(self):
        self.rect.x -= self.speed

    def update(self, player, game_vars):
        self.check_collisions(game_vars.rockList, game_vars.big_alienList, game_vars, is_bullet=False)
        self.check_player_collision(game_vars.big_alienList, game_vars, player=player)

        collisions = pygame.sprite.spritecollide(self, game_vars.bulletList, False)
        remove = []
        for bullet in collisions:
            game_vars.bulletList.remove(bullet)
            self.lives -= 1
            if self.lives < 0:
                game_vars.aliensKilled += 1
                remove.append(self)
        for big_alien in remove:
            if big_alien in game_vars.big_alienList:
                game_vars.big_alienList.remove(big_alien)

    def show(self, window, alien_big_sprite, offset):
        window.blit(alien_big_sprite[self.lives], (self.rect.x + offset[0], self.rect.y + offset[1]))


class ShootAlien(Alien):
    def __init__(self, shoot_alien_sprite, x, y):
        super().__init__(shoot_alien_sprite, x, y)
        self.speed = 3
        self.rate = 0

    def move(self, player, window, game_vars):
        self.rect.x -= self.speed
        if self.rect.x < window.get_width():
            alien_shoot(AlienBullet, player, self, game_vars.alien_bulletList)
            bullet_check(game_vars.alien_bulletList, window)

    def update(self, player, game_vars):
        if self.rate > 0:
            self.rate -= 1

        self.check_collisions(game_vars.rockList, game_vars.shoot_alienList, game_vars, is_bullet=False)
        self.check_collisions(game_vars.bulletList, game_vars.shoot_alienList, game_vars, is_bullet=True)
        self.check_player_collision(game_vars.shoot_alienList, game_vars, player=player)

    def show(self, window, offset):
        window.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))