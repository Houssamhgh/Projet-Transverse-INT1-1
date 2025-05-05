import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Définition des classes
class Stickman:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.width = 20
        self.height = 50
        self.grappin = False
        self.grappin_x = 0
        self.grappin_y = 0

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        if self.grappin:
            pygame.draw.line(screen, BLACK, (self.x + self.width // 2, self.y), (self.grappin_x, self.grappin_y), 2)

class Barre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 20

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

# Création des objets
stickman = Stickman()
barres = [Barre(300, 100), Barre(500, 300), Barre(700, 200)]

# Boucle principale
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            stickman.grappin = True
            stickman.grappin_x = mouse_x
            stickman.grappin_y = mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            stickman.grappin = False

    # Déplacement du stickman
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        stickman.x -= 5
    if keys[pygame.K_RIGHT]:
        stickman.x += 5

    # Collision avec les barres
    for barre in barres:
        if (stickman.x + stickman.width > barre.x and
            stickman.x < barre.x + barre.width and
            stickman.y + stickman.height > barre.y and
            stickman.y < barre.y + barre.height):
            print("Collision avec la barre !")
            # Vous pouvez ajouter un code pour faire quelque chose lorsque le stickman touche une barre

    # Dessin de la scène
    screen.fill(WHITE)
    stickman.draw()
    for barre in barres:
        barre.draw()

    # Mise à jour de la fenêtre
    pygame.display.flip()

    # Limite de 60 images par seconde
    pygame.time.Clock().tick(60)
