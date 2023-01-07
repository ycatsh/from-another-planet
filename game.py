import pygame
import sys
from pygame.locals import *
import random
import math

clock = pygame.time.Clock()
pygame.init()


windowSize = 1920,1080
window = pygame.display.set_mode((windowSize), pygame.FULLSCREEN|SCALED, vsync=1)

# icons
icon = pygame.image.load('assets/icon.png').convert_alpha()
pygame.display.set_caption("From Another Planet")
pygame.display.set_icon(icon)

# fonts C&C Red Alert [INET]
menuFont = pygame.font.Font("assets/fonts/font.ttf", 100)
font = pygame.font.Font("assets/fonts/font.ttf", 60)
font2 = pygame.font.Font("assets/fonts/font.ttf", 30)

lvl = 1
aliensKilled = 0
nA = 4  # number of aliens every level; level 1: 4
n_bA = 2  # number of blue aliens every level
n_bgA = 1  # number of big aliens every level
n_sA = 2 # number of shooting aliens every level

a3 = []
alienList = []
blue_alienList = []
big_alienList = []
shoot_alienList = []
alien_bulletList = []
laserList = []
rockList = []
bulletList = []
particleList = [] #DEV
particleColors = [(251, 0, 0)] #DEV

# cursor
cursor = pygame.image.load('assets/cursor.png').convert_alpha()

# backgrounds
bg = pygame.image.load('assets/bg.png').convert_alpha()
start_bg = pygame.image.load('assets/start_bg.png').convert_alpha()
menu_bg = pygame.image.load('assets/menu_bg.png').convert_alpha()
over_bg = pygame.image.load('assets/over_bg.png').convert_alpha()

#player and enemy
p = pygame.image.load('assets/p.png').convert_alpha()
a = pygame.image.load('assets/aliens/a1.png').convert_alpha()
a2 = pygame.image.load('assets/aliens/a2.png').convert_alpha()
a4 = pygame.image.load('assets/aliens/a4.png').convert_alpha()

for l in range(3):
    img = pygame.image.load(f'assets/aliens/big/aB{l}.png').convert_alpha()
    a3.append(img)

# bullet
b = pygame.image.load('assets/bullet.png').convert_alpha()
a_b = pygame.image.load('assets/aliens/a_b.png').convert_alpha()

# bomb
# bmb = pygame.image.load('assets/bomb.png').convert_alpha()

# laser
l1 = pygame.image.load('assets/laser1.png').convert_alpha()
l2 = pygame.image.load('assets/laser2.png').convert_alpha()

rockRandom = []
for i in range(1, 7):
    rockChoose = pygame.image.load(f'assets/rocks/r{i}.png').convert_alpha()
    rockRandom.append(rockChoose)

mColor = (110, 69, 206)


def menu(text, font, mColor, x, y):
    m = font.render(text, True, mColor)
    window.blit(m, (x, y))

class Button():
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
                self.click = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

        window.blit(self.image, (self.rect.x, self.rect.y))

        return action


# buttons
bP = pygame.image.load('assets/resume_button.png').convert_alpha()
bQ = pygame.image.load('assets/quit_button.png').convert_alpha()

playButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40)
quitButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140)
play_overButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40)
quit_overButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140)
play_pauseButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40)
quit_pauseButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            p, (int(p.get_width()*scale), p.get_height() * scale))
        self.lives = 6
        self.flip = False
        self.directionx = 0
        self.directiony = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.location = location
        self.rate = 0

    def update(self):
        if self.rate > 0:
            self.rate -= 1

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
        for _ in collisionsRock:
            if self.lives != 0:
                self.lives = 0

        collisionsLaser = pygame.Rect.colliderect(self.rect, laser.rect)
        if collisionsLaser:
            #print(log.pos, self.rect.y)
            if self.rect.y < laser.pos - 32 or self.rect.y > laser.pos + 32:
                if self.lives != 0:
                    self.lives = 0
            else:
                pass

    def move(self, moveR, moveL, moveU, moveD):
        x = 0
        y = 0

        if moveR:
            x = self.location
            self.directionx = 1
            self.flip = False
            y = 0

        if moveL:
            x = -self.location
            self.directionx = -1
            self.flip = True
            y = 0

        if moveU:
            y = -self.location
            self.directiony = 1
            x = 0

        if moveD:
            y = self.location
            self.directiony = -1
            x = 0

        if self.rect.bottom + y > window.get_height()-60:
            y = window.get_height()-60 - self.rect.bottom

        if self.rect.top + y < 65:
            y = 5

        if self.rect.left + x > window.get_width()-120:
            x = window.get_width()-120 - self.rect.left

        if self.rect.right + x <= 120:
            x = 120 - self.rect.right

        self.rect.x += x
        self.rect.y += y

    def show(self):
        window.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


player = Player(round(window.get_width()/2), round(window.get_height()/2), 1, 5)

lives = []
for x in range(7):
    healthImage = pygame.image.load(f'assets/health/{x}.png').convert_alpha()
    lives.append(healthImage)


class HealthBar():
    def __init__(self, image, x, y, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def show(self):
        window.blit(lives[player.lives], (self.rect.x, self.rect.y))


HEALTH = HealthBar(lives[player.lives], round(window.get_width()/2), window.get_height()-45, 0.7)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = b
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


def bullet_move():
    sX, sY = pygame.mouse.get_pos()

    distanceX = sX - player.rect.x
    distanceY = sY - player.rect.y

    angle = math.atan2(distanceY, distanceX)

    speedX = int(8 * math.cos(angle))
    speedY = int(8 * math.sin(angle))

    if player.rate == 0:
        player.rate = 30
        bulletList.append(Bullet(
            player.rect.centerx, player.rect.centery, speedX, speedY))

def bullet_check():
    if not len(bulletList) == 0:
        for bullet in bulletList:
            if not bullet.rect.x >= 0 and bullet.rect.x <= window.get_width() and bullet.rect.y >= 60 and bullet.rect.y <= window.get_height()-60:
                try:
                    bulletList.remove(bullet)
                except ValueError:
                    pass

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = a_b
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 6
        self.rate = 0
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            alien_bulletList.remove(self)
            player.lives -= 1

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

def alien_shoot():
    global alien_bullet 
    freq = random.randint(75, 150)

    pX, pY = player.rect.x, player.rect.y

    distanceX = pX - alienShoot.rect.x
    distanceY = pY - alienShoot.rect.y

    angle = math.atan2(distanceY, distanceX)

    speedX = int(6 * math.cos(angle))
    speedY = int(6 * math.sin(angle))

    if alienShoot.rate == 0:
        alienShoot.rate = freq
        alien_bulletList.append(AlienBullet(alienShoot.rect.centerx, alienShoot.rect.centery, speedX, speedY))

def alien_bullet_check():
    if not len(alien_bulletList) == 0:
        for alien_bullet in alien_bulletList:
            if not  alien_bullet.rect.x >= 0 and alien_bullet.rect.x <= window.get_width() and alien_bullet.rect.y >= 60 and alien_bullet.rect.y <= window.get_height()-60:
                try:
                    alien_bulletList.remove(alien_bullet)
                except ValueError:
                    pass

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = a
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def move(self):
        self.rect.x -= self.speed

    def update(self):
        global aliensKilled

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
        for _ in collisionsRock:
            alienList.remove(self)


        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False)
        for bullet in collisionsBullet:
            # particle_show()
            #particle_start(self.rect.centerx, self.rect.centery)
            if player.lives > 0:
                bulletList.remove(bullet)
                alienList.remove(self)
                aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            alienList.remove(alien)
            player.lives -= 1

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


for _ in range(nA):
    alien = Alien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    alienList.append(alien)


class BlueAlien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = a2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3.5
        self.chance = random.randint(1, 5)

    def move(self):
        if self.chance == 2:
            self.rect.x -= self.speed

    def update(self):
        global aliensKilled

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
        for _ in collisionsRock:
            blue_alienList.remove(self)


        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False)
        for bullet in collisionsBullet:
            # particle_show()
            #particle_start(self.rect.centerx, self.rect.centery)
            if player.lives > 0:
                bulletList.remove(bullet)
                blue_alienList.remove(self)
                aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            blue_alienList.remove(self)
            player.lives -= 1

    def show(self):
        if self.chance == 2:
            window.blit(self.image, (self.rect.x, self.rect.y))


for _ in range(n_bA):
    alienBlue = BlueAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    blue_alienList.append(alienBlue)


class BigAlien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 2
        self.image = a3[self.lives]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.chance = random.randint(1, 4)

    def move(self):
        if lvl > 4:
            if self.chance == 3:
                self.rect.x -= self.speed

    def update(self):
        global aliensKilled

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
        for _ in collisionsRock:
            big_alienList.remove(self)

        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False)
        for bullet in collisionsBullet:
            # particle_show()
            #particle_start(self.rect.centerx, self.rect.centery)
            if player.lives > 0:
                self.lives -= 1
                bulletList.remove(bullet)
                if self.lives < 0:
                    big_alienList.remove(self)
                    aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            self.lives -= 1
            if self.lives < 0:
                big_alienList.remove(self)
                player.lives -= 1

    def show(self):
        if lvl > 4:
            if self.chance == 3:
                window.blit(a3[self.lives], (self.rect.x, self.rect.y))


for _ in range(n_bgA):
    alienBig = BigAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    big_alienList.append(alienBig)


class ShootAlien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = a4
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.chance = random.randint(1,2)
        self.rate = 0

    def move(self):
        if lvl > 2:
            if self.chance == 2:
                self.rect.x -= self.speed
                if self.rect.x < window.get_width():
                    alien_shoot()
                    alien_bullet_check()

    def update(self):

        global aliensKilled

        if self.rate > 0:
            self.rate -= 1

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
        for _ in collisionsRock:
            shoot_alienList.remove(self)

        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False)
        for bullet in collisionsBullet:
            # particle_show()
            #particle_start(self.rect.centerx, self.rect.centery)
            if player.lives > 0:
                bulletList.remove(bullet)
                shoot_alienList.remove(self)
                aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            shoot_alienList.remove(self)
            player.lives -= 1

    def show(self):
        if lvl > 2:
            if self.chance == 2:
                window.blit(self.image, (self.rect.x, self.rect.y))

for _ in range(n_sA):
    alienShoot = ShootAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    shoot_alienList.append(alienShoot)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.sprites = [] #disabling animation for now
        # self.sprites.append(l1)
        # self.sprites.append(l2)
        #self.current_sprite = 0
        #self.image = self.sprites[self.current_sprite]
        self.image = l1
        self.image2 = pygame.image.load('assets/opening.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect.center = (x, y)
        self.rect2.center = (x, y)
        self.speed = 2
        self.pos = random.randint(200, 560)

    def update(self):
        slowdown = random.randint(1, 2)
        self.speed += lvl/8

        if self.speed > 5.5:
            if slowdown == 1:
                self.speed = 3.5

    def moveLR(self):
        self.rect.x += self.speed
        self.rect2.x += self.speed

    def moveRL(self):
        self.rect.x = (self.rect.x * -1) + self.speed
        self.rect2.x = (self.rect2.x * -1) + self.speed
        self.pos = random.randint(200, 560)

    def show(self):
        # disabling animation for now
        #self.current_sprite += 0
        # if self.current_sprite > 1:
        #self.current_sprite = 0
        #self.image = self.sprites[int(self.current_sprite)]
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.image2, (self.rect2.x, self.pos))


laser = Laser(1, round(window.get_height()/2))


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rockRandom)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.chanceV = random.randint(1, 2)

    def update(self):
        x = 0
        y = 0

        if self.chanceV == 1:
            y = -self.speed
            x = self.speed

        if self.chanceV == 2:
            y = self.speed
            x = self.speed

        if self.rect.y + y > 1300:
            self.rect.y = -100

        self.rect.x += x
        self.rect.y += y

    def show(self):
        if rock.rect.x < window.get_width()+100 and rock.rect.x > -100 and rock.rect.y > 50 and rock.rect.y < window.get_height()-100:
            window.blit(self.image, (self.rect.x, self.rect.y))


for i in range(2, 4):
    x = random.randint(-window.get_width()+200, window.get_width()+100)
    y = random.randint(window.get_height()-200, window.get_height()+100)

    rock = Rock(x, y, random.randint(1, 3))
    rockList.append(rock)

''' UNDER DEVELOPMENT
class Bomb(pygame.sprite.Sprite): #
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bm
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.timer = 20
        self.velo = 2

    def update(self):
        if self.timer > 0:
            self.timer -= 1

        if self.velo == 2:
            self.velo -= 0.01

    def throw(self):
        if self.timer <= 0:
            self.timer = 20
            self.rect.x += (player.directionx * self.velo)
            self.velo = 2
    
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Particle():
    def __init__(self, x, y, dx, dy, radius, color, d=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.d = d
        self.radius = radius
        self.color = color

    def render(self, window):
        pChance = random.randint(1, 4)
        if pChance == 1:
            self.x += self.dx
            self.y += self.dy
        if pChance == 2:
            self.x += self.dx
            self.y -= self.dy
        if pChance == 3:
            self.x -= self.dx
            self.y += self.dy
        if pChance == 4:
            self.x -= self.dx
            self.y -= self.dy

        if self.d is not None:
            self.dx += self.d

        self.radius -= 0.1
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


def particle_show():
    for particle in particleList:
        particle.render(window)


def particle_start(x, y):
    for _ in range(random.randint(5, 10)):
        particle = Particle(x, y, random.randint(0, 15), random.randint(-30, -5),
                            random.randint(1, 4), random.choice(particleColors), 0.2)
        particleList.append(particle)

        if len(particleList) == 20:
            particleList.clear()
            return

'''

# game loop

def main():

    global lvl, nA, n_bA, n_bgA, n_sA, bulletList, alienList, blue_alienList, big_alienList, alien_bulletList,aliensKilled, alien, alienBlue, alienBig, alienShoot, laser, player, laserNUM, rock

    # game variables
    gamePause = False
    gameOver = False
    gameStart = False

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1
    scroll = 0

    moveR = False
    moveL = False
    moveU = False
    moveD = False
    shoot = False

    while True:

        if gameStart == False:
            window.blit(start_bg, (0, 0))

            if playButton.draw():
                gameStart = True

            if quitButton.draw():
                pygame.quit()
                sys.exit()

        if gameOver == True:
            gameStart = False
            window.blit(over_bg, (0, 0))
            menu("YOU DIED...", font, mColor, round(window.get_width()/2)-110, (window.get_height()/2)-150)
            menu("GAME OVER", font, mColor, round(window.get_width()/2)-110, (window.get_height()/2)-70)

            # if play_overButton.draw():
            #gameStart = True

            if quit_overButton.draw():
                pygame.quit()
                sys.exit()

        if gamePause == True:
            if gameOver == True:
                pass
            else:
                window.blit(menu_bg, (0, 0))
                menu("PAUSE MENU", font, mColor, round(window.get_width()/2)-130, (window.get_height()/2)-200)

                if play_pauseButton.draw():
                    gamePause = False

                if quit_pauseButton.draw():
                    pygame.quit()
                    sys.exit()

        if gameStart == True and gamePause == False:

            if player.lives <= 0:
                gameOver = True
                gameStart = False

            for i in range(0, tiles):
                window.blit(bg, (i*bg.get_width() + scroll, 0))

            scroll -= 5
            if abs(scroll) > bg.get_width():
                scroll = 0

            clock.tick()
            menu(f"FPS: {int(clock.get_fps())}", font2, mColor, 75, 20)

            HEALTH.show()

            menu(f"ALIENS KILLED: {aliensKilled}", font2, mColor, window.get_width()-220, window.get_height()-50)
            menu(f"LEVEL: {lvl}", font2, mColor, 50, window.get_height()-50)

            if len(alienList) == 0:
                lvl += 1
                nA += 1
                n_bA += 1

                if lvl > 2:
                    n_sA += 1
                    if n_sA > 5:
                        n_sA = 1

                if lvl > 4:
                    n_bgA += 1
                    if n_bgA > 5:
                        n_bgA = 0

                for _ in range(nA):
                    alien = Alien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                    alienList.append(alien)

                for _ in range(n_bA):
                    alienBlue = BlueAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                    blue_alienList.append(alienBlue)

                if lvl > 4:
                    for _ in range(n_bgA):
                        alienBig = BigAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                        big_alienList.append(alienBig)

                if lvl > 2:
                    for _ in range(n_sA):
                        alienShoot = ShootAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                        shoot_alienList.append(alienShoot)

                laser.update()

            laser.show()
            laser.moveLR()
            if laser.rect2.x >= window.get_width() and laser.rect.x >= window.get_width():
                laser.moveRL()
                #print(log.rect.x, log.rect2.x)

            for rock in rockList:
                rock.show()
                rock.update()

                if player.lives > 0:

                    if len(rockList) < 3:
                        for i in range(1, random.randint(4, 6)):
                            x = random.randint(-window.get_width()+200, window.get_width()+100)
                            y = random.randint(window.get_height()-200, window.get_height()+300)

                            rock = Rock(x, y, random.randint(1, 3))
                            rockList.append(rock)

                if rock.rect.x > window.get_width()+800 or rock.rect.x < -100 and rock.rect.y > window.get_height()+1200 or rock.rect.y < -100:
                    rockList.remove(rock)

            player.update()
            player.show()
            player.move(moveR, moveL, moveU, moveD)

            if player.lives <= 6 and player.lives > 0:
                if shoot:
                    bullet_move()
                    bullet_check()

            for bullet in bulletList:
                bullet.update()
                bullet.show()

            for alien in alienList:
                alien.show()
                alien.update()
                alien.move()
                if player.lives > 0:
                    if alien.rect.x + alien.image.get_width() < 64:
                        player.lives -= 1
                        alienList.remove(alien)
            
            for alienBlue in blue_alienList:
                alienBlue.show()
                alienBlue.update()
                alienBlue.move()

                if player.lives > 0:
                    if alienBlue.rect.x + alienBlue.image.get_width() < 64:
                        player.lives -= 1
                        blue_alienList.remove(alienBlue)

            for alienBig in big_alienList:
                alienBig.show()
                alienBig.update()
                alienBig.move()

                if player.lives > 0:
                    if alienBig.rect.x + alienBig.image.get_width() < 64:
                        player.lives -= 1
                        big_alienList.remove(alienBig)


            for alien_bullet in alien_bulletList:
                alien_bullet.update()
                alien_bullet.show()

            for alienShoot in shoot_alienList:
                alienShoot.show()
                alienShoot.update()
                alienShoot.move()

                if player.lives > 0:
                    if alienShoot.rect.x + alienShoot.image.get_width() < 64:
                        player.lives -= 1
                        shoot_alienList.remove(alienShoot)

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

        pygame.mouse.set_cursor(
            (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        cX, cY = pygame.mouse.get_pos()
        pos = [cX, cY]
        window.blit(cursor, pos)

        pygame.display.update()
        clock.tick(60)


main()
