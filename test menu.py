import pygame
import sys

# Initialisation globale de pygame
pygame.init()

# Configuration de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu avec Images Boutons")
clock = pygame.time.Clock()
background_img = pygame.image.load("BACKG.png")  # Changez le nom selon votre fichier
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Couleurs (si nécessaires pour des éléments supplémentaires)

screen.blit(background_img, (0, 0))
logo_img = pygame.image.load("LOGO.png")
# Redimensionner si nécessaire
logo_img = pygame.transform.scale(logo_img, (500, 200))
screen.blit(logo_img, (WIDTH // 2 - logo_img.get_width() // 2, 50))

# Charger les images des boutons
try:
    start_game_img = pygame.image.load("MENU.png")
    load_game_img = pygame.image.load("RESTART.png")
    settings_img = pygame.image.load("SET.png")
    quit_img = pygame.image.load("BACK.png")

    # Redimensionnement des images pour uniformité (si requis)
    start_game_img = pygame.transform.scale(start_game_img, (200, 100))
    load_game_img = pygame.transform.scale(load_game_img, (200, 100))
    settings_img = pygame.transform.scale(settings_img, (200, 100))
    quit_img = pygame.transform.scale(quit_img, (200, 100))
except pygame.error as e:
    print(f"Erreur lors du chargement des images : {e}")
    pygame.quit()
    sys.exit()


# Fonction générique pour afficher des images et détecter les clics des boutons
def image_button(image, x, y, action=None):
    """
    Affiche un bouton sous forme d'image et détecte les clics dessus.

    Args:
        image : Surface de l'image à afficher pour le bouton.
        x, y : Position (coordonnées) de l'image à l'écran.
        action : Fonction à appeler lorsqu'un clic est détecté.
    """
    button_rect = image.get_rect(topleft=(x, y))
    screen.blit(image, (x, y))  # Afficher l'image

    # Gérer les événements de clic
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if button_rect.collidepoint(mouse_pos):  # Si la souris survole le bouton
        if mouse_click[0] and action:  # Si clique gauche (0 = clique gauche)
            action()


# Actions du menu
def start_game():
    print("Démarrage du jeu...")
    # Vous pouvez lancer ici votre logique de jeu.
    pass


def load_game():
    print("Chargement du jeu...")
    # Ajoutez ici de la logique pour charger une partie.
    pass


def open_settings():
    print("Ouverture des paramètres...")
    # Ajoutez ici la logique pour ouvrir le menu des paramètres.
    pass


def quit_game():
    print("Quitter le jeu...")
    pygame.quit()
    sys.exit()


# Fonction principale du menu
def menu_screen():
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Afficher le fond et le contenu
          # Fond noir

        # Afficher les boutons avec leurs actions respectives
        image_button(start_game_img, WIDTH // 2 - 100, 200, start_game)
        image_button(load_game_img, WIDTH // 2 - 100, 300, load_game)
        image_button(settings_img, WIDTH // 2 - 100, 400, open_settings)
        image_button(quit_img, WIDTH // 2 - 100, 500, quit_game)

        # Mettre à jour l'écran
        pygame.display.flip()

        # Contrôle des FPS
        clock.tick(60)

    pygame.quit()


# Lancer le menu
if __name__ == "__main__":
    menu_screen()
