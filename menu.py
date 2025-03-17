import pygame
import sys
import math
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spidey Hook")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont("Comic Sans MS", 80)
small_font = pygame.font.SysFont("Arial", 30)

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

game_state = "menu"
music_on = True
sounds_on = True
player_name = ""
best_scores = {}
selected_music = "Track 1"
input_text = ""

def draw_button(text, x, y, width, height, color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Vérifier si la souris est sur le bouton
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, BLUE, (x, y, width, height))
        if mouse_click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    # Calculer la position pour centrer le texte dans le bouton
    text_surface = small_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  # Centrer le texte dans le bouton
    screen.blit(text_surface, text_rect)


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

def toggle_music():
    global music_on
    music_on = not music_on
    print("Musique:", "Activée" if music_on else "Désactivée")

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on
    print("Sons:", "Activés" if sounds_on else "Désactivés")


def draw_button(text, x, y, width, height, color, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse):
        if click[0] == 1:  # Si le bouton gauche est enfoncé
            pygame.time.wait(200)  # Attendre pour éviter les clics multiples
            action()  # Exécute l'action

    pygame.draw.rect(screen, color, button_rect)
    render_text(text, small_font, (255, 255, 255), x + width // 2, y + height // 2)

def change_music(track):
    global selected_music
    selected_music = track
    print(f"Musique changée: {selected_music}")

def menu():
    screen.fill(background_color)
    draw_spider_web()

    # Centrer le titre "Spidey Hook"
    title_text = "Spidey Hook"
    title_surface = font.render(title_text, True, RED)
    title_rect = title_surface.get_rect(center=(screen_width // 2, 100))  # Centrer le texte horizontalement
    screen.blit(title_surface, title_rect)

    # Centrer les boutons du menu
    draw_button("Start Game", screen_width // 2 - 100, 200, 200, 50, GRAY, start_game)
    draw_button("Load Game", screen_width // 2 - 100, 300, 200, 50, GRAY, load_game)
    draw_button("Settings", 20, screen_height-70, 200, 50, GRAY, settings)

    # Faire bouger les araignées
    for spider in spiders:
        spider.move()
        spider.draw()

def settings_menu():
    screen.fill(background_color)
    render_text("Settings", font, RED, screen_width // 2, 100)  # Centré avec render_text

    # Aligner les boutons et les textes avec le titre
    button_width = 200
    button_height = 50
    button_x = screen_width // 2 - button_width // 2  # Centrer les boutons par rapport à l'écran

    draw_button(f"Music: {'On' if music_on else 'Off'}", button_x, 200, button_width, button_height, GRAY, toggle_music)
    draw_button(f"Sounds: {'On' if sounds_on else 'Off'}", button_x, 300, button_width, button_height, GRAY, toggle_sounds)
    draw_button("Change Music", button_x, 400, button_width, button_height, GRAY, music_settings)
    draw_button("Back", button_x, 500, button_width, button_height, GRAY, lambda: set_state("menu"))

def music_selection_menu():
    screen.fill(background_color)

    # Centrer le titre "Select Music Track"
    render_text("Select Music Track", font, RED, screen_width // 2, 100)  # Centré avec render_text

    # Centrer le texte "Current Music"
    render_text(f"Current Music: {selected_music}", small_font, WHITE, screen_width // 2, 150)

    # Définir la largeur des boutons et la hauteur pour les centrer
    button_width = 200
    button_height = 50
    button_x = screen_width // 2 - button_width // 2  # Centrer horizontalement les boutons

    # Centrer les boutons
    draw_button("Track 1", button_x, 250, button_width, button_height, GRAY, lambda: change_music("Track 1"))
    draw_button("Track 2", button_x, 320, button_width, button_height, GRAY, lambda: change_music("Track 2"))
    draw_button("Track 3", button_x, 390, button_width, button_height, GRAY, lambda: change_music("Track 3"))
    draw_button("Back", button_x, 460, button_width, button_height, GRAY, lambda: set_state("settings"))


def load_game_screen():
    global input_text
    screen.fill(background_color)

    # Centrer le titre "Enter your name"
    render_text("Enter your name:", font, RED, screen_width // 2, 100)

    # Message d'indication centré
    render_text("Please enter your name and press Enter", small_font, WHITE, screen_width // 2, 160)

    # Créer une boîte de saisie pour le nom et la centrer
    input_box = pygame.Rect(screen_width // 2 - 100, 200, 200, 40)
    pygame.draw.rect(screen, GRAY, input_box)
    render_text(input_text, small_font, WHITE, screen_width // 2, 215)  # Centrer le texte

    # Classement centré
    render_text("Leaderboard:", small_font, WHITE, screen_width // 2, 300)
    render_text("No scores yet.", small_font, WHITE, screen_width // 2, 350)

    # Boutons centrés
    draw_button("Confirm", screen_width-220, 450, 200, 50, GRAY, lambda: set_state("playing"))
    draw_button("Back", screen_width-220, screen_height-70, 200, 50, GRAY, lambda: set_state("menu"))

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
            settings_menu()
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


