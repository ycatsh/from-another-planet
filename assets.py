import pygame
from pygame.locals import *

pygame.init()

# window
windowSize = 1920,1080
window = pygame.display.set_mode((windowSize), pygame.FULLSCREEN|SCALED, vsync=1)

# icons
icon = pygame.image.load('assets/icon.png').convert_alpha()
pygame.display.set_caption("From Another Planet")
pygame.display.set_icon(icon)

# fonts
font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 60)
sm_font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 30)
color = (110, 69, 206)


# cursor
cursor = pygame.image.load('assets/cursor.png').convert_alpha()
crosshair = pygame.image.load('assets/crosshair.png').convert_alpha()


# backgrounds
bg = pygame.image.load('assets/bg.png').convert_alpha()
start_bg = pygame.image.load('assets/start_bg.png').convert_alpha()
menu_bg = pygame.image.load('assets/menu_bg.png').convert_alpha()
over_bg = pygame.image.load('assets/over_bg.png').convert_alpha()


# player and enemy
p = pygame.image.load('assets/p.png').convert_alpha()
a = pygame.image.load('assets/aliens/a1.png').convert_alpha()
a2 = pygame.image.load('assets/aliens/a2.png').convert_alpha()
a3 = [pygame.image.load(f'assets/aliens/big/aB{i}.png').convert_alpha() for i in range(3)]
a4 = pygame.image.load('assets/aliens/a4.png').convert_alpha()


# bullets
b = pygame.image.load('assets/bullet.png').convert_alpha()
a_b = pygame.image.load('assets/aliens/a_b.png').convert_alpha()


# rocks and laser
l = pygame.image.load('assets/laser.png').convert_alpha()
rockRandom = [pygame.image.load(f'assets/rocks/r{i}.png').convert_alpha() for i in range(1,7)]


#buttons
bP = pygame.image.load('assets/resume_button.png').convert_alpha()
bQ = pygame.image.load('assets/quit_button.png').convert_alpha()


#lives
lives = [pygame.image.load(f'assets/health/{i}.png').convert_alpha() for i in range(7)]


#explosion
explosion_frames = []
for i in range(100):
    surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 255, 255), (100, 100), 100-(i/1.5))
    explosion_frames.append(surface)