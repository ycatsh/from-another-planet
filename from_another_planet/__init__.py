import pygame
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

# window
windowSize = 1920,1080
window = pygame.display.set_mode((windowSize), pygame.FULLSCREEN|SCALED, vsync=1)

# icons
icon = pygame.image.load('from_another_planet/assets/menus/icon.png').convert_alpha()
pygame.display.set_caption("From Another Planet")
pygame.display.set_icon(icon)

# fonts
font = pygame.font.Font("from_another_planet/assets/fonts/C&C Red Alert [INET].ttf", 60)
sm_font = pygame.font.Font("from_another_planet/assets/fonts/C&C Red Alert [INET].ttf", 30)
color = (110, 69, 206)

# music and sounds
#pygame.mixer.music.load('from_another_planet/assets/sounds/music.wav')
gun_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/gun.wav')
gun_sound.set_volume(0.1)
gun_channel = pygame.mixer.Channel(0)

shotgun_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/shotgun.wav')
shotgun_sound.set_volume(0.3)
shotgun_channel = pygame.mixer.Channel(1)

laser_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/laser.ogg')
laser_channel = pygame.mixer.Channel(2)
burn_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/burn.mp3')
burn_channel = pygame.mixer.Channel(5)

rock_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/asteroid.wav')
rock_channel = pygame.mixer.Channel(3)

teleport_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/teleport.wav')
teleport_sound.set_volume(0.2)
teleport_channel = pygame.mixer.Channel(4)

alien_shoot_sound = pygame.mixer.Sound('from_another_planet/assets/sounds/alien_gun.wav')
alien_shoot_sound.set_volume(0.4)
alien_shoot_channel = pygame.mixer.Channel(6)


# cursor
cursor = pygame.image.load('from_another_planet/assets/cursors/cursor.png').convert_alpha()
crosshair = pygame.image.load('from_another_planet/assets/cursors/crosshair.png').convert_alpha()
tp_cursor = pygame.image.load('from_another_planet/assets/cursors/tp_cursor.png').convert_alpha()


# backgrounds/menus
bg = pygame.image.load('from_another_planet/assets/menus/bg.png').convert_alpha()
menu_bg = pygame.image.load('from_another_planet/assets/menus/menu_bg.png').convert_alpha()
comet = pygame.image.load('from_another_planet/assets/menus/comet.png').convert_alpha()


#logos 
logo = pygame.image.load('from_another_planet/assets/logos/logo.png').convert_alpha()
pause_logo = pygame.image.load('from_another_planet/assets/logos/paused.png').convert_alpha()
over_logo = pygame.image.load('from_another_planet/assets/logos/ended.png').convert_alpha()


# player and enemy
p = pygame.image.load('from_another_planet/assets/p.png').convert_alpha()
a = pygame.image.load('from_another_planet/assets/aliens/a1.png').convert_alpha()
a2 = pygame.image.load('from_another_planet/assets/aliens/a2.png').convert_alpha()
a3 = [pygame.image.load(f'from_another_planet/assets/aliens/big/aB{i}.png').convert_alpha() for i in range(3)]
a4 = pygame.image.load('from_another_planet/assets/aliens/a4.png').convert_alpha()


# bullets
b = pygame.image.load('from_another_planet/assets/bullet.png').convert_alpha()
a_b = pygame.image.load('from_another_planet/assets/aliens/a_b.png').convert_alpha()


# rocks and laser
l = pygame.image.load('from_another_planet/assets/laser.png').convert_alpha()
rockRandom = [pygame.image.load(f'from_another_planet/assets/rocks/r{i}.png').convert_alpha() for i in range(1,7)]


#buttons
bQ = pygame.image.load('from_another_planet/assets/buttons/quit.png').convert_alpha()
bT = pygame.image.load('from_another_planet/assets/buttons/tuto.png').convert_alpha()
bN = pygame.image.load('from_another_planet/assets/buttons/newg.png').convert_alpha()
bR = pygame.image.load('from_another_planet/assets/buttons/resu.png').convert_alpha()

bQc = pygame.image.load('from_another_planet/assets/buttons/quit-clicked.png').convert_alpha()
bTc = pygame.image.load('from_another_planet/assets/buttons/tuto-clicked.png').convert_alpha()
bNc = pygame.image.load('from_another_planet/assets/buttons/newg-clicked.png').convert_alpha()
bRc = pygame.image.load('from_another_planet/assets/buttons/resu-clicked.png').convert_alpha()


#lives
lives = [pygame.image.load(f'from_another_planet/assets/health/{i}.png').convert_alpha() for i in range(7)]