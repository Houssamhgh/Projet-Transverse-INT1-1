import pygame
import sys

pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, GRAY, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (200, 200, 200), (255, 0, 0), (0, 255, 0), (
0, 0, 255)
FONT = pygame.font.Font(None, 36)

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook Menu")

# États
game_state = "menu"
music_on = True
sounds_on = True
player_name = ""
best_scores = {}  # Classement vide
selected_music = "Track 1"
input_text = ""

# Fonctions utiles
def draw_text(text, y, color=BLACK):
    surface = FONT.render(text, True, color)
    text_rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, text_rect)

def draw_button(text, y, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(WIDTH // 2 - 100, y, 200, 50)
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

if __name__ == "__main__":
    main_loop()
