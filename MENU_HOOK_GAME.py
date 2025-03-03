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

    # Vérifie si la souris est au-dessus du bouton
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, BLUE, (x, y, width, height))
        if mouse_click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    render_text(text, small_font, WHITE, x + width // 2, y + height // 2)

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
    print("Navigating to settings menu.")
def music_settings():
    global game_state
    game_state = "music_settings"
def toggle_music():
    global music_on
    music_on = not music_on
    print("Musique:", "Activée" if music_on else "Désactivée")
    if music_on:
        pass
    else:
        pass
def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on
    print("Sons:", "Activés" if sounds_on else "Désactivés")
    if sounds_on:
        pass
    else:
        pass
def change_music(track):
    global selected_music
    selected_music = track
    print(f"Musique changée: {selected_music}")

def menu():
    screen.fill(background_color)
    draw_spider_web()
    title_text = "Spidey Hook"
    title_surface = font.render(title_text, True, RED)
    title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
    screen.blit(title_surface, title_rect)
    draw_button("Start Game", screen_width // 2 - 100, 200, 200, 50, GRAY, start_game)
    draw_button("Load Game", screen_width // 2 - 100, 300, 200, 50, GRAY, load_game)
    draw_button("Settings", screen_width // 2 - 100, 400, 200, 50, GRAY, settings)
    for spider in spiders:
        spider.move()
        spider.draw()
def settings_menu():
    screen.fill(background_color)
    settings_text = "Settings"
    render_text(settings_text, font, RED, screen_width // 2, 100)
    button_width = 200
    button_height = 50
    button_x = screen_width // 2 - button_width // 2
    button_y = 200
    draw_button(f"Music: {'On' if music_on else 'Off'}", button_x, button_y, button_width, button_height, GRAY, toggle_music)
    button_y += button_height + 10
    draw_button(f"Sounds: {'On' if sounds_on else 'Off'}", button_x, button_y, button_width, button_height, GRAY, toggle_sounds)
    button_y += button_height + 10
    draw_button("Change Music", button_x, button_y, button_width, button_height, GRAY, music_settings)
    button_y += button_height + 10
    draw_button("Back", button_x, button_y, button_width, button_height, GRAY, lambda: set_state("menu"))

def music_selection_menu():
    screen.fill(background_color)
    render_text("Select Music Track", font, RED, screen_width // 2 - 150, 100)
    render_text(f"Current Music: {selected_music}", small_font, WHITE, screen_width // 2 - 120, 150)
    draw_button("Track 1", 200, 250, 200, 50, GRAY, lambda: change_music("Track 1"))
    draw_button("Track 2", 200, 320, 200, 50, GRAY, lambda: change_music("Track 2"))
    draw_button("Track 3", 200, 390, 200, 50, GRAY, lambda: change_music("Track 3"))
    draw_button("Back", 200, 460, 200, 50, GRAY, lambda: set_state("settings"))
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
