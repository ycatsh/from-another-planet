import pygame
import sys
from game import text, init_game
from assets import window, start_bg, over_bg, menu_bg


def ui(clock, player, game_variables):
    text(f"FPS: {int(clock.get_fps())}", 75, 20, small=True)
    text(f"<SPACE> TO TELEPORT", (window.get_width()/2)-50, 20, small=True) if player.charge == "ACTIVATED" else 0
    text(f"CHARGE: {player.charge}", window.get_width()-300, 20, small=True)
    text(f"ALIENS KILLED: {game_variables.aliensKilled}", window.get_width()-220, window.get_height()-50, small=True)
    text(f"LEVEL: {game_variables.lvl}", 50, window.get_height()-50, small=True)


def main_menu(game_variables, play_button, quit_button):
    if not game_variables.gameStart:
        window.blit(start_bg, (0, 0))

        if play_button.draw():
            game_variables.gameStart = True
        if quit_button.draw():
            pygame.quit()
            sys.exit()


def end_menu(game_variables, play_button, quit_button):
    if game_variables.gameOver:
        window.blit(over_bg, (0, 0))
        text("YOU DIED", round(window.get_width()/2)-85, (window.get_height()/2)-150)
        text("GAME OVER", round(window.get_width()/2)-110, (window.get_height()/2)-70)

        if play_button.draw():
            game_variables.gameOver = False
            init_game()
        if quit_button.draw():
            pygame.quit()
            sys.exit()


def pause_menu(game_variables, play_button, quit_button):
    if game_variables.gamePause:
        if not game_variables.gameOver:
            window.blit(menu_bg, (0, 0))
            text("PAUSE MENU", round(window.get_width()/2)-130, (window.get_height()/2)-200)

            if play_button.draw():
                game_variables.gamePause = False
            if quit_button.draw():
                pygame.quit()
                sys.exit()