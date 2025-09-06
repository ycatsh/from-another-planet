import sys
import random

import pygame

from from_another_planet import(
    window, menu_bg, logo, pause_logo, over_logo
)
from from_another_planet.helper.animate import CometAnimation
from run import text


cometList = [CometAnimation(random.randint(1500, 5000), -random.randint(10, 10000), random.randint(1, 4)) for _ in range(6)]

def ui(clock, player, game_variables):
    text(f"FPS: {int(clock.get_fps())}", 75, 20, small=True)
    text(f"<SPACE> TO TELEPORT", (window.get_width()/2)-400, 20, small=True) if player.charge == "ACTIVATED" else 0
    text(f"<MB2> FOR SHOTGUN {'(READY)' if player.srate <= 0 else '(CHARGING)'}", (window.get_width()/2)+100, 20, small=True) if player.gun else 0
    text(f"CHARGE: {player.charge}", window.get_width()-300, 20, small=True)
    text(f"ALIENS KILLED: {game_variables.aliensKilled}", window.get_width()-220, window.get_height()-50, small=True)
    text(f"LEVEL: {game_variables.lvl}", 50, window.get_height()-50, small=True)


def main_menu(game_variables, play_button, tuto_button, quit_button):
    pygame.mixer.stop()
    window.blit(menu_bg, (0, 0))
    for comet in cometList:
        comet.update()
        comet.show()
        comet.move()
    window.blit(logo, ((window.get_width()/2)-290, (window.get_height()/2)-400))

    if play_button.pressed():
        game_variables.gameStart = True
    if tuto_button.pressed():
        pass
    if quit_button.pressed():
        pygame.quit()
        sys.exit()


def reset_menu(game_variables, play_button, tuto_button, quit_button, init_game):
    pygame.mixer.stop()
    window.blit(menu_bg, (0, 0))
    window.blit(over_logo, ((window.get_width()/2)-300, (window.get_height()/2)-400))
    text(f"Score: {game_variables.aliensKilled}", (window.get_width()/2)-45, (window.get_height()/2)-70, small=True)
    text(f"Cause of Death: {game_variables.cause_of_death}", 
         (window.get_width()/2)-(10*len(game_variables.cause_of_death)), (window.get_height()/2)-30, small=True)

    if play_button.pressed():
        init_game()
    if tuto_button.pressed():
        pass
    if quit_button.pressed():
        pygame.quit()
        sys.exit()


def pause_menu(game_variables, play_button, tuto_button, quit_button):
    pygame.mixer.stop()
    window.blit(menu_bg, (0, 0))
    window.blit(pause_logo, ((window.get_width()/2)-290, (window.get_height()/2)-300))

    if play_button.pressed():
        game_variables.gamePause = False
    if tuto_button.pressed():
        pass
    if quit_button.pressed():
        pygame.quit()
        sys.exit()
