import pygame
import random
import math
import sys

# Initialisation globale de pygame
pygame.init()

# Configuration de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Polices
font = pygame.font.SysFont("Comic Sans MS", 80)
small_font = pygame.font.SysFont("Arial", 30)

# Variables du jeu
game_state = "menu"  # menu, playing, game_over
MASS = 0.05
GRAVITATIONAL_CONST = 9.81
GRAVITY = MASS * GRAVITATIONAL_CONST
SPACE_BETWEEN_ROPES = 300
CAMERA_OFFSET = WIDTH // 3
ON_GROUND = False

# Variables du menu
music_on = True
sounds_on = True
player_name = ""
best_scores = {}
selected_music = "Track 1"
input_text = ""

# Classe du joueur (Ball)
class Ball:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.radius = 10
        self.velocity = pygame.Vector2(0, 0)
        self.is_attached = False
        self.attached_rope = None
        self.is_alive = True

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, WHITE, (int(self.pos.x - camera_x), int(self.pos.y)), self.radius)

    def update(self, keys, platforms):
        if self.is_alive:
            if keys[pygame.K_SPACE] and not self.is_attached:
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)  # Attach to closest rope

            self.velocity.y += GRAVITY
            self.pos += self.velocity

            # Vérifier collision avec plateforme
            for platform in platforms:
                if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius,
                                                         self.radius * 2, self.radius * 2)):
                    self.pos.y = platform.rect.top - self.radius
                    self.velocity.y = 0
                    break

            if self.pos.y > HEIGHT - self.radius:  # Si la balle tombe au-delà du bas de l'écran
                self.is_alive = False  # La balle meurt

# Classe des plateformes
class Platform:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, self.color, self.rect.move(-camera_x, 0))

# Générer des plateformes horizontales uniquement
def generate_platforms():
    return [
        Platform(100, 500, 200, 10, GREEN),
        Platform(400, 450, 200, 10, RED),
        Platform(700, 400, 200, 10, GREEN),
        Platform(1000, 350, 200, 10, RED),
        Platform(1300, 300, 200, 10, GREEN),
    ]

# Boucle d'affichage du menu
def menu_screen():
    screen.fill(BLACK)
    render_text("Spidey Hook", font, RED, WIDTH // 2, HEIGHT // 3)
    draw_button("Start Game", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GRAY, start_game)

# Démarrer le jeu
def start_game():
    global game_state, ball, platforms
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    platforms = generate_platforms()
    game_state = "playing"

# Écran de jeu
def game_screen():
    global game_state
    keys = pygame.key.get_pressed()
    ball.update(keys, platforms)

    screen.fill(BLACK)
    for platform in platforms:
        platform.draw(screen, 0)  # Pas de décalage horizontal pour la première version
    ball.draw(screen, 0)  # Pas de décalage

    if not ball.is_alive:
        game_state = "game_over"

# Écran de fin de jeu
def game_over_screen():
    screen.fill(BLACK)
    render_text("Game Over", font, RED, WIDTH // 2, HEIGHT // 3)
    draw_button("Play Again", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GRAY, start_game)

# Fonction pour dessiner le texte
def render_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Fonction pour dessiner un bouton
def draw_button(text, x, y, width, height, color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, button_rect, 3)  # Bordure bleue si survol
        if mouse_click[0] == 1 and action is not None:
            action()

# Boucle principale
running = True
ball = Ball(WIDTH // 2, HEIGHT // 2)
platforms = generate_platforms()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":
        menu_screen()
    elif game_state == "playing":
        game_screen()
    elif game_state == "game_over":
        game_over_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

