import math

import pygame

from from_another_planet.helper.config  import hide_cursor, teleport_cursor
from from_another_planet.helper.animate import TeleportAnimation
from from_another_planet import teleport_channel, teleport_sound


class Player:
    def __init__(self, player_sprite, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_sprite
        self.lives = 6
        self.charge = "NOT ACTIVATED"
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5
        self.srate = 0
        self.gun = False
        self.next_teleport = 10
        self.friction = 0.96
        self.mass = 5

    def update(self, telep, game_vars):
        if self.srate > 0:
            self.srate -= 1
        if game_vars.aliensKilled >= 30:
            self.gun = True

        mXY = pygame.mouse.get_pos()
        angle = math.atan2(mXY[1]-self.rect.centery, mXY[0]-self.rect.centerx)*180/math.pi
        self.rotated_image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)

        if game_vars.aliensKilled > 0:
            if game_vars.aliensKilled >= self.next_teleport:
                self.charge = "ACTIVATED"
                hide_cursor()
                teleport_cursor()
                if telep:
                    self.next_teleport = game_vars.aliensKilled + 10
                    self.rect.x = mXY[0]
                    self.rect.y = mXY[1]
                    teleport_channel.play(teleport_sound)
                    for _ in range(game_vars.NUM_TELEPORT_PARTICLES):
                        game_vars.teleportParticles.append(TeleportAnimation(self, game_vars.NUM_TELEPORT_PARTICLES))
            else:
                self.charge = "NOT ACTIVATED"

    def collide(self, game_vars, laser):
        for _ in pygame.sprite.spritecollide(self, game_vars.rockList, False):
            self.lives = 0
            game_vars.cause_of_death = "Killed by asteroid"

        if pygame.Rect.colliderect(self.rect, laser.rect):
            self.lives = 0
            game_vars.cause_of_death = "Killed by Laser"

    def move(self, window, moveR, moveL, moveU, moveD):
        x_acceleration = 0
        y_acceleration = 0

        if moveR:
            x_acceleration = self.acceleration
        elif moveL:
            x_acceleration = -self.acceleration
        else:
            x_acceleration = 0
        if moveU:
            y_acceleration = -self.acceleration
        elif moveD:
            y_acceleration = self.acceleration
        else:
            y_acceleration = 0

        self.velocity_x += x_acceleration
        self.velocity_y += y_acceleration

        if not (moveR or moveL):
            self.velocity_x *= 0.95
        if not (moveU or moveD):
            self.velocity_y *= 0.95

        self.velocity_x = max(min(self.velocity_x, self.speed), -self.speed)
        self.velocity_y = max(min(self.velocity_y, self.speed), -self.speed)
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.bottom > window.get_height() - 81:
             self.rect.bottom = window.get_height() - 81
             self.velocity_y = 0

        if self.rect.top < 81:
            self.rect.top = 81
            self.velocity_y = 0

        if self.rect.right > window.get_width() - 20:
            self.rect.right = window.get_width() - 20
            self.velocity_x = 0

        if self.rect.left <= 20:
           self.rect.left = 25
           self.velocity_x = 0

    def slowdown(self):
        if abs(self.velocity_x) > 0:
            self.velocity_x *= self.friction
        if abs(self.velocity_y) > 0:
            self.velocity_y *= self.friction
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def show(self, window, offset):
        window.blit(self.rotated_image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class HealthBar:
    def __init__(self, health_bar_sprite, x, y, scale):
        width = health_bar_sprite.get_width()
        height = health_bar_sprite.get_height()
        self.image = pygame.transform.scale(health_bar_sprite, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def show(self, window, sprites, player):
        window.blit(sprites[player.lives], (self.rect.x, self.rect.y))