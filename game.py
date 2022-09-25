import pygame, sys
from pygame.locals import *
import buttons 
import random

clock = pygame.time.Clock()

pygame.init()

windowSize = (1200, 800)
window = pygame.display.set_mode(windowSize, 0, 32)

#pause
gamePause = False 

icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("From Another Planet")

font = pygame.font.Font("fonts/font.ttf", 60)
font2 = pygame.font.Font("fonts/font.ttf", 30)
font3 = pygame.font.Font("fonts/font.ttf", 25)

mColor = (110, 69, 206)

resumeb = pygame.image.load('assets/resume_button.png').convert_alpha()
resumeButton = buttons.Button(580, 380, resumeb, 1)

quitb = pygame.image.load('assets/quit_button.png').convert_alpha()
quitButton = buttons.Button(580, 490, quitb, 1)

def menu(text, font, mColor, x, y):
    m = font.render(text, True, mColor)
    window.blit(m, (x,y))

bg = pygame.image.load('assets/bg.png')
menu_bg = pygame.image.load('assets/menu_bg.png')
over_bg = pygame.image.load('assets/over_bg.png')
p = pygame.image.load('assets/p.png')
b = pygame.image.load('assets/bullet.png')
rockList = []

for i in range(1,6):
    rockChoose = pygame.image.load(f'assets/rocks/r{i}.png')
    rockList.append(rockChoose)

print(rockList)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(p, (int(p.get_width()*scale), p.get_height() * scale))
        self.lives = 3
        self.flip = False
        self.directionx = 0
        self.directiony = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.location = location
        self.rate = 0

    def update(self):
        if self.rate > 0:
            self.rate -= 1
    
    def move(self, moveR, moveL, moveU, moveD):
        x = 0
        y = 0

        if moveR: 
            x = self.location
            self.directionx = 1
            self.flip = True
        if moveL:
            x = -self.location
            self.directionx = -1
            self.flip = False 
        if moveU: 
            y = -self.location
            self.directiony = 1
            self.flip = True
        if moveD:
            y = self.location
            self.directiony = -1
            self.flip = False

        if self.rect.bottom + y > 740:
            y = 740 - self.rect.bottom
        
        if self.rect.top + y < 65:
            y = 5

        if self.rect.left + x > 1080:
            x = 1080 - self.rect.left

        if self.rect.right + x <= 120:
            x = 120 - self.rect.right
        
        self.rect.x += x
        self.rect.y += y

    def shoot(self):
        if self.rate == 0:
            self.rate = 30
            bullet = Bullet(self.rect.centerx+(40*self.directionx), self.rect.centery+(5*self.directiony),self.directionx, self.directiony)
            bulletGroup.add(bullet)

    def show(self):
        window.blit(pygame.transform.flip(self.image, self.flip, self.flip), self.rect)

player = Player(600, 400, 1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, directionx, directiony):
        pygame.sprite.Sprite.__init__(self)
        self.image = b
        self.directionx = directionx
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 10

    def update(self):
        self.rect.x += (self.directionx * self.speed)

        if self.rect.right < 95 or self.rect.left > 1105:
            #print(self.rect.right)
            #print(self.rect.left)
            self.kill()

bulletGroup = pygame.sprite.Group()

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rockList)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

rockGroup = pygame.sprite.Group()
for i in range(3):
    rock = Rock(random.randint(60, 950), random.randint(100, 660), random.randint(200, 1500))
    rockGroup.add(rock)

lvl = 1
gameOver = False
moveR = False
moveL = False
moveU = False
moveD = False
shoot = False
playerTurn = False

#game loop
while True: 

    window.blit(bg, (0, 0))

    if gameOver == True: 
        window.blit(over_bg, (0, 0))
        menu("GAME OVER", font, mColor, 600, 400)

    elif gamePause == True:
        window.blit(menu_bg, (0, 0))
        menu("GAME MENU", font, mColor, 470, 240)

        if resumeButton.draw(window):
            gamePause = False

        if quitButton.draw(window):
            pygame.quit()
            sys.exit()

    else:

        menu("press 'ESC' to pause", font3, mColor, 920, 745)
        menu(f"LEVEL: {lvl}", font3, mColor, 995, 90)
        menu(f"Direction: {player.directionx, player.directiony}", font3, mColor, 75, 745)
        hearts = player.lives * ' X '
        if player.lives == 0:
            menu(f"LIVES: *DEAD*", font3, mColor, 995, 65)
        else:
            menu(f"LIVES:{hearts}", font3, mColor, 995, 65)
        menu(f"Location: {player.rect.x, player.rect.y}", font3, mColor, 75, 20)
        menu(f"tap SPACE to shoot", font3, mColor, 350, 745)
        if player.rate == 0:
            menu(f"Fire Rate: ready", font3, mColor, 655, 745)
        else:
            menu(f"Fire Rate: {player.rate}", font3, mColor, 655, 745)
        
        rockGroup.draw(window)

        bulletGroup.draw(window)
        bulletGroup.update()

        player.update()
        player.show()
        player.move(moveR, moveL, moveU, moveD)

        if player.lives <= 3 and player.lives != 0:
            if shoot: 
                comb = []
                comb.append(player.directionx)
                comb.append(player.directiony)
                #print(comb) 
                player.shoot()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gamePause = True
            if event.key == K_SPACE:
                shoot = True
            if event.key == K_RIGHT or event.key == K_d:
                moveR = True
            if event.key == K_LEFT or event.key == K_a:
                moveL = True
            if event.key == K_UP or event.key == K_w:
                moveU = True
            if event.key == K_DOWN or event.key == K_s:
                moveD = True

        if event.type == KEYUP:
            if event.key == K_SPACE:
                shoot = False
            if event.key == K_RIGHT or event.key == K_d:
                moveR = False
            if event.key == K_LEFT or event.key == K_a:
                moveL = False
            if event.key == K_UP or event.key == K_w:
                moveU = False
            if event.key == K_DOWN or event.key == K_s:
                moveD = False

        if player.lives == 0:
            gameOver = True

    pygame.display.update()
    clock.tick(60)
