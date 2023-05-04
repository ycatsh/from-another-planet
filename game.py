import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import sys
import random
import math
from pygame.locals import *
from funcs import *
from assets import *
from buttons import *

clock = pygame.time.Clock()


# game state 
def init_game():

    global game_variables, playButton, quitButton, player, health, laser, tiles, EXPLOSION_FRAME_EVENT

    game_variables = GameVariables()
    
    playButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40)
    quitButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140)

    player = Player(round(window.get_width()/2), round(window.get_height()/2), 5)
    health = HealthBar(lives[player.lives], round(window.get_width()/2), window.get_height()-45, 0.7)

    add_alien(Alien, game_variables.NUM_ALIENS, game_variables.alienList)
    add_alien(BlueAlien, game_variables.NUM_BLUE_ALIENS, game_variables.blue_alienList)
    add_alien(BigAlien, game_variables.NUM_BIG_ALIENS, game_variables.big_alienList)
    add_alien(ShootAlien, game_variables.NUM_SHOOTING_ALIENS, game_variables.shoot_alienList)

    laser = Laser(1, round(window.get_height()/2))
    add_rocks(Rock, game_variables.rockList)

    EXPLOSION_FRAME_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(EXPLOSION_FRAME_EVENT, 50)

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1


# game variables and constants
class GameVariables:
    def __init__(self):
        self.NUM_ALIENS = 4  
        self.NUM_BLUE_ALIENS = 2 
        self.NUM_BIG_ALIENS = 1  
        self.NUM_SHOOTING_ALIENS = 2 

        self.scroll = 0

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


class Player:
    def __init__(self, x, y, location):
        self.reset(x, y, location)

    def update(self):
        if self.rate > 0:
            self.rate -= 1

        mXY = pygame.mouse.get_pos()
        angle = math.atan2(mXY[1]-self.rect.centery, mXY[0]-self.rect.centerx)*180/math.pi
        self.rotated_image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            self.lives = 0

        collisionsLaser = pygame.Rect.colliderect(self.rect, laser.rect)
        if collisionsLaser:
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
        
    def reset(self, x, y, location):
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
            game_variables.alienList.remove(self)
            player.lives -= 1

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


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
                    shoot(AlienBullet, player, self, game_variables.alien_bulletList, enemy=True)
                    bullet_check(game_variables.alien_bulletList)

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


class Rock:
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rockRandom)
        self.tmp_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = 10
        self.lives = 5
        self.directionx = random.choice([1, -1])
        self.directiony = random.choice([1, -1])
        self.explosion_index = 0

    def explode(self, radius, frames):
        if self.lives <= 0:
            explosionX = self.rect.x + self.image.get_width() // 2 - radius
            explosionY = self.rect.y + self.image.get_height() // 2 - radius
            window.blit(frames[self.explosion_index], (explosionX, explosionY))

            self.explosion_index += 1
            if self.explosion_index >= len(frames)-1:
                game_variables.rockList.remove(self)

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

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            game_variables.bulletList.remove(bullet)
            self.lives -= 1            

    def show(self):
        window.blit(self.tmp_image, (self.rect.x, self.rect.y))


def main():

    init_game()

    while True:
        if not game_variables.gameStart:
            window.blit(start_bg, (0, 0))
            if playButton.draw():
                game_variables.gameStart = True

            if quitButton.draw():
                pygame.quit()
                sys.exit()

        if game_variables.gameOver:
            window.blit(over_bg, (0, 0))
            text("YOU DIED...", round(window.get_width()/2)-110, (window.get_height()/2)-150)
            text("GAME OVER", round(window.get_width()/2)-110, (window.get_height()/2)-70)

            if playButton.draw():
                game_variables.gameOver = False
                init_game()

            if quitButton.draw():
                pygame.quit()
                sys.exit()

        if game_variables.gamePause:
            if not game_variables.gameOver:
                window.blit(menu_bg, (0, 0))
                text("PAUSE MENU", round(window.get_width()/2)-130, (window.get_height()/2)-200)

                if playButton.draw():
                    game_variables.gamePause = False

                if quitButton.draw():
                    pygame.quit()
                    sys.exit()

        if game_variables.gameStart and not game_variables.gamePause:

            change_cursor()

            if player.lives <= 0:
                game_variables.gameOver = True
                game_variables.gameStart = False

            for i in range(0, tiles):
                window.blit(bg, (i*bg.get_width() + game_variables.scroll, 0))

            game_variables.scroll -= 5
            if abs(game_variables.scroll) > bg.get_width():
                game_variables.scroll = 0

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

                add_alien(Alien, game_variables.NUM_ALIENS, game_variables.alienList)

                add_alien(BlueAlien, game_variables.NUM_BLUE_ALIENS, game_variables.blue_alienList)

                if game_variables.lvl > 4:
                    add_alien(BigAlien, game_variables.NUM_BIG_ALIENS, game_variables.big_alienList)

                if game_variables.lvl > 2:
                    add_alien(ShootAlien, game_variables.NUM_SHOOTING_ALIENS, game_variables.shoot_alienList)

                laser.update()

            laser.show()
            laser.moveLR()
            if laser.rect.x >= window.get_width()+200:
                laser.moveRL()

            for rock in game_variables.rockList:
                rock.show()
                rock.update()
                if rock.lives <= 0:
                    rock.explode(100, explosion_frames)

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
                    shoot(Bullet, player, "", game_variables.bulletList, enemy=False) #alien param here doesn't matter
                    bullet_check(game_variables.bulletList)

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

            health.show()
            clock.tick()
            
            text(f"FPS: {int(clock.get_fps())}", 75, 20, small=True)
            text(f"ALIENS KILLED: {game_variables.aliensKilled}", window.get_width()-220, window.get_height()-50, small=True)
            text(f"LEVEL: {game_variables.lvl}", 50, window.get_height()-50, small=True)

        else:
            show_cursor()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == EXPLOSION_FRAME_EVENT:
                for rock in game_variables.rockList:
                    if rock.lives <= 0:
                        rock.explosion_index += 1

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
    main()