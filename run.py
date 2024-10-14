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
from from_another_planet.views.buttons import *
from from_another_planet.views.menus import *
from from_another_planet.helper.shoot import *

clock = pygame.time.Clock()


# game variables and constants
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
    global game_variables, buttons, player, health, laser, tiles
    game_variables = GameVariables()

    newgButton = Button(bN, bNc, round(window.get_width() / 2), round(window.get_height() / 2) + 80)
    resuButton = Button(bR, bRc, round(window.get_width() / 2), round(window.get_height() / 2) + 80)
    tutoButton = Button(bT, bTc, round(window.get_width() / 2), round(window.get_height() / 2) + 180)
    quitButton = Button(bQ, bQc, round(window.get_width() / 2), round(window.get_height() / 2) + 280)
    buttons = [newgButton, tutoButton, quitButton, resuButton]

    player = Player(p, round(window.get_width() / 2), round(window.get_height() / 2), 6)
    health = HealthBar(lives[player.lives], round(window.get_width() / 2), (window.get_height() - 45), 0.7)

    add_alien(Alien, a, game_variables.NUM_ALIENS, game_variables.alienList)
    add_alien(BlueAlien, a2, game_variables.NUM_BLUE_ALIENS, game_variables.blue_alienList)
    add_alien(BigAlien, a3, game_variables.NUM_BIG_ALIENS, game_variables.big_alienList)
    add_alien(ShootAlien, a4, game_variables.NUM_SHOOTING_ALIENS, game_variables.shoot_alienList)

    laser = Laser(l, 1, round(window.get_height() / 2))
    add_rocks(4, Rock, rockRandom, game_variables.rockList, min_speed=1, max_speed=3)

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1


def main():
    global game_variables, buttons, player, health, laser, tiles
    init_game()

    while True:
        shake_offset = game_variables.screen_effects.screenshake()
        screen_offset = game_variables.screen_effects.screenshake(window=True)
        window.fill((0, 0, 0))

        # Menus 
        if not game_variables.gameOver and not game_variables.gameStart:
            main_menu(game_variables, buttons[0], buttons[1], buttons[2])
        if game_variables.gameOver:
            reset_menu(game_variables, buttons[0], buttons[1], buttons[2], init_game)
        if game_variables.gamePause:
            pause_menu(game_variables, buttons[3], buttons[1], buttons[2])
        if game_variables.gameStart and not game_variables.gamePause:
            change_cursor()

            if player.lives <= 0:
                game_variables.gameOver = True
                game_variables.gameStart = False

            # Scrolling background
            for i in range(0, tiles):
                window.blit(bg, (i * bg.get_width() + game_variables.scroll + screen_offset[0], screen_offset[1]))

            game_variables.scroll -= 5
            if abs(game_variables.scroll) > bg.get_width():
                game_variables.scroll = 0


            # Level up
            if len(game_variables.alienList) == 0:
                change_level(game_variables)
                add_alien(Alien, a, game_variables.NUM_ALIENS, game_variables.alienList)
                add_alien(BlueAlien, a2, game_variables.NUM_BLUE_ALIENS, game_variables.blue_alienList)
                if game_variables.lvl > 2:
                    add_alien(ShootAlien, a4, game_variables.NUM_SHOOTING_ALIENS, game_variables.shoot_alienList)
                if game_variables.lvl > 4:
                    add_alien(BigAlien, a3, game_variables.NUM_BIG_ALIENS, game_variables.big_alienList)
                laser.update(game_variables)

            # Laser
            laser.show(window, shake_offset)
            laser.moveLR(window, player)
            if laser.rect.x >= window.get_width()+200:
                laser.reset()

            # Rock
            for rock in game_variables.rockList:
                if rock.lives > 0:
                    rock.update(window)
                    rock.show(window, shake_offset)
                    rock.collide(game_variables, laser)
                if len(game_variables.rockList) < 4:
                    add_rocks(random.randint(6, 8), Rock, rockRandom, game_variables.rockList, min_speed=2, max_speed=6)
            game_variables.rockList = [rock for rock in game_variables.rockList if not rock.remove]

            for explosion in game_variables.explosionParticles:
                explosion.update()
                explosion.show()
            game_variables.explosionParticles = RockExplosion.cleanup(game_variables.explosionParticles)

            # Player
            player.move(window, game_variables.moveR, game_variables.moveL, game_variables.moveU, game_variables.moveD)
            player.update(game_variables.telep, game_variables)
            player.collide(game_variables, laser)
            player.show(window, shake_offset)

            for particle in game_variables.teleportParticles:
                particle.update(clock.get_time())
                particle.show()
            game_variables.teleportParticles = TeleportAnimation.cleanup(game_variables.teleportParticles)

            # Shooting
            bullet_check(game_variables.bulletList, window)
            if game_variables.shoot:
                player_shoot(Bullet, player, game_variables.bulletList, game_variables.screen_effects)
                game_variables.screen_effects.shake_duration = 5
            if game_variables.shotg:
                player_shotgun(Shell, player, game_variables.bulletList, game_variables.screen_effects)
                game_variables.screen_effects.shake_duration = 10
            for bullets in game_variables.bulletList:
                    bullets.update()
                    bullets.show(window)
            game_variables.screen_effects.update_recoil(player)

            # Aliens
            for alien in game_variables.alienList:
                alien.show(window, shake_offset)
                alien.update(player, game_variables)
                alien.move()
                reduce_life_edge(player, alien, game_variables.alienList)
            
            for alienBlue in game_variables.blue_alienList:
                alienBlue.show(window, shake_offset)
                alienBlue.update(player, game_variables)
                alienBlue.move()
                reduce_life_edge(player, alienBlue, game_variables.blue_alienList)

            for alienBig in game_variables.big_alienList:
                alienBig.show(window, a3, shake_offset)
                alienBig.update(player, game_variables)
                alienBig.move()
                reduce_life_edge(player, alienBig, game_variables.big_alienList)

            for alien_bullet in game_variables.alien_bulletList:
                alien_bullet.update(player, game_variables)
                alien_bullet.show(window)
            for alienShoot in game_variables.shoot_alienList:
                alienShoot.show(window, shake_offset)
                alienShoot.update(player, game_variables)
                alienShoot.move(player, window, game_variables)
                reduce_life_edge(player, alienShoot, game_variables.shoot_alienList)

            health.show(window, lives, player)
            clock.tick()
            ui(clock, player, game_variables)
        else:
            show_cursor()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Keys
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

            if not (game_variables.moveR or game_variables.moveL or game_variables.moveU or game_variables.moveD):
                player.slowdown()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_variables.shoot = True
                gun_channel.play(gun_sound, loops=-1)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game_variables.shoot = False
                gun_channel.stop()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game_variables.shotg = True 
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