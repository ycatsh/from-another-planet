import pygame
from pygame.locals import *
from assets import window, cursor, crosshair


def menu(text, font, COLOR, x, y):
    m = font.render(text, True, COLOR)
    window.blit(m, (x, y))

def show_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(cursor, pos)

def change_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    cX, cY = pygame.mouse.get_pos()
    pos = [cX, cY]
    window.blit(crosshair, pos)