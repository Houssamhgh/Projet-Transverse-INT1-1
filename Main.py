import sys
from Screens import *

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

