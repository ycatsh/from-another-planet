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
from menus import *

clock = pygame.time.Clock()


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
        self.shellList = []

        self.gamePause = False
        self.gameOver = False
        self.gameStart = False

        self.moveR = False
        self.moveL = False
        self.moveU = False
        self.moveD = False
        self.shoot = False
        self.shotg = False
        self.telep = False


class Player:
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = p
        self.lives = 6
        self.charge = "NOT ACTIVATED"
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.rate = 0
        self.srate = 0
        self.gun = False
        self.next_teleport = 10

    def update(self, telep):
        if self.rate > 0:
            self.rate -= 1

        if self.srate > 0:
            self.srate -= 1

        if game_variables.aliensKilled >= 30:
            self.gun = True

        mXY = pygame.mouse.get_pos()

        if game_variables.aliensKilled > 0:
            if game_variables.aliensKilled >= self.next_teleport:
                self.charge = "ACTIVATED"
                hide_cursor()
                teleport_cursor()
                if telep:
                    self.next_teleport = game_variables.aliensKilled + 10
                    self.rect.x = mXY[0]
                    self.rect.y = mXY[1]
            else:
                self.charge = "NOT ACTIVATED"
    
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
            x = self.speed
            
        if moveL:
            x = -self.speed

        if moveU:
            y = -self.speed

        if moveD:
            y = self.speed

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
        self.movement = True

    def show(self):
        window.blit(self.rotated_image, self.rect)


class HealthBar:
    def __init__(self, image, x, y, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
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

    def rotate(self, angle):
        self.rotated_image = pygame.transform.rotate(self.image, -math.degrees(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def show(self):
        window.blit(self.rotated_image, (self.rect.x, self.rect.y))


class AlienBullet:
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = a_b
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
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


class Shell(Bullet):
    def __init__(self, x, y, dx, dy, angle):
        super().__init__(x, y, dx, dy)
        self.angle = angle
      

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
            game_variables.alienList.remove(self) if self in game_variables.alienList else None

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                game_variables.bulletList.remove(bullet)
                game_variables.alienList.remove(self) if self in game_variables.alienList else None
                game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.alienList.remove(self) if self in game_variables.alienList else None
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
            game_variables.blue_alienList.remove(self) if self in game_variables.blue_alienList else None

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                game_variables.bulletList.remove(bullet)
                game_variables.blue_alienList.remove(self) if self in game_variables.blue_alienList else None
                game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.blue_alienList.remove(self) if self in game_variables.blue_alienList else None
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
            game_variables.big_alienList.remove(self) if self in game_variables.big_alienList else None

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                self.lives -= 1
                game_variables.bulletList.remove(bullet)
                if self.lives < 0:
                    game_variables.big_alienList.remove(self) if self in game_variables.big_alienList else None
                    game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            self.lives -= 1
            if self.lives < 0:
                game_variables.big_alienList.remove(self) if self in game_variables.big_alienList else None
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
                    shoot(AlienBullet, player, self, game_variables.alien_bulletList, bullet_type='enemy')
                    bullet_check(game_variables.alien_bulletList)

    def update(self):
        if self.rate > 0:
            self.rate -= 1

        collisionsRock = pygame.sprite.spritecollide(self, game_variables.rockList, False)
        for _ in collisionsRock:
            game_variables.shoot_alienList.remove(self) if self in game_variables.shoot_alienList else None

        collisionsBullet = pygame.sprite.spritecollide(self, game_variables.bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                game_variables.bulletList.remove(bullet)
                game_variables.shoot_alienList.remove(self) if self in game_variables.shoot_alienList else None
                game_variables.aliensKilled += 1

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect)
        if collisionsPlayer:
            game_variables.shoot_alienList.remove(self) if self in game_variables.shoot_alienList else None
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

        if self.speedx > 8 or self.speedy > 8:
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

        other_rocks = []
        for rock in game_variables.rockList:
            if rock != self:
                other_rocks.append(rock)

        collisionsRock = pygame.sprite.spritecollide(self, other_rocks, False)
        for rock in collisionsRock:
            self.lives -= 1
            rock.lives -= 1

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

    global game_variables, buttons, player, health, laser, tiles, EXPLOSION_FRAME_EVENT

    game_variables = GameVariables()
    
    newgButton = Button(bN, bNc, round(window.get_width()/2), round(window.get_height()/2)+80)
    resuButton = Button(bR, bRc, round(window.get_width()/2), round(window.get_height()/2)+80)
    tutoButton = Button(bT, bTc, round(window.get_width()/2), round(window.get_height()/2)+180)
    quitButton = Button(bQ, bQc, round(window.get_width()/2), round(window.get_height()/2)+280)

    buttons = [newgButton, tutoButton, quitButton, resuButton]

    player = Player(round(window.get_width()/2), round(window.get_height()/2), 5)
    health = HealthBar(lives[player.lives], round(window.get_width()/2), window.get_height()-45, 0.7)

    add_alien(Alien, game_variables.NUM_ALIENS, game_variables.alienList)
    add_alien(BlueAlien, game_variables.NUM_BLUE_ALIENS, game_variables.blue_alienList)
    add_alien(BigAlien, game_variables.NUM_BIG_ALIENS, game_variables.big_alienList)
    add_alien(ShootAlien, game_variables.NUM_SHOOTING_ALIENS, game_variables.shoot_alienList)

    laser = Laser(1, round(window.get_height()/2))
    add_rocks(4, Rock, game_variables.rockList, 1, 3)

    EXPLOSION_FRAME_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(EXPLOSION_FRAME_EVENT, 50)

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1

    while True:

        if not game_variables.gameOver and not game_variables.gameStart:
            main_menu(game_variables, buttons[0], buttons[1], buttons[2])

        if game_variables.gameOver:
            window.blit(menu_bg, (0, 0))
            window.blit(over_logo, ((window.get_width()/2)-300, (window.get_height()/2)-400))

            if buttons[0].pressed(): #reset game
                game_variables = GameVariables()
                newgButton = Button(bN, bNc, round(window.get_width()/2), round(window.get_height()/2)+80)
                resuButton = Button(bR, bRc, round(window.get_width()/2), round(window.get_height()/2)+80)
                tutoButton = Button(bT, bTc, round(window.get_width()/2), round(window.get_height()/2)+180)
                quitButton = Button(bQ, bQc, round(window.get_width()/2), round(window.get_height()/2)+280)
                buttons = [newgButton, tutoButton, quitButton, resuButton]
                player = Player(round(window.get_width()/2), round(window.get_height()/2), 5)
                health = HealthBar(lives[player.lives], round(window.get_width()/2), window.get_height()-45, 0.7)
                add_alien(Alien, game_variables.NUM_ALIENS, game_variables.alienList)
                add_alien(BlueAlien, game_variables.NUM_BLUE_ALIENS, game_variables.blue_alienList)
                add_alien(BigAlien, game_variables.NUM_BIG_ALIENS, game_variables.big_alienList)
                add_alien(ShootAlien, game_variables.NUM_SHOOTING_ALIENS, game_variables.shoot_alienList)
                laser = Laser(1, round(window.get_height()/2))
                add_rocks(4, Rock, game_variables.rockList, 1, 3)
                EXPLOSION_FRAME_EVENT = pygame.USEREVENT + 1
                pygame.time.set_timer(EXPLOSION_FRAME_EVENT, 50)
                tiles = math.ceil(window.get_width() / bg.get_width()) + 1

            if buttons[1].pressed():
                pass
            if buttons[2].pressed():
                pygame.quit()
                sys.exit()

        if game_variables.gamePause:
            pause_menu(game_variables, buttons[3], buttons[1], buttons[2])

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
                change_level(game_variables)

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
                if rock.lives > 0:
                    rock.show()
                    rock.update()
                else:
                    rock.explode(100, explosion_frames)

                if len(game_variables.rockList) < 3:
                    add_rocks(random.randint(6, 8), Rock, game_variables.rockList, 2, 6)

            player.update(game_variables.telep)
            player.move(game_variables.moveR, game_variables.moveL, game_variables.moveU, game_variables.moveD)
            player.show()

            if player.lives <= 6 and player.lives > 0:
                bullet_check(game_variables.bulletList)

                if game_variables.shoot:
                    shoot(Bullet, player, "", game_variables.bulletList, bullet_type='bullet') #alien param here doesn't matter

                if game_variables.shotg:
                    shoot(Shell, player, "", game_variables.bulletList, bullet_type='shotgun')

            for bullets in game_variables.bulletList:
                    bullets.update()
                    bullets.show()

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
            
            ui(clock, player, game_variables)

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
                if event.key == K_SPACE:
                    game_variables.telep = True   

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #shoot_sound.play()
                game_variables.shoot = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game_variables.shotg = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game_variables.shoot = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                game_variables.shotg = False

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    game_variables.moveR = False
                if event.key == K_LEFT or event.key == K_a:
                    game_variables.moveL = False
                if event.key == K_UP or event.key == K_w:
                    game_variables.moveU = False
                if event.key == K_DOWN or event.key == K_s:
                    game_variables.moveD = False
                if event.key == K_SPACE:
                    game_variables.telep = False

        if not game_variables.gamePause and not game_variables.gameOver and game_variables.gameStart:
            change_cursor()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()