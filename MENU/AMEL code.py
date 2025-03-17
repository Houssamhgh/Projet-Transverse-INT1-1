import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spidey Hook")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Polices
font = pygame.font.SysFont("Comic Sans MS", 80)
small_font = pygame.font.SysFont("Arial", 30)

# Couleur de fond
background_color = (30, 30, 30)

def render_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class Spider:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 3)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > screen_width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > screen_height:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)

spiders = [Spider() for _ in range(5)]

def draw_spider_web():
    center_x, center_y = screen_width // 2, screen_height // 2
    num_lines = 10
    for i in range(1, num_lines + 1):
        pygame.draw.circle(screen, WHITE, (center_x, center_y), i * 40, 2)

    for i in range(0, 360, 30):
        x1 = center_x + 40 * num_lines * math.cos(math.radians(i))
        y1 = center_y + 40 * num_lines * math.sin(math.radians(i))
        pygame.draw.line(screen, WHITE, (center_x, center_y), (x1, y1), 2)

# Gestion de l'état du jeu
game_state = "menu"
music_on = True
sounds_on = True
selected_music = "track1"
input_text = ""

# Gestion des boutons
def draw_button(text, x, y, width, height, color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, BLUE, (x, y, width, height))
        if mouse_click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    text_surface = small_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Gestion de la musique
def load_music(track_name):
    try:
        pygame.mixer.music.load(f"musique/{track_name}.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)  # -1 pour répéter indéfiniment
        print(f"Musique {track_name} chargée et en lecture.")
    except pygame.error as e:
        print(f"Erreur de chargement de la musique: {track_name}. Détails: {e}")

def stop_music():
    pygame.mixer.music.stop()
    print("Musique arrêtée.")

def change_music(track):
    global selected_music
    selected_music = track
    stop_music()  # Arrêter la musique actuelle avant de charger une nouvelle
    load_music(selected_music)

def menu():
    screen.fill(background_color)
    draw_spider_web()

    # Titre du jeu
    title_text = "Spidey Hook"
    title_surface = font.render(title_text, True, RED)
    title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
    screen.blit(title_surface, title_rect)

    # Boutons du menu
    draw_button("Start Game", screen_width // 2 - 100, 200, 200, 50, GRAY, start_game)
    draw_button("Load Game", screen_width // 2 - 100, 300, 200, 50, GRAY, load_game)
    draw_button("Settings", screen_width // 2 - 100, 400, 200, 50, GRAY, settings)

    for spider in spiders:
        spider.move()
        spider.draw()

def start_game():
    global game_state
    game_state = "playing"

def load_game():
    global game_state, input_text
    game_state = "load_game"
    input_text = ""

def settings():
    global game_state
    game_state = "settings"

def music_settings():
    global game_state
    game_state = "music_settings"

def music_selection_menu():
    screen.fill(background_color)
    render_text("Select Music Track", font, RED, screen_width // 2, 100)
    render_text(f"Current Music: {selected_music}", small_font, WHITE, screen_width // 2, 150)

    button_width = 200
    button_height = 50
    button_x = screen_width // 2 - button_width // 2

    draw_button("Track 1", button_x, 250, button_width, button_height, GRAY, lambda: change_music("track1"))
    draw_button("Track 2", button_x, 320, button_width, button_height, GRAY, lambda: change_music("track2"))
    draw_button("Track 3", button_x, 390, button_width, button_height, GRAY, lambda: change_music("track3"))
    draw_button("Back", button_x, 460, button_width, button_height, GRAY, lambda: set_state("settings"))

def load_game_screen():
    global input_text
    screen.fill(background_color)

    render_text("Enter your name:", font, RED, screen_width // 2, 100)
    render_text("Please enter your name and press Enter", small_font, WHITE, screen_width // 2, 160)

    input_box = pygame.Rect(screen_width // 2 - 100, 200, 200, 40)
    pygame.draw.rect(screen, GRAY, input_box)
    render_text(input_text, small_font, WHITE, screen_width // 2, 215)

    render_text("Leaderboard:", small_font, WHITE, screen_width // 2, 300)
    render_text("No scores yet.", small_font, WHITE, screen_width // 2, 350)

    draw_button("Confirm", screen_width // 2, 450, 200, 50, GRAY, lambda: set_state("playing"))
    draw_button("Back", screen_width // 2, 520, 200, 50, GRAY, lambda: set_state("menu"))

def set_state(state):
    global game_state
    game_state = state

def main_loop():
    global game_state, input_text
    clock = pygame.time.Clock()
    running = True

    while running:
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
            settings()
        elif game_state == "music_settings":
            music_selection_menu()
        elif game_state == "load_game":
            load_game_screen()
        elif game_state == "playing":
            screen.fill(background_color)
            render_text("Game in progress...", small_font, WHITE, screen_width // 2 - 150, screen_height // 2)
            draw_button("Back to Menu", 500, 500, 200, 50, GRAY, lambda: set_state("menu"))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()
