import pygame
import sys
import random
import math
from settings import *
from utils import Spider, Ball, generate_rope_chain, generate_platforms, generate_slopes, Rope
from ui import render_text, draw_button

# Initialisation pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()

# État global
game_state = "menu"
music_on = True
sounds_on = True
selected_music = "Track 1"
input_text = ""
click_released = True

# Variables de niveau
current_level_index = 0
camera_x = 0
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain(current_level_index)
platforms = generate_platforms(current_level_index)
slopes = generate_slopes(current_level_index)
finish_line = pygame.Rect(4200, 0, 20, HEIGHT)

# Araignées du menu
spiders = [Spider() for _ in range(5)]

# Fonctions d’état
def set_state(state):
    global game_state
    game_state = state

def toggle_music():
    global music_on
    music_on = not music_on

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on

def change_music():
    global selected_music
    selected_music = random.choice(["Track 1", "Track 2", "Track 3"])
    print(f"Musique changée: {selected_music}")

def start_game(difficulty='easy'):
    index_map = {'easy': 0, 'medium': 1, 'hard': 2}
    index = index_map.get(difficulty, 0)
    start_game_by_index(index)

def start_game_by_index(index):
    global ball, ropes, platforms, slopes, camera_x, finish_line, game_state, current_level_index
    current_level_index = index
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    ropes = generate_rope_chain(index)
    platforms = generate_platforms(index)
    slopes = generate_slopes(index)
    finish_line = pygame.Rect(4200, 0, 20, HEIGHT)
    camera_x = 0
    game_state = "playing"

# Écrans
def menu_screen():
    screen.fill(BLACK)
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    for i in range(1, 11):
        pygame.draw.circle(screen, WHITE, (center_x, center_y), i * 40, 2)
    for angle in range(0, 360, 30):
        x = center_x + 400 * math.cos(math.radians(angle))
        y = center_y + 400 * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (center_x, center_y), (x, y), 2)

    render_text("Spidey Hook", font, RED, WIDTH // 2, 100, screen)
    draw_button(screen, "Start Game", WIDTH // 2 - 100, 200, 200, 50, GRAY, small_font, lambda: start_game("easy"))
    draw_button(screen, "Load Game", WIDTH // 2 - 100, 300, 200, 50, GRAY, small_font, lambda: set_state("load_game"))
    draw_button(screen, "Settings", 20, HEIGHT - 70, 200, 50, GRAY, small_font, lambda: set_state("settings"))

    for spider in spiders:
        spider.move()
        spider.draw(screen)

def settings_screen():
    screen.fill(BLACK)
    render_text("Settings", font, RED, WIDTH // 2, 100, screen)
    x = WIDTH // 2 - 100
    draw_button(screen, f"Music: {'On' if music_on else 'Off'}", x, 200, 200, 50, GRAY, small_font, toggle_music)
    draw_button(screen, f"Sounds: {'On' if sounds_on else 'Off'}", x, 300, 200, 50, GRAY, small_font, toggle_sounds)
    draw_button(screen, "Change Music", x, 400, 200, 50, GRAY, small_font, change_music)
    draw_button(screen, "Back", x, 500, 200, 50, GRAY, small_font, lambda: set_state("menu"))

def load_game_screen():
    screen.fill(BLACK)
    render_text("Choose your level:", font, RED, WIDTH // 2, 100, screen)
    draw_button(screen, "Easy", WIDTH // 3 - 75, HEIGHT // 2 - 75, 150, 150, GRAY, small_font, lambda: start_game("easy"))
    draw_button(screen, "Normal", WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150, GRAY, small_font, lambda: start_game("medium"))
    draw_button(screen, "Hard", 2 * WIDTH // 3 - 75, HEIGHT // 2 - 75, 150, 150, GRAY, small_font, lambda: start_game("hard"))
    draw_button(screen, "Back", WIDTH - 220, HEIGHT - 70, 200, 50, GRAY, small_font, lambda: set_state("menu"))

def game_screen():
    global camera_x, game_state, current_level_index

    keys = pygame.key.get_pressed()
    ball.update(keys, platforms, slopes, ropes)
    camera_x = ball.pos.x - CAMERA_OFFSET

    if not ball.is_alive or ball.pos.y >= HEIGHT - ball.radius:
        game_state = "game_over"

    if pygame.Rect(ball.pos.x - ball.radius, ball.pos.y - ball.radius, ball.radius * 2, ball.radius * 2).colliderect(finish_line):
        current_level_index += 1
        if current_level_index < 4:
            start_game_by_index(current_level_index)
        else:
            game_state = "win_level"

    for rope in ropes:
        rope.update(ball)
    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))

    screen.fill(BLACK)
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)
    for platform in platforms:
        platform.draw(screen, camera_x)
    for slope in slopes:
        slope.draw(screen, camera_x)

    pygame.draw.rect(screen, GREEN, pygame.Rect(finish_line.x - camera_x, finish_line.y, finish_line.width, finish_line.height))
    draw_button(screen, "Menu", WIDTH - 120, 20, 100, 40, GRAY, small_font, lambda: set_state("menu"))

def game_over_screen():
    screen.fill(BLACK)
    render_text("Game Over", font, RED, WIDTH // 2, HEIGHT // 3, screen)
    draw_button(screen, "Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, small_font, lambda: start_game("easy"))
    draw_button(screen, "Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, small_font, lambda: set_state("menu"))

def win_level_screen():
    screen.fill(BLACK)
    render_text("Congratulations", font, BLUE, WIDTH // 2, HEIGHT // 3, screen)
    draw_button(screen, "Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, small_font, lambda: start_game("easy"))
    draw_button(screen, "Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, small_font, lambda: set_state("menu"))

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
