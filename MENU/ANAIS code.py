import pygame
import sys
import math
import random

# Initialiser Pygame
pygame.init()

# Définir la taille de l'écran et les couleurs
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spidey Hook")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Définir la police
font = pygame.font.SysFont("Comic Sans MS", 80)
small_font = pygame.font.SysFont("Arial", 30)

# Utilisation d'une couleur pour remplacer l'image de fond
background_color = (30, 30, 30)  # Fond sombre

# Classe Araignée pour les araignées animées
class Spider:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 3)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Si l'araignée sort de l'écran, on la ramène à l'opposé
        if self.x < 0 or self.x > screen_width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > screen_height:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)  # Représenter l'araignée par un cercle blanc

# Créer une liste d'araignées
spiders = [Spider() for _ in range(5)]

# Fonction pour dessiner une toile d'araignée
def draw_spider_web():
    # Dessiner des cercles concentriques
    center_x, center_y = screen_width // 2, screen_height // 2
    num_lines = 10
    for i in range(1, num_lines + 1):
        pygame.draw.circle(screen, WHITE, (center_x, center_y), i * 40, 2)

    # Dessiner les lignes qui relient les cercles
    for i in range(0, 360, 30):
        x1 = center_x + 40 * num_lines * math.cos(math.radians(i))
        y1 = center_y + 40 * num_lines * math.sin(math.radians(i))
        pygame.draw.line(screen, WHITE, (center_x, center_y), (x1, y1), 2)

# États
game_state = "menu"
music_on = True
sounds_on = True
player_name = ""
best_scores = {}  # Classement vide
selected_music = "Track 1"
input_text = ""

# Fonctions utiles
def draw_text(text, y, color=BLACK, font=small_font):
    surface = font.render(text, True, color)  # Utilisation de "font" ici
    text_rect = surface.get_rect(center=(screen_width // 2, y))
    screen.blit(surface, text_rect)

def draw_button(text, y, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(screen_width // 2 - 100, y, 200, 50)  # Change WIDTH to screen_width
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, y + 25, BLACK)

    if rect.collidepoint(mouse) and click[0] == 1:
        pygame.time.delay(200)
        if action:
            action()


def start_game():
    global game_state
    game_state = "playing"

def load_game():
    global game_state, input_text
    game_state = "load_game"
    input_text = ""  # Réinitialiser l'entrée du texte lorsqu'on charge la partie

def settings():
    global game_state
    game_state = "settings"

def music_settings():
    global game_state
    game_state = "music_settings"

def toggle_music():
    global music_on
    music_on = not music_on
    print("Musique:", "Activée" if music_on else "Désactivée")

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on
    print("Sons:", "Activés" if sounds_on else "Désactivés")

def change_music(track):
    global selected_music
    selected_music = track
    print(f"Musique changée: {selected_music}")

def menu():
    screen.fill(WHITE)
    draw_text("Spidey Hook", 100, BLUE)
    draw_button("Start", 200, start_game)
    draw_button("Load", 300, load_game)
    draw_button("Settings", 400, settings)

def settings_menu():
    screen.fill(WHITE)
    draw_text("Settings", 100, BLUE)
    draw_button(f"Music: {'On' if music_on else 'Off'}", 200, toggle_music)
    draw_button(f"Sounds: {'On' if sounds_on else 'Off'}", 300, toggle_sounds)
    draw_button("Change Music", 400, music_settings)
    draw_button("Back", 500, lambda: set_state("menu"))

def music_selection_menu():
    screen.fill(WHITE)
    draw_text("Select Music Track", 100, BLUE)
    draw_text(f"Current Music: {selected_music}", 150, BLACK)
    draw_button("Track 1", 250, lambda: change_music("Track 1"))
    draw_button("Track 2", 310, lambda: change_music("Track 2"))
    draw_button("Track 3", 370, lambda: change_music("Track 3"))
    draw_button("Back", 450, lambda: set_state("settings"))

def load_game_screen():
    global input_text
    screen.fill(WHITE)
    draw_text("Enter your name:", 100, BLUE)

    input_box = pygame.Rect(WIDTH // 2 - 100, 200, 200, 40)
    pygame.draw.rect(screen, GRAY, input_box)
    draw_text(input_text, 215, BLACK)

    draw_text("Leaderboard:", 300, BLUE)
    y_offset = 350
    draw_text("No scores yet.", y_offset, BLACK)

    draw_button("Confirm", 500, lambda: set_state("playing"))
    draw_button("Back", 560, lambda: set_state("menu"))

def set_state(state):
    global game_state
    game_state = state

def main_loop():
    global game_state, input_text
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game_state == "load_game" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    set_state("playing")
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        if game_state == "menu":
            menu()
        elif game_state == "settings":
            settings_menu()
        elif game_state == "music_settings":
            music_selection_menu()
        elif game_state == "load_game":
            load_game_screen()
        elif game_state == "playing":
            screen.fill(WHITE)
            draw_text("Game in progress...", 250, BLACK)
            draw_button("Back to Menu", 400, lambda: set_state("menu"))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == ("__main__"):
    main_loop()