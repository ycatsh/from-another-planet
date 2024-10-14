import random
import math 

import pygame

from from_another_planet import window, comet


class CometAnimation:
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


class TeleportAnimation:
    def __init__(self, player, num_particles):
        self.player = player
        self.lifetime = random.randint(200, 500)
        self.size = random.uniform(2, 5)
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)
        self.num_particles = num_particles
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(0.5, 2)
        self.orbit_radius = random.uniform(45, 65)

    def update(self, time):
        self.angle += random.uniform(-0.05, 0.05) * self.speed
        self.dx += random.uniform(-0.5, 0.5)
        self.dy += random.uniform(-0.5, 0.5)

        self.lifetime -= time
        if self.lifetime < 100:
            self.size = max(self.size - 0.05, 0.5)

    def is_alive(self):
        return self.lifetime > 0

    @staticmethod
    def cleanup(particles):
        return [particle for particle in particles if particle.is_alive()]

    def show(self):
        angle_in_radians = math.radians(self.angle)
        particle_x = self.orbit_radius * math.cos(angle_in_radians)
        particle_y = self.orbit_radius * math.sin(angle_in_radians)
        color = (random.randint(140, 160), random.randint(60, 100), random.randint(230, 255))
        pygame.draw.circle(window, color, (int(self.player.rect.centerx + particle_x), int(self.player.rect.centery + particle_y)), int(self.size))


class RockExplosion:
    def __init__(self, x, y, radius, particle_count=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.color_list = [(109, 111, 115), (195, 195, 195), (188, 190, 194), (147, 149, 153)]
        self.particle_count = particle_count
        self.lifetime = 100
        self.frames = []
        self.create_frames()

    def create_frames(self):
        for i in range(self.lifetime):
            current_radius = self.radius - (i * 3)
            current_radius = max(1, current_radius)
            color_list = self.color_list[:len(self.color_list) - i // 10]
            surface = self.generate_explosion(current_radius, color_list)
            self.frames.append(surface)

    def generate_explosion(self, radius, color_list):
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        center = (radius, radius)
        for color in color_list:
            for _ in range(self.particle_count):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, radius)
                x = int(center[0] + distance * math.cos(angle))
                y = int(center[1] + distance * math.sin(angle))
                particle_size = random.randint(8, 12)
                pygame.draw.rect(surface, color, (x, y, particle_size, particle_size))
        return surface

    def update(self):
        if self.lifetime > 0:
            self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

    def show(self):
        if self.lifetime > 0:
            current_frame = 100 - self.lifetime
            window.blit(self.frames[current_frame], (self.x - self.radius, self.y - self.radius))

    @staticmethod
    def cleanup(particles):
        return [particle for particle in particles if particle.is_alive()]