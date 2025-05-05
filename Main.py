# main.py (corrigé)
import pygame
import sys
import json
from module import Ball, Spider, generate_rope_chain, generate_platforms, generate_slopes, SPACE_BETWEEN_ROPES
from function import draw_button, draw_spider_web, render_text, draw_text

pygame.init()

# Dimensions & setup
WIDTH, HEIGHT = 800, 600
CAMERA_OFFSET = WIDTH // 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()

# Couleurs & polices
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont("Comic Sans MS", 80)
small_font = pygame.font.SysFont("Arial", 30)

# Etat
game_state = "menu"
music_on = True
sounds_on = True
player_name = ""
selected_music = "Track 1"
input_text = ""

# Objets dynamiques
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
platforms = generate_platforms()
slopes = generate_slopes()
spiders = [Spider(WIDTH, HEIGHT) for _ in range(5)]
camera_x = 0
finish_line = pygame.Rect(4200, 0, 20, HEIGHT)

def toggle_music():
    global music_on
    music_on = not music_on

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on

def change_music(track="Track 2"):
    global selected_music
    selected_music = track

def set_state(state):
    global game_state
    game_state = state

def start_game():
    global ball, ropes, platforms, slopes, camera_x, finish_line, game_state
    game_state = "playing"
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    ropes = generate_rope_chain()
    platforms = generate_platforms()
    slopes = generate_slopes()
    camera_x = 0
    finish_line = pygame.Rect(4200, 0, 20, HEIGHT)

def init_game_from_data(data):
    global player_name
    player_name = data.get("player_name", "Unknown")

def check_save_exists(level):
    return False

def load_saved_game(difficulty):
    try:
        with open(f"save_{difficulty}.json", "r") as file:
            data = json.load(file)
            init_game_from_data(data)
            set_state("playing")
    except FileNotFoundError:
        print(f"Pas de sauvegarde pour {difficulty}")
        set_state("menu")
    except json.JSONDecodeError:
        print("Erreur JSON")

def menu_screen():
    screen.fill(BLACK)
    draw_spider_web(screen, WIDTH, HEIGHT)
    render_text("Spidey Hook", font, RED, WIDTH // 2, 100, screen)
    draw_button("Start Game", WIDTH // 2 - 100, 200, 200, 50, GRAY, screen, small_font, start_game)
    draw_button("Load Game", WIDTH // 2 - 100, 300, 200, 50, GRAY, screen, small_font, lambda: set_state("load_game"))
    draw_button("Settings", 20, HEIGHT - 70, 200, 50, GRAY, screen, small_font, lambda: set_state("settings"))
    for spider in spiders:
        spider.move()
        spider.bounce(WIDTH, HEIGHT)
        spider.draw(screen)

def settings_screen():
    screen.fill(BLACK)
    render_text("Settings", font, RED, WIDTH // 2, 100, screen)
    button_x = WIDTH // 2 - 100
    draw_button(f"Music: {'On' if music_on else 'Off'}", button_x, 200, 200, 50, GRAY, screen, small_font, toggle_music)
    draw_button(f"Sounds: {'On' if sounds_on else 'Off'}", button_x, 300, 200, 50, GRAY, screen, small_font, toggle_sounds)
    draw_button("Change Music", button_x, 400, 200, 50, GRAY, screen, small_font, change_music)
    draw_button("Back", button_x, 500, 200, 50, GRAY, screen, small_font, lambda: set_state("menu"))

def load_game_screen():
    screen.fill(BLACK)
    render_text("Choose Your Level", font, RED, WIDTH // 2, 100, screen)
    levels = ["Easy", "Normal", "Hard"]
    positions = [(WIDTH // 3 - 100, 300), (WIDTH // 2 - 75, 300), (2 * WIDTH // 3 - 50, 300)]
    for i, level in enumerate(levels):
        draw_button(level, positions[i][0], positions[i][1], 150, 150, GRAY, screen, small_font,
                    lambda l=level: load_saved_game(l))

def game_screen():
    global camera_x, game_state
    keys = pygame.key.get_pressed()
    ball.update(keys, platforms, slopes, ropes, HEIGHT)
    camera_x = ball.pos.x - CAMERA_OFFSET
    if not ball.is_alive:
        game_state = "game_over"
    if pygame.Rect(ball.pos.x - ball.radius, ball.pos.y - ball.radius, ball.radius * 2, ball.radius * 2).colliderect(finish_line):
        game_state = "win_level"
    for rope in ropes:
        rope.update(ball)
    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(ropes[-1].__class__(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))
    screen.fill(BLACK)
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)
    for platform in platforms:
        platform.draw(screen, camera_x)
    for slope in slopes:
        slope.draw(screen, camera_x)
    pygame.draw.rect(screen, GREEN, pygame.Rect(finish_line.x - camera_x, 0, 20, HEIGHT))
    draw_button("Menu", WIDTH - 120, 20, 100, 40, GRAY, screen, small_font, lambda: set_state("menu"))

def game_over_screen():
    screen.fill(BLACK)
    render_text("Game Over", font, RED, WIDTH // 2, HEIGHT // 3, screen)
    draw_button("Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, screen, small_font, start_game)
    draw_button("Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, screen, small_font, lambda: set_state("menu"))

def win_level_screen():
    screen.fill(BLACK)
    render_text("Congratulations", font, BLUE, WIDTH // 2, HEIGHT // 3, screen)
    draw_button("Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, screen, small_font, start_game)
    draw_button("Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, screen, small_font, lambda: set_state("menu"))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "load_game" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_game()
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    if game_state == "menu":
        menu_screen()
    elif game_state == "settings":
        settings_screen()
    elif game_state == "load_game":
        load_game_screen()
    elif game_state == "playing":
        game_screen()
    elif game_state == "game_over":
        game_over_screen()
    elif game_state == "win_level":
        win_level_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
