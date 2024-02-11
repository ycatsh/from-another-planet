import pygame

from assets import window


class Button:
    def __init__(self, image, clicked,  x, y):
        self.image = image
        self.clicked = clicked
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.click = False

    def pressed(self):
        action = False
        mXY = pygame.mouse.get_pos()

        if self.rect.collidepoint(mXY):
            self.tmp_image = self.clicked

            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                action = True
                self.click = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False
        else:
            self.tmp_image = self.image

        window.blit(self.tmp_image, (self.rect.x, self.rect.y))

        return action
