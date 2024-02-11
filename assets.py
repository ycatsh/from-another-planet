import pygame
from pygame.locals import *


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

# window
windowSize = 1920,1080
window = pygame.display.set_mode((windowSize), pygame.FULLSCREEN|SCALED, vsync=1)

# icons
icon = pygame.image.load('assets/menus/icon.png').convert_alpha()
pygame.display.set_caption("From Another Planet")
pygame.display.set_icon(icon)

# fonts
font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 60)
sm_font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 30)
color = (110, 69, 206)

#music 
#pygame.mixer.music.load('assets/sounds/music.wav')
#shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.wav')


# cursor
cursor = pygame.image.load('assets/cursors/cursor.png').convert_alpha()
crosshair = pygame.image.load('assets/cursors/crosshair.png').convert_alpha()
tp_cursor = pygame.image.load('assets/cursors/tp_cursor.png').convert_alpha()


# backgrounds/menus
bg = pygame.image.load('assets/menus/bg.png').convert_alpha()
menu_bg = pygame.image.load('assets/menus/menu_bg.png').convert_alpha()
comet = pygame.image.load('assets/menus/comet.png').convert_alpha()


#logos 
logo = pygame.image.load('assets/logos/logo.png').convert_alpha()
pause_logo = pygame.image.load('assets/logos/paused.png').convert_alpha()
over_logo = pygame.image.load('assets/logos/ended.png').convert_alpha()


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
bQ = pygame.image.load('assets/buttons/quit.png').convert_alpha()
bT = pygame.image.load('assets/buttons/tuto.png').convert_alpha()
bN = pygame.image.load('assets/buttons/newg.png').convert_alpha()
bR = pygame.image.load('assets/buttons/resu.png').convert_alpha()

bQc = pygame.image.load('assets/buttons/quit-clicked.png').convert_alpha()
bTc = pygame.image.load('assets/buttons/tuto-clicked.png').convert_alpha()
bNc = pygame.image.load('assets/buttons/newg-clicked.png').convert_alpha()
bRc = pygame.image.load('assets/buttons/resu-clicked.png').convert_alpha()


#lives
lives = [pygame.image.load(f'assets/health/{i}.png').convert_alpha() for i in range(7)]


#explosion
explosion_frames = []
for i in range(100):
    surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 255, 255), (100, 100), 100-(i/1.5))
    explosion_frames.append(surface)
