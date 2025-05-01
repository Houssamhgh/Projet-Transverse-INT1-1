import pygame
WIDTH, HEIGHT = 800, 600



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
