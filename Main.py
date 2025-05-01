import pygame
import random
import math
import sys
from Levels import ropes, platforms, slopes

# Initialisation globale de pygame
pygame.init()



# Initialisation des objets du jeu
ball = Ball(WIDTH // 2, HEIGHT // 2)
spiders = [Spider() for _ in range(5)]
camera_x = 0

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "load_game" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_game()
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    if game_state == "menu":
        menu_screen()
    elif game_state == "settings":
        settings_screen()
    elif game_state == "load_game":
        load_game_screen()
    elif game_state == "playing":
        game_screen()
    elif game_state == "win_level":
        win_level_screen()
    elif game_state == "game_over":
        game_over_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

