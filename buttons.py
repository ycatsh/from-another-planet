import pygame
from assets import window


class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.click = False

    def draw(self):
        action = False
        mXY = pygame.mouse.get_pos()

        if self.rect.collidepoint(mXY):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                action = True
                self.click = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

        window.blit(self.image, (self.rect.x, self.rect.y))

        return action