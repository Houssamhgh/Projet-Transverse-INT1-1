from Constants import *
from Settings import *
from Menu import *
from Classes import *
from Levels import *
from Main import spiders


def menu_screen():
    screen.fill(BLACK)
    draw_spider_web()

    render_text("Spidey Hook", font, RED, WIDTH // 2, 100)

    draw_button("Start Game", WIDTH // 2 - 100, 200, 200, 50, GRAY, start_game)
    draw_button("Load Game", WIDTH // 2 - 100, 300, 200, 50, GRAY, lambda: set_state("load_game"))
    draw_button("Settings", 20, HEIGHT-70, 200, 50, GRAY, lambda: set_state("settings"))

    for spider in spiders:
        spider.move()
        spider.draw()



def settings_screen():
    screen.fill(BLACK)
    render_text("Settings", font, RED, WIDTH // 2, 100)

    button_width = 200
    button_height = 50
    button_x = WIDTH // 2 - button_width // 2

    draw_button(f"Music: {'On' if music_on else 'Off'}", button_x, 200, button_width, button_height, GRAY, toggle_music)
    draw_button(f"Sounds: {'On' if sounds_on else 'Off'}", button_x, 300, button_width, button_height, GRAY, toggle_sounds)
    draw_button(f"Change Music", button_x, 400, button_width, button_height, GRAY,
                change_music)
    draw_button("Back", button_x, 500, button_width, button_height, GRAY, lambda: set_state("menu"))



def set_state(state):
    global game_state
    game_state = state

def start_game():
    global game_state, ball, ropes, platforms, slopes, camera_x, finish_line
    game_state = "playing"
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    ropes = generate_rope_chain()
    platforms = generate_platforms()
    slopes = generate_slopes()
    camera_x = 0
    finish_line = pygame.Rect(4200,0,20,HEIGHT)





def load_game_screen():
    global input_text
    screen.fill(BLACK)

    render_text("Choose your level:", font, RED, WIDTH // 2, 100)



    draw_button("Easy", 25, HEIGHT//3, 150, 150, GRAY, start_game)
    draw_button("Normal", 325, HEIGHT // 3, 150, 150, GRAY, start_game)
    draw_button("Hard", 625, HEIGHT // 3, 150, 150, GRAY, start_game)
    draw_button("Back", WIDTH-220, HEIGHT-70, 200, 50, GRAY, lambda: set_state("menu"))


def game_screen():
    global game_state, camera_x, score, score_increased

    keys = pygame.key.get_pressed()
    ball.update(keys, platforms,slopes)
    camera_x = ball.pos.x - CAMERA_OFFSET

    if ball.pos.y >= HEIGHT - ball.radius or ball.is_alive==False:
        game_state = "game_over"

    # Crée un rectangle représentant la balle
    ball_rect = pygame.Rect(ball.pos.x - ball.radius, ball.pos.y - ball.radius,
                            ball.radius * 2, ball.radius * 2)

    # Vérifie la collision avec la ligne d'arrivée
    if ball_rect.colliderect(finish_line):
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

    pygame.draw.rect(screen, (0, 255, 0),
                     pygame.Rect(finish_line.x - camera_x, finish_line.y,
                                 finish_line.width, finish_line.height))

    draw_button("Menu", WIDTH - 120, 20, 100, 40, GRAY, lambda: set_state("menu"))

def game_over_screen():
    screen.fill(BLACK)
    render_text("Game Over", font, RED, WIDTH // 2, HEIGHT // 3)
    draw_button("Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, start_game)
    draw_button("Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, lambda: set_state("menu"))

def win_level_screen():
    screen.fill(BLACK)
    render_text("Congratulations", font, BLUE, WIDTH // 2, HEIGHT // 3)
    draw_button("Play Again", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, start_game)
    draw_button("Menu", WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50, GRAY, lambda: set_state("menu"))






