import pygame
import sys
from pygame.locals import *
import random
import math

clock = pygame.time.Clock()
pygame.init()

# window
windowSize = 1920,1080
window = pygame.display.set_mode((windowSize), pygame.FULLSCREEN|SCALED, vsync=1)

# icons
icon = pygame.image.load('assets/icon.png').convert_alpha()
pygame.display.set_caption("From Another Planet")
pygame.display.set_icon(icon)

# fonts
menuFont = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 100)
font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 60)
font2 = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 30)
COLOR = (110, 69, 206)

# game variables and constants
class GameVariables:
    def __init__(self):
        self.NUM_ALIENS = 4  
        self.NUM_BLUE_ALIENS = 2 
        self.NUM_BIG_ALIENS = 1  
        self.NUM_SHOOTING_ALIENS = 2 

        self.lvl = 1
        self.aliensKilled = 0

        self.alienList = []
        self.blue_alienList = []
        self.big_alienList = []
        self.shoot_alienList = []
        self.alien_bulletList = []
        self.laserList = []
        self.rockList = []
        self.bulletList = []

        self.gamePause = False
        self.gameOver = False
        self.gameStart = False

        self.moveR = False
        self.moveL = False
        self.moveU = False
        self.moveD = False
        self.shoot = False

game_variables = GameVariables()


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


class Player:
    def __init__(self, x, y, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = p
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

        mXY = pygame.mouse.get_pos()
        angle = 360-math.atan2(mXY[1]-300, mXY[0]-400)*180/math.pi

        image = self.image.copy()
        self.rotated_image = pygame.transform .rotate(image, angle)

        angle += 1 % 360 

        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            if self.lives != 0:
                self.lives = 0

        collisionsLaser = pygame.Rect.colliderect(self.rect, laser.rect)
        if collisionsLaser:
            if self.lives != 0:
                self.lives = 0

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

        if self.rect.bottom + y > window.get_height()-81:
            y = window.get_height()-81 - self.rect.bottom

        if self.rect.top + y < 81:
            y = 5

        if self.rect.left + x > window.get_width()-20:
            x = window.get_width()-20 - self.rect.left

        if self.rect.right + x <= 20:
            x = 20 - self.rect.right

        self.rect.x += x
        self.rect.y += y

    def show(self):
        window.blit(pygame.transform.flip(
            self.rotated_image, False, False), self.rect)

player = Player(round(window.get_width()/2), round(window.get_height()/2), 5)

lives = [pygame.image.load(f'assets/health/{i}.png').convert_alpha() for i in range(7)]


class HealthBar:
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


class Bullet:
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = b
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
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

    speedX = int(16 * math.cos(angle))
    speedY = int(16 * math.sin(angle))

    if player.rate == 0:
        player.rate = 20
        game_variables.bulletList.append(Bullet(player.rect.centerx, player.rect.centery, speedX, speedY))

def bullet_check():
    if not len(game_variables.bulletList) == 0:
        game_variables.bulletList[:] = [bullet for bullet in game_variables.bulletList if bullet.rect.x >= 0 and bullet.rect.x <= window.get_width() and bullet.rect.y >= 60 and bullet.rect.y <= window.get_height()-60]


class AlienBullet:
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = a_b
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 6
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.alien_bulletList.remove(self)
            player.lives -= 1

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

def alien_shoot():
    freq = random.randint(50, 175)

    pX, pY = player.rect.x, player.rect.y

    distanceX = pX - alienShoot.rect.x
    distanceY = pY - alienShoot.rect.y

    angle = math.atan2(distanceY, distanceX)

    speedX = int(10 * math.cos(angle))
    speedY = int(10 * math.sin(angle))

    if alienShoot.rate == 0:
        alienShoot.rate = freq
        game_variables.alien_bulletList.append(AlienBullet(alienShoot.rect.centerx, alienShoot.rect.centery, speedX, speedY))

def alien_bullet_check():
    if not len(game_variables.alien_bulletList) == 0:
        game_variables.alien_bulletList[:] = [alien_bullet for alien_bullet in game_variables.alien_bulletList if alien_bullet.rect.x >= -20 and alien_bullet.rect.x <= window.get_width()+20 and alien_bullet.rect.y >= 60 and alien_bullet.rect.y <= window.get_height()-60]
                

class Alien:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = a
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def move(self):
        self.rect.x -= self.speed

    def update(self):
        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            game_variables.alienList.remove(self)

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                game_variables.bulletList.remove(bullet)
                game_variables.alienList.remove(self)
                game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.alienList.remove(alien)
            player.lives -= 1

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


for _ in range(game_variables.NUM_ALIENS):
    alien = Alien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    game_variables.alienList.append(alien)


class BlueAlien:
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
        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            game_variables.blue_alienList.remove(self)


        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                game_variables.bulletList.remove(bullet)
                game_variables.blue_alienList.remove(self)
                game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.blue_alienList.remove(self)
            player.lives -= 1

    def show(self):
        if self.chance == 2:
            window.blit(self.image, (self.rect.x, self.rect.y))


for _ in range(game_variables.NUM_BLUE_ALIENS):
    alienBlue = BlueAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    game_variables.blue_alienList.append(alienBlue)


class BigAlien:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 2
        self.image = a3[self.lives]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.chance = random.randint(1, 4)

    def move(self):
        if game_variables.lvl > 4:
            if self.chance == 3:
                self.rect.x -= self.speed

    def update(self):
        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            game_variables.big_alienList.remove(self)

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                self.lives -= 1
                game_variables.bulletList.remove(bullet)
                if self.lives < 0:
                    game_variables.big_alienList.remove(self)
                    game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            self.lives -= 1
            if self.lives < 0:
                game_variables.big_alienList.remove(self)
                player.lives -= 1

    def show(self):
        if game_variables.lvl > 4:
            if self.chance == 3:
                window.blit(a3[self.lives], (self.rect.x, self.rect.y))


for _ in range(game_variables.NUM_BIG_ALIENS):
    alienBig = BigAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    game_variables.big_alienList.append(alienBig)


class ShootAlien:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = a4
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.chance = random.randint(1,2)
        self.rate = 0

    def move(self):
        if game_variables.lvl > 2:
            if self.chance == 2:
                self.rect.x -= self.speed
                if self.rect.x < window.get_width():
                    alien_shoot()
                    alien_bullet_check()

    def update(self):
        if self.rate > 0:
            self.rate -= 1

        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            game_variables.shoot_alienList.remove(self)

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                game_variables.bulletList.remove(bullet)
                game_variables.shoot_alienList.remove(self)
                game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.shoot_alienList.remove(self)
            player.lives -= 1

    def show(self):
        if game_variables.lvl > 2:
            if self.chance == 2:
                window.blit(self.image, (self.rect.x, self.rect.y))

for _ in range(game_variables.NUM_SHOOTING_ALIENS):
    alienShoot = ShootAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
    game_variables.shoot_alienList.append(alienShoot)


class Laser:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = l
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 2
        self.speedy = 2
        self.directiony = random.choice([1, -1])

    def update(self):
        slowdown = random.randint(1, 2)
        self.speedx += game_variables.lvl/8
        self.speedy += game_variables.lvl/12

        if self.speedx > 6 or self.speedy > 6:
            if slowdown == 1:
                self.speedx = 3
                self.speedy = 3


    def moveLR(self):
        self.rect.x += self.speedx

        if self.rect.top < 10:
            self.directiony = 1
        if self.rect.bottom > window.get_height()-10:
            self.directiony = -1

        self.rect.y += self.speedy * self.directiony


    def moveRL(self):
        self.rect.x = (self.rect.x * -1) + self.speedx

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(window, (126, 14, 22), (self.rect.x, self.rect.y), special_flags=BLEND_RGB_ADD)

laser = Laser(1, round(window.get_height()/2))


class Rock:
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rockRandom)
        self.tmp_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = 10
        self.directionx = random.choice([1, -1])
        self.directiony = random.choice([1, -1])

    def update(self):

        self.tmp_image = pygame.transform.rotate(self.image, self.angle)
        self.angle += 1%360

        if self.rect.right < -random.randint(100, 300):
            self.directionx = 1

        if self.rect.right > window.get_width()+random.randint(100, 300):
            self.directionx = -1

        if self.rect.top < -random.randint(100, 300):
            self.directiony = 1

        if self.rect.bottom > window.get_height()+random.randint(100, 300):
            self.directiony = -1

        self.rect.x += self.speed * self.directionx
        self.rect.y += self.speed * self.directiony

        collisionsLaser= pygame.Rect.colliderect(self.rect, laser.rect)
        if collisionsLaser:
            game_variables.rockList.remove(self)

    def show(self):
        window.blit(self.tmp_image, (self.rect.x, self.rect.y))


for i in range(4):
    x = random.choice([random.randint(-window.get_width()+200, -window.get_width()+800), random.randint(window.get_width()+200, window.get_width()+800)])
    y = random.choice([random.randint(window.get_height()+200, window.get_height()+800), random.randint(-window.get_height()+200, -window.get_height()+800)])

    rock = Rock(x, y, random.randint(1, 3))
    game_variables.rockList.append(rock)


# game loop
def main(game_variables):

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1
    scroll = 0

    global alienShoot

    while True:

        if game_variables.gameStart == False:
            window.blit(start_bg, (0, 0))
            if playButton.draw():
                game_variables.gameStart = True

            if quitButton.draw():
                pygame.quit()
                sys.exit()

        if game_variables.gameOver == True:
            game_variables.gameStart = False
            window.blit(over_bg, (0, 0))
            menu("YOU DIED...", font, COLOR, round(window.get_width()/2)-110, (window.get_height()/2)-150)
            menu("GAME OVER", font, COLOR, round(window.get_width()/2)-110, (window.get_height()/2)-70)

            # if play_overButton.draw():
            #gameStart = True

            if quitButton.draw():
                pygame.quit()
                sys.exit()

        if game_variables.gamePause == True:
            if game_variables.gameOver == True:
                pass
            else:
                window.blit(menu_bg, (0, 0))
                menu("PAUSE MENU", font, COLOR, round(window.get_width()/2)-130, (window.get_height()/2)-200)

                if playButton.draw():
                    game_variables.gamePause = False

                if quitButton.draw():
                    pygame.quit()
                    sys.exit()

        if game_variables.gameStart == True and game_variables.gamePause == False:

            change_cursor()

            if player.lives <= 0:
                game_variables.gameOver = True
                game_variables.gameStart = False

            for i in range(0, tiles):
                window.blit(bg, (i*bg.get_width() + scroll, 0))

            scroll -= 5
            if abs(scroll) > bg.get_width():
                scroll = 0

            if len(game_variables.alienList) == 0:
                game_variables.lvl += 1
                game_variables.NUM_ALIENS += 1
                game_variables.NUM_BLUE_ALIENS += 1

                if game_variables.lvl > 2:
                    game_variables.NUM_SHOOTING_ALIENS += 2
                    if game_variables.NUM_SHOOTING_ALIENS > 6:
                        game_variables.NUM_SHOOTING_ALIENS = 3

                if game_variables.lvl > 4:
                    game_variables.NUM_BIG_ALIENS += 1
                    if game_variables.NUM_BIG_ALIENS > 5:
                        game_variables.NUM_BIG_ALIENS = 0

                for _ in range(game_variables.NUM_ALIENS):
                    alien = Alien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                    game_variables.alienList.append(alien)

                for _ in range(game_variables.NUM_BLUE_ALIENS):
                    alienBlue = BlueAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                    game_variables.blue_alienList.append(alienBlue)

                if game_variables.lvl > 4:
                    for _ in range(game_variables.NUM_BIG_ALIENS):
                        alienBig = BigAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                        game_variables.big_alienList.append(alienBig)

                if game_variables.lvl > 2:
                    for _ in range(game_variables.NUM_SHOOTING_ALIENS):
                        alienShoot = ShootAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120)))
                        game_variables.shoot_alienList.append(alienShoot)

                laser.update()

            laser.show()
            laser.moveLR()
            if laser.rect.x >= window.get_width()+200:
                laser.moveRL()

            for rock in game_variables.rockList:
                rock.show()
                rock.update()

                if len(game_variables.rockList) < 3:
                    for i in range(random.randint(4, 6)):
                        x = random.choice([random.randint(-window.get_width()+200, -window.get_width()+800), random.randint(window.get_width()+200, window.get_width()+800)])
                        y = random.choice([random.randint(window.get_height()+200, window.get_height()+800), random.randint(-window.get_height()+200, -window.get_height()+800)])
                        rock = Rock(x, y, random.randint(1, 6))
                        game_variables.rockList.append(rock)

                if len(game_variables.rockList) > 6:
                    game_variables.rockList.remove(rock)

            player.update()
            player.show()
            player.move(game_variables.moveR, game_variables.moveL, game_variables.moveU, game_variables.moveD)

            if player.lives <= 6 and player.lives > 0:
                if game_variables.shoot:
                    bullet_move()
                    bullet_check()

            for bullet in game_variables.bulletList:
                bullet.update()
                bullet.show()

            for alien in game_variables.alienList:
                alien.show()
                alien.update()
                alien.move()
                if player.lives > 0:
                    if alien.rect.x + alien.image.get_width() < 10:
                        player.lives -= 1
                        game_variables.alienList.remove(alien)
            
            for alienBlue in game_variables.blue_alienList:
                alienBlue.show()
                alienBlue.update()
                alienBlue.move()

                if player.lives > 0:
                    if alienBlue.rect.x + alienBlue.image.get_width() < 10:
                        player.lives -= 1
                        game_variables.blue_alienList.remove(alienBlue)

            for alienBig in game_variables.big_alienList:
                alienBig.show()
                alienBig.update()
                alienBig.move()

                if player.lives > 0:
                    if alienBig.rect.x + alienBig.image.get_width() < 10:
                        player.lives -= 1
                        game_variables.big_alienList.remove(alienBig)


            for alien_bullet in game_variables.alien_bulletList:
                alien_bullet.update()
                alien_bullet.show()
                
            for alienShoot in game_variables.shoot_alienList:
                alienShoot.show()
                alienShoot.update()
                alienShoot.move()

                if player.lives > 0:
                    if alienShoot.rect.x + alienShoot.image.get_width() < 64:
                        player.lives -= 1
                        game_variables.shoot_alienList.remove(alienShoot)
           
            clock.tick()
            HEALTH.show()

            menu(f"FPS: {int(clock.get_fps())}", font2, COLOR, 75, 20)
            menu(f"ALIENS KILLED: {game_variables.aliensKilled}", font2, COLOR, window.get_width()-220, window.get_height()-50)
            menu(f"LEVEL: {game_variables.lvl}", font2, COLOR, 50, window.get_height()-50)

        else:
            show_cursor()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_variables.gamePause = True
                if event.key == K_RIGHT or event.key == K_d:
                    game_variables.moveR = True
                if event.key == K_LEFT or event.key == K_a:
                    game_variables.moveL = True
                if event.key == K_UP or event.key == K_w:
                    game_variables.moveU = True
                if event.key == K_DOWN or event.key == K_s:
                    game_variables.moveD = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_variables.shoot = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game_variables.shoot = False

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    game_variables.moveR = False
                if event.key == K_LEFT or event.key == K_a:
                    game_variables.moveL = False
                if event.key == K_UP or event.key == K_w:
                    game_variables.moveU = False
                if event.key == K_DOWN or event.key == K_s:
                    game_variables.moveD = False

        if not game_variables.gamePause and not game_variables.gameOver and game_variables.gameStart:
            change_cursor()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main(game_variables)
