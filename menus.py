from assets import window, menu_bg, logo, pause_logo
from animate import Comet
from game import text
import random
import pygame
import sys

cometList = [Comet(random.randint(1500, 5000), -random.randint(10, 10000), random.randint(1, 4)) for _ in range(6)]

def ui(clock, player, game_variables):
    text(f"FPS: {int(clock.get_fps())}", 75, 20, small=True)
    text(f"<SPACE> TO TELEPORT", (window.get_width()/2)-400, 20, small=True) if player.charge == "ACTIVATED" else 0
    text(f"<MB2> FOR SHOTGUN {'(READY)' if player.srate <= 0 else '(CHARGING)'}", (window.get_width()/2)+100, 20, small=True) if player.gun else 0
    text(f"CHARGE: {player.charge}", window.get_width()-300, 20, small=True)
    text(f"ALIENS KILLED: {game_variables.aliensKilled}", window.get_width()-220, window.get_height()-50, small=True)
    text(f"LEVEL: {game_variables.lvl}", 50, window.get_height()-50, small=True)


def main_menu(game_variables, play_button, tuto_button, quit_button):
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


def pause_menu(game_variables, play_button, tuto_button, quit_button):
    window.blit(menu_bg, (0, 0))
    window.blit(pause_logo, ((window.get_width()/2)-290, (window.get_height()/2)-300))

    if play_button.pressed():
        game_variables.gamePause = False
    if tuto_button.pressed():
        pass
    if quit_button.pressed():
        pygame.quit()
        sys.exit()