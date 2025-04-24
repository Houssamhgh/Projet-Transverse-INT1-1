import pygame
import random
import math
import sys

# Initialisation globale de pygame
pygame.init()

# Configuration de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Hook")
clock = pygame.time.Clock()

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

class Spider:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 3)
        self.speed_y = random.choice([-1, 1]) * random.randint(1, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > WIDTH:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)

spiders = [Spider() for _ in range(5)]

class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.anchor = pygame.Vector2(x, y)
        self.length = None

    def attach(self, ball):
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        ball.initial_velocity = ball.velocity.length()

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            keys= pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.length = max(10,self.length-2)
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length


    def draw(self, screen, ball, camera_x):
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, WHITE,
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        if ball.pos.x<4100:
            pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(8, 5)
        self.is_attached = False
        self.attached_rope = None
        self.state = ON_GROUND
        self.mass = 1.0
        self.is_alive=True

    def update(self, keys, platforms,slopes):
        if not self.is_alive:
            return
        if keys[pygame.K_SPACE]:
            if not self.is_attached:
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)
        else:
            self.is_attached = False
            self.attached_rope = None


        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.velocity.y = 0

        if self.is_attached:
            direction = self.pos - self.attached_rope.anchor
            distance = direction.length()
            if distance > 0:
                direction.normalize_ip()
                theta = math.atan2(direction.x, direction.y)
                force_tangential = self.mass * GRAVITY * math.sin(theta)
                tangent = pygame.Vector2(-direction.y, direction.x)
                self.velocity += tangent * force_tangential
                self.pos += self.velocity
                current_distance = (self.pos - self.attached_rope.anchor).length()
                if abs(current_distance - self.attached_rope.length) > 1:
                    correction = direction * (self.attached_rope.length - current_distance)
                    self.pos += correction
                    self.velocity -= direction * direction.dot(self.velocity)
        else:
            self.velocity.y += GRAVITY
            self.pos += self.velocity

        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.velocity.y = 0
            self.state = ON_GROUND

        for platform in platforms:
            if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius,
                                                     self.radius * 2, self.radius * 2)):

                if platform.bouncy:
                    self.velocity.y = -self.velocity.y * 1.5
                    self.state = ON_GROUND
                    self.is_attached = False
                else:
                    self.state = ON_GROUND
                    self.is_attached = False
                    self.is_alive = False
                    self.kill()
                    break

        for slope in slopes:
            slope.check_collision_and_bounce(ball)

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, BLUE, (self.pos.x - camera_x, self.pos.y), self.radius)


class SlopedPlatform (pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, bouncy=True):
        super().__init__()
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.bouncy = bouncy
        self.thickness = 8
        self.color = (0, 255, 0) if bouncy else (255, 0, 0)

    def draw(self, screen, camera_x):
        start = self.start - pygame.Vector2(camera_x, 0)
        end = self.end - pygame.Vector2(camera_x, 0)
        pygame.draw.line(screen, self.color, start, end, self.thickness)

    def check_collision_and_bounce(self, ball):
        # Vecteur de la pente
        line_vec = self.end - self.start
        line_unit = line_vec.normalize()
        normal = pygame.Vector2(-line_unit.y, line_unit.x)

        # Projection du centre de la balle sur la pente
        ball_to_start = ball.pos - self.start
        proj_length = ball_to_start.dot(line_unit)
        proj_length_clamped = max(0, min(proj_length, line_vec.length()))
        closest_point = self.start + proj_length_clamped * line_unit

        # Distance entre la balle et la pente
        delta = ball.pos - closest_point
        distance = delta.length()

        if distance < ball.radius:
            # Vérifie que la balle va vers la pente (collision réelle)
            if ball.velocity.dot(normal) > 0:
                # Calcule la pénétration exacte
                penetration_depth = ball.radius - distance
                if distance != 0:
                    correction_vector = delta.normalize() * penetration_depth
                else:
                    correction_vector = normal * penetration_depth  # fallback si pile sur le point

                ball.pos += correction_vector

                if self.bouncy:
                    # Rebond réaliste
                    ball.velocity = ball.velocity.reflect(normal) * 1.2
                    return True
                else:
                    ball.is_alive = False
                    ball.kill()
                    return False  # rebond non effectué
        return False


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bouncy=False):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.bouncy= bouncy

    def draw(self, screen, camera_x):
        if self.bouncy:
            pygame.draw.rect(screen, GREEN, self.rect.move(-camera_x, 0))
        else:
            pygame.draw.rect(screen, RED, self.rect.move(-camera_x, 0))



def generate_rope_chain():
    return [
        Rope(600, 50),
        Rope(1000, 150),
        Rope(1300, 200),
        Rope(2000, 100),
        Rope(2700, 70),
        Rope(3200, 100),
        Rope(3700, 80),
        Rope(4000, 50),
        Rope(5000, 100),
        ]


def generate_platforms():
    return [
        Platform(615, 400, 150, 10,bouncy=True),
        Platform(1050, 400, 150, 20,bouncy=False),
        Platform(1800, 400, 150, 20,bouncy=True),
        Platform(2700, 400, 150, 20,bouncy=False),
        Platform(3600, 400, 150, 20,bouncy=True),

    ]
def generate_slopes():
    return[
        SlopedPlatform(350, 300, 600, 400),
        SlopedPlatform(350, 100, 350,300 ),
        SlopedPlatform(4000,400, 4000, 300 ),
    ]
def draw_spider_web():
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    num_lines = 10
    for i in range(1, num_lines + 1):
        pygame.draw.circle(screen, WHITE, (center_x, center_y), i * 40, 2)

    for i in range(0, 360, 30):
        x1 = center_x + 40 * num_lines * math.cos(math.radians(i))
        y1 = center_y + 40 * num_lines * math.sin(math.radians(i))
        pygame.draw.line(screen, WHITE, (center_x, center_y), (x1, y1), 2)

def render_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, button_rect, 3)
        if mouse_click[0] == 1 and action is not None:
            pygame.time.delay(100)
            action()

    text_surface = small_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def toggle_music():
    global music_on
    music_on = not music_on

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on

def change_music(track):
    global selected_music
    selected_music = track
    print(f"Musique changée: {selected_music}")

def set_state(state):
    global game_state
    game_state = state

def start_game():
    global game_state, ball, ropes, platforms, slopes, camera_x,finish_line
    game_state = "playing"
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    ropes = generate_rope_chain()
    platforms = generate_platforms()
    slopes = generate_slopes()
    camera_x = 0
    finish_line = pygame.Rect(4200,0,20,HEIGHT)

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

def load_game_screen():
    global input_text
    screen.fill(BLACK)
    render_text("Enter your name:", font, RED, WIDTH // 2, 100)
    render_text("Please enter your name and press Enter", small_font, WHITE, WIDTH // 2, 160)

    input_box = pygame.Rect(WIDTH // 2 - 100, 200, 200, 40)
    pygame.draw.rect(screen, GRAY, input_box)
    render_text(input_text, small_font, BLACK, WIDTH // 2, 220)

    render_text("Leaderboard:", small_font, WHITE, WIDTH // 2, 300)
    render_text("No scores yet.", small_font, WHITE, WIDTH // 2, 350)

    draw_button("Confirm", WIDTH // 2 - 100, 450, 200, 50, GRAY, start_game)
    draw_button("Back", WIDTH // 2 - 100, 520, 200, 50, GRAY, lambda: set_state("menu"))

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
# Initialisation des objets du jeu
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
platforms = generate_platforms()
slopes=generate_slopes()
camera_x = 0

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
    elif game_state == "win_level":
        win_level_screen()
    elif game_state == "game_over":
        game_over_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


