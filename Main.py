# main.py
import sys
import random
import math
from settings import *
from utils import Spider, Ball, generate_rope_chain, generate_platforms, generate_slopes, Rope, SoundManager
from ui import render_text, draw_button, draw_trajectory, draw_direction_arrow

# Initialisation pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()
sound_manager = SoundManager()

# Etat global
game_state = "menu"
music_on = True
sounds_on = True
selected_music = "Track 1"
input_text = ""
click_released = True
is_aiming = True
gravity = 0.5

# Trajectoire initiale
initial_velocity = pygame.Vector2(8, -5)

# Niveau
current_level_index = 0
camera_x = 0
ball = Ball(100, HEIGHT - 100)
ropes = generate_rope_chain(current_level_index)
platforms = generate_platforms(current_level_index)
slopes = generate_slopes(current_level_index)
finish_line = pygame.Rect(4200, 0, 20, HEIGHT)

# Araignées dans le menu
spiders = [Spider() for _ in range(5)]


def set_state(state):
    global game_state
    game_state = state
    if sounds_on:
        if state == "menu":
            sound_manager.play_sound("starting_sound")
        elif state == "game_over":
            sound_manager.play_sound("gameover_sound")
        elif state == "win_level":
            sound_manager.play_sound("win_sound")
    if music_on:
        if state == "menu":
            sound_manager.play_music(selected_music.lower().replace(" ", ""), loop=True)
        elif state in ("game_over", "win_level"):
            sound_manager.stop_music()

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
    global ball, ropes, platforms, slopes, camera_x, finish_line, game_state, current_level_index, initial_velocity
    current_level_index = index
    ball = Ball(0, HEIGHT - 100)  # Positionnée en bas à gauche de l'écran
    ropes = generate_rope_chain(index)
    platforms = generate_platforms(index)
    slopes = generate_slopes(index)
    finish_line = pygame.Rect(4200, 0, 20, HEIGHT)
    camera_x = 0
    initial_velocity = pygame.Vector2(0, 0)
    if sounds_on:
        sound_manager.play_sound("starting_sound")
    if music_on:
        sound_manager.play_music(selected_music.lower().replace(" ", ""), loop=True)
    # Début avec une vitesse nulle
    game_state = "aiming"  # Lancement directement dans l'écran d'aiming

def menu_screen():


    render_text("Spidey Hook", font, RED, WIDTH // 2, 100, screen)
    draw_button(screen, "Start Game", WIDTH // 2 - 100, 200, 200, 50, GRAY, small_font, lambda: start_game("easy"))
    draw_button(screen, "Load Game", WIDTH // 2 - 100, 300, 200, 50, GRAY, small_font, lambda: set_state("load_game"))
    draw_button(screen, "Settings", 20, HEIGHT - 70, 200, 50, GRAY, small_font, lambda: set_state("settings"))

    for spider in spiders:
        spider.move()
        spider.draw(screen)

camera_x = 0  # Global

def draw_platforms(camera_x):
    # Cette fonction dessine les plateformes sur l'écran
    for platform in platforms:
        platform.draw(screen, camera_x)  # On suppose que platform.draw utilise .rect

def draw_aiming_arrow(start_pos, direction, color, length=100, segment_length=10):
    # Si la direction est un vecteur nul, on évite la normalisation
    if direction.length() == 0:
        return  # Si la direction est nulle, on ne dessine rien

    # Dessine une flèche discontinue
    for i in range(0, length, segment_length * 2):  # Laisse un espace entre chaque segment
        segment_end = start_pos + direction.normalize() * (i + segment_length)
        pygame.draw.line(screen, color, start_pos + pygame.Vector2(camera_x, 0), segment_end + pygame.Vector2(camera_x, 0), 2)

def aiming_screen():
    global initial_velocity, game_state, ball, camera_x  # Ajout de camera_x ici

    screen.fill(BLACK)

    render_text("Utilise les flèches pour viser, puis Entrée/Espace pour tirer", small_font, RED, WIDTH // 2, 50, screen)

    # Gestion des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        initial_velocity.x -= 0.2
    if keys[pygame.K_RIGHT]:
        initial_velocity.x += 0.2
    if keys[pygame.K_UP]:
        initial_velocity.y -= 0.2
    if keys[pygame.K_DOWN]:
        initial_velocity.y += 0.2

    # Si tir validé
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        ball.velocity = initial_velocity.copy()
        game_state = "playing"

    # Affichage de la flèche de visée discontinue
    draw_aiming_arrow(ball.pos, initial_velocity, GREEN, length=100)

    # Affichage de la flèche de direction (solide et de couleur différente)
    direction = initial_velocity
    pygame.draw.line(screen, WHITE, ball.pos - pygame.Vector2(camera_x, 0), ball.pos + direction * 10 - pygame.Vector2(camera_x, 0), 2)

    # Affichage de la trajectoire
    draw_trajectory(ball.pos, direction, camera_x=camera_x, steps=100, dt=0.1)

    ball.draw(screen, camera_x)
    draw_platforms(camera_x)

    # Mise à jour de la caméra
    camera_x = ball.pos.x - CAMERA_OFFSET


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
    draw_button(screen, "Easy", WIDTH // 3 - 150 // 2 - (100 // 2), HEIGHT // 2 - 150 // 2, 150, 150, GRAY, small_font, lambda: start_game("easy"))
    draw_button(screen, "Normal", WIDTH // 2 - 150 // 2, HEIGHT // 2 - 150 // 2, 150, 150, GRAY, small_font, lambda: start_game("medium"))
    draw_button(screen, "Hard", 2 * WIDTH // 3 - 150 // 2 + (100 // 2), HEIGHT // 2 - 150 // 2, 150, 150, GRAY, small_font, lambda: start_game("hard"))
    draw_button(screen, "Back", WIDTH - 220, HEIGHT - 70, 200, 50, GRAY, small_font, lambda: set_state("menu"))

def game_screen():
    global camera_x, game_state, current_level_index

    keys = pygame.key.get_pressed()
    ball.update(keys, platforms, slopes, ropes)
    camera_x = ball.pos.x - CAMERA_OFFSET

    if not ball.is_alive or ball.pos.y >= HEIGHT - ball.radius:
        if sounds_on:
            sound_manager.play_sound('Sound/game_over_sound.wav')
        game_state = "game_over"

    if pygame.Rect(ball.pos.x - ball.radius, ball.pos.y - ball.radius, ball.radius * 2, ball.radius * 2).colliderect(finish_line):
        if sounds_on:
            sound_manager.play_sound('Sound/level_up_sound.wav')
        current_level_index += 1
        if current_level_index < 4:
            start_game_by_index(current_level_index)
        else:
            if sounds_on:
                sound_manager.play_sound('Sound/end_game_sound.wav')
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

    # Gestion des différentes scènes du jeu
    if game_state == "menu":
        menu_screen()
    elif game_state == "settings":
        settings_screen()
    elif game_state == "load_game":
        load_game_screen()
    elif game_state == "aiming":
        aiming_screen()  # Affichage de la sélection de la trajectoire
    elif game_state == "playing":
        game_screen()  # Affichage du jeu une fois la trajectoire choisie
    elif game_state == "game_over":
        game_over_screen()
    elif game_state == "win_level":
        win_level_screen()

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
