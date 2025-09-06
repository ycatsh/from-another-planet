import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random
import math
import sys

import pygame
from pygame.locals import *

from from_another_planet import *
from from_another_planet.player import *
from from_another_planet.aliens import *
from from_another_planet.laser import *
from from_another_planet.rock import *
from from_another_planet.bullet import *
from from_another_planet.helper.animate import *
from from_another_planet.helper.effects import *
from from_another_planet.helper.config import *
from from_another_planet.menus.buttons import *
from from_another_planet.menus.menus import *
from from_another_planet.helper.shoot import *


clock = pygame.time.Clock()

# Game variables and constants
class GameVariables:
    def __init__(self):
        self.NUM_ALIENS = 4  
        self.NUM_BLUE_ALIENS = 2 
        self.NUM_BIG_ALIENS = 1  
        self.NUM_SHOOTING_ALIENS = 1
        self.NUM_TELEPORT_PARTICLES = 50

        self.scroll = 0

        self.lvl = 1
        self.aliensKilled = 0
        self.cause_of_death = ""

        self.alienList = []
        self.blue_alienList = []
        self.big_alienList = []
        self.shoot_alienList = []
        self.alien_bulletList = []
        self.laserList = []
        self.rockList = []
        self.bulletList = []
        self.shellList = []

        self.screen_effects = ScreenEffects()
        self.teleportParticles = []
        self.explosionParticles = []

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


## Initialize game state 
def init_game():
    global game_vars, buttons, player, health, laser, tiles
    game_vars = GameVariables()

    newgButton = Button(bN, bNc, round(window.get_width() / 2), round(window.get_height() / 2) + 80)
    resuButton = Button(bR, bRc, round(window.get_width() / 2), round(window.get_height() / 2) + 80)
    tutoButton = Button(bT, bTc, round(window.get_width() / 2), round(window.get_height() / 2) + 180)
    quitButton = Button(bQ, bQc, round(window.get_width() / 2), round(window.get_height() / 2) + 280)
    buttons = [newgButton, tutoButton, quitButton, resuButton]

    player = Player(p, round(window.get_width() / 2), round(window.get_height() / 2), 6)
    health = HealthBar(lives[player.lives], round(window.get_width() / 2), (window.get_height() - 45), 0.7)

    add_alien(Alien, a, game_vars.NUM_ALIENS, game_vars.alienList)
    add_alien(BlueAlien, a2, game_vars.NUM_BLUE_ALIENS, game_vars.blue_alienList)
    add_alien(BigAlien, a3, game_vars.NUM_BIG_ALIENS, game_vars.big_alienList)
    add_alien(ShootAlien, a4, game_vars.NUM_SHOOTING_ALIENS, game_vars.shoot_alienList)

    laser = Laser(l, 1, round(window.get_height() / 2))
    add_rocks(8, Rock, rockRandom, game_vars.rockList, min_speed=1, max_speed=3)

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1


def main():
    global game_vars, buttons, player, health, laser, tiles
    init_game()

    while True:
        shake_offset = game_vars.screen_effects.screenshake()
        screen_offset = game_vars.screen_effects.screenshake(window=True)
        window.fill((0, 0, 0))

        # Menus 
        if not game_vars.gameOver and not game_vars.gameStart:
            main_menu(game_vars, buttons[0], buttons[1], buttons[2])
        if game_vars.gameOver:
            reset_menu(game_vars, buttons[0], buttons[1], buttons[2], init_game)
        if game_vars.gamePause:
            pause_menu(game_vars, buttons[3], buttons[1], buttons[2])
        if game_vars.gameStart and not game_vars.gamePause:
            change_cursor()

            if player.lives <= 0:
                game_vars.gameOver = True
                game_vars.gameStart = False

            # Scrolling background
            for i in range(0, tiles):
                window.blit(bg, (i * bg.get_width() + game_vars.scroll + screen_offset[0], screen_offset[1]))

            game_vars.scroll -= 5
            if abs(game_vars.scroll) > bg.get_width():
                game_vars.scroll = 0

            # Level up
            if len(game_vars.alienList) == 0:
                change_level(game_vars)
                add_alien(Alien, a, game_vars.NUM_ALIENS, game_vars.alienList)
                add_alien(BlueAlien, a2, game_vars.NUM_BLUE_ALIENS, game_vars.blue_alienList)
                if game_vars.lvl > 2:
                    add_alien(ShootAlien, a4, game_vars.NUM_SHOOTING_ALIENS, game_vars.shoot_alienList)
                if game_vars.lvl > 4:
                    add_alien(BigAlien, a3, game_vars.NUM_BIG_ALIENS, game_vars.big_alienList)
                laser.update(game_vars)

            # Laser
            laser.show(window, shake_offset)
            laser.moveLR(window, player)
            if laser.rect.x >= window.get_width()+200:
                laser.reset()

            # Rock
            game_vars.rockList = [rock for rock in game_vars.rockList if not rock.remove]
            for rock in game_vars.rockList: 
                rock.update(window)
                rock.show(window, shake_offset)
                rock.collide(window, game_vars, laser)
            if len(game_vars.rockList) < 4:
                add_rocks(random.randint(8, 10), Rock, rockRandom, game_vars.rockList, min_speed=2, max_speed=6)

            for explosion in game_vars.explosionParticles:
                explosion.update()
                explosion.show()
            game_vars.explosionParticles = RockExplosion.cleanup(game_vars.explosionParticles)

            # Player
            player.move(window, game_vars.moveR, game_vars.moveL, game_vars.moveU, game_vars.moveD)
            player.update(game_vars.telep, game_vars)
            player.collide(game_vars, laser)
            player.show(window, shake_offset)

            for particle in game_vars.teleportParticles:
                particle.update(clock.get_time())
                particle.show()
            game_vars.teleportParticles = TeleportAnimation.cleanup(game_vars.teleportParticles)

            # Shooting
            bullet_check(game_vars.bulletList, window)
            if game_vars.shoot:
                player_shoot(Bullet, player, game_vars.bulletList, game_vars.screen_effects)
                game_vars.screen_effects.shake_duration = 5
                game_vars.shoot = False
            if game_vars.shotg:
                player_shotgun(Shell, player, game_vars.bulletList, game_vars.screen_effects)
                game_vars.screen_effects.shake_duration = 10
            for bullets in game_vars.bulletList:
                    bullets.update()
                    bullets.show(window)
            game_vars.screen_effects.update_recoil(player)

            # Aliens
            for alien in game_vars.alienList:
                alien.show(window, shake_offset)
                alien.update(player, game_vars)
                alien.move()
                reduce_life_edge(player, alien, game_vars.alienList)
            
            for alienBlue in game_vars.blue_alienList:
                alienBlue.show(window, shake_offset)
                alienBlue.update(player, game_vars)
                alienBlue.move()
                reduce_life_edge(player, alienBlue, game_vars.blue_alienList)

            for alienBig in game_vars.big_alienList:
                alienBig.show(window, a3, shake_offset)
                alienBig.update(player, game_vars)
                alienBig.move()
                reduce_life_edge(player, alienBig, game_vars.big_alienList)

            for alien_bullet in game_vars.alien_bulletList:
                alien_bullet.update(player, game_vars)
                alien_bullet.show(window)
            for alienShoot in game_vars.shoot_alienList:
                alienShoot.show(window, shake_offset)
                alienShoot.update(player, game_vars)
                alienShoot.move(player, window, game_vars)
                reduce_life_edge(player, alienShoot, game_vars.shoot_alienList)

            health.show(window, lives, player)
            clock.tick()
            ui(clock, player, game_vars)
        else:
            show_cursor()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Keys
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_vars.gamePause = True
                if event.key == K_RIGHT or event.key == K_d:
                    game_vars.moveR = True
                if event.key == K_LEFT or event.key == K_a:
                    game_vars.moveL = True
                if event.key == K_UP or event.key == K_w:
                    game_vars.moveU = True
                if event.key == K_DOWN or event.key == K_s:
                    game_vars.moveD = True
                if event.key == K_SPACE:
                    game_vars.telep = True   

            if not (game_vars.moveR or game_vars.moveL or game_vars.moveU or game_vars.moveD):
                player.slowdown()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_vars.shoot = True
                gun_channel.play(gun_sound)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game_vars.shoot = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game_vars.shotg = True 
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                game_vars.shotg = False

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    game_vars.moveR = False
                if event.key == K_LEFT or event.key == K_a:
                    game_vars.moveL = False
                if event.key == K_UP or event.key == K_w:
                    game_vars.moveU = False
                if event.key == K_DOWN or event.key == K_s:
                    game_vars.moveD = False
                if event.key == K_SPACE:
                    game_vars.telep = False

        if not game_vars.gamePause and not game_vars.gameOver and game_vars.gameStart:
            change_cursor()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
