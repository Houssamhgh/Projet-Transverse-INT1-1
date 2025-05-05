import pygame
#constantes et paramètres
# Dimensions de l'écran
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Constantes physiques
MASS = 0.05
GRAVITATIONAL_CONST = 9.81
GRAVITY = MASS * GRAVITATIONAL_CONST
SPACE_BETWEEN_ROPES = 300
CAMERA_OFFSET = WIDTH // 3
ON_GROUND = False
GAME_STATES = ["menu", "aiming", "playing", "load_game", "settings", "game_over", "win_level"]

# Fonts
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 80)
small_font = pygame.font.SysFont("Arial", 30)
