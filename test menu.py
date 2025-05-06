import pygame
import sys

# Initialisation de Pygame
pygame.init()
pygame.font.init()

# Configuration de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boutons Image ou Texte")
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()
# Couleurs de base
WHITE      = (255, 255, 255)
LIGHT_GRAY = (170, 170, 170)  # couleur au survol
DARK_GRAY  = (100, 100, 100)  # couleur normale

# Police pour le texte des boutons
FONT = pygame.font.SysFont(None, 36)

# Cache pour les images de boutons (évite de recharger plusieurs fois le même fichier)
image_cache = {}

def draw_image_button(screen, text, x, y, width, height, image_path=None, action=None):
    """
    Affiche un bouton sur l'écran `screen` en utilisant une image si disponible, sinon en texte.
    - text : le texte à afficher sur le bouton si l'image n'est pas chargée.
    - x, y : coordonnées du coin supérieur gauche du bouton.
    - width, height : dimensions du bouton.
    - image_path : chemin vers le fichier image (ex: 'START.png'), ou None.
    - action : fonction à appeler si le bouton est cliqué.
    """
    # Obtenir la position de la souris et l'état des boutons (True si enfoncé)
    mouse = pygame.mouse.get_pos()               # (x, y) de la souris:contentReference[oaicite:5]{index=5}
    click = pygame.mouse.get_pressed()           # état des boutons:contentReference[oaicite:6]{index=6}

    # Essayons de charger et d'afficher l'image du bouton
    if image_path:
        try:
            # Charger l'image depuis le cache ou depuis le disque
            if image_path in image_cache:
                img = image_cache[image_path]
            else:
                img_loaded = pygame.image.load(image_path)  # charge l'image en Surface:contentReference[oaicite:7]{index=7}
                # Convertir en format optimal : convert_alpha() gère la transparence:contentReference[oaicite:8]{index=8}
                try:
                    img = img_loaded.convert_alpha()
                except Exception:
                    img = img_loaded.convert()
                image_cache[image_path] = img

            # Redimensionner l'image aux dimensions du bouton
            img = pygame.transform.scale(img, (width, height))  # redimensionnement rapide:contentReference[oaicite:9]{index=9}
            rect = img.get_rect()  # obtient un Rect couvrant toute l'image:contentReference[oaicite:10]{index=10}
            rect.topleft = (x, y)

            # Afficher l'image du bouton
            screen.blit(img, rect)

            # Détection du survol de souris
            if rect.collidepoint(mouse):  # si la souris est sur le bouton:contentReference[oaicite:11]{index=11}
                # Dessiner un contour pour indiquer le survol
                pygame.draw.rect(screen, LIGHT_GRAY, rect, 3)
                # Si clic gauche, exécuter l'action associée
                if click[0] == 1 and action:
                    action()
            return  # terminaison après dessin de l'image

        except Exception:
            # En cas d'erreur de chargement (fichier manquant, etc.), on passe au fallback texte
            pass

    # --- Fallback : bouton texte simple (pas d'image disponible) ---

    # Créer un rect de bouton
    rect = pygame.Rect(x, y, width, height)

    # Changer la couleur selon le survol
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, LIGHT_GRAY, rect)  # survol
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, DARK_GRAY, rect)   # état normal

    # Afficher le texte centré sur le bouton
    text_surf = FONT.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Fonctions d'exemple pour les actions des boutons (à adapter dans le projet)
def start_game():
    print("Action : Démarrer le jeu")
def load_game():
    print("Action : Charger une partie")
def open_settings():
    print("Action : Ouvrir les paramètres")
def back_to_menu():
    print("Action : Retour au menu")
def play_again():
    print("Action : Rejouer")
def menu_action():
    print("Action : Retourner au menu")
def quit_game():
    pygame.quit()
    sys.exit()

# --- Écrans utilisant draw_image_button ---

def menu_screen():
    """
    Écran du menu principal avec les boutons Start, Load, Settings, Quit.
    Utilise les images START.png, LOAD.png, SETTINGS.png, QUIT.png si disponibles.
    """
    screen.fill((0, 0, 0))  # fond noir

    # Titre du menu
    title_surf = FONT.render("Menu Principal", True, WHITE)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))

    # Boutons du menu principal
    draw_image_button(screen, "Start",    300, 150, 200, 50, "PIC BOUTONS/START.png",    start_game)
    draw_image_button(screen, "Load",     300, 220, 200, 50, "PIC BOUTONS/LOAD.png",     load_game)
    draw_image_button(screen, "Settings", 300, 290, 200, 50, "PIC BOUTONS/SET.png", open_settings)
    draw_image_button(screen, "Quit",     300, 360, 200, 50, "PIC BOUTONS/BACK.png",     quit_game)

    pygame.display.update()


def settings_screen():
    """
    Écran des paramètres avec un bouton Retour (Back).
    Utilise BACK.png pour le bouton Retour si disponible.
    """
    screen.fill((0, 0, 0))  # fond noir

    # Titre des paramètres
    title_surf = FONT.render("Paramètres", True, WHITE)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))

    # Exemple de paramètre (placeholder)
    param_surf = FONT.render("Option 1: ...", True, WHITE)
    screen.blit(param_surf, (100, 150))

    # Bouton Retour
    draw_image_button(screen, "Back", 300, 500, 200, 50, "BACK.png", back_to_menu)

    pygame.display.update()


def load_game_screen():
    """
    Écran de chargement de partie avec un bouton Retour (Back).
    Utilise BACK.png pour le bouton Retour si disponible.
    """
    screen.fill((0, 0, 0))  # fond noir

    # Titre du chargement
    title_surf = FONT.render("Charger une partie", True, WHITE)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))

    # Exemples de slots de sauvegarde (placeholder)
    slot_surf1 = FONT.render("Slot 1 - Sauvegarde A", True, WHITE)
    slot_surf2 = FONT.render("Slot 2 - Sauvegarde B", True, WHITE)
    screen.blit(slot_surf1, (100, 150))
    screen.blit(slot_surf2, (100, 200))

    # Bouton Retour
    draw_image_button(screen, "Back", 300, 500, 200, 50, "BACK.png", back_to_menu)

    pygame.display.update()


def game_over_screen():
    """
    Écran de fin de partie (Game Over) avec boutons Play Again et Menu.
    Utilise PLAY_AGAIN.png et MENU.png si disponibles.
    """
    screen.fill((0, 0, 0))  # fond noir

    # Message Game Over
    over_surf = FONT.render("Game Over", True, WHITE)
    screen.blit(over_surf, (SCREEN_WIDTH//2 - over_surf.get_width()//2, 50))

    # Boutons
    draw_image_button(screen, "Play Again", 250, 200, 300, 50, "PLAY_AGAIN.png", play_again)
    draw_image_button(screen, "Menu",       250, 280, 300, 50, "MENU.png",       menu_action)

    pygame.display.update()


def win_level_screen():
    """
    Écran de victoire de niveau avec boutons Play Again et Menu.
    Utilise PLAY_AGAIN.png et MENU.png si disponibles.
    """
    screen.fill((0, 0, 0))  # fond noir

    # Message Victoire
    win_surf = FONT.render("Vous avez gagné !", True, WHITE)
    screen.blit(win_surf, (SCREEN_WIDTH//2 - win_surf.get_width()//2, 50))

    # Boutons
    draw_image_button(screen, "Play Again", 250, 200, 300, 50, "PLAY_AGAIN.png", play_again)
    draw_image_button(screen, "Menu",       250, 280, 300, 50, "MENU.png",       menu_action)

    pygame.display.update()
    pygame.display.flip()
clock.tick(60)