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
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Polices
small_font = pygame.font.SysFont("Arial", 30)

# Constantes du jeu
MASS = 0.05
GRAVITATIONAL_CONST = 9.81
GRAVITY = MASS * GRAVITATIONAL_CONST
SPACE_BETWEEN_ROPES = 300
CAMERA_OFFSET = WIDTH // 3
ON_GROUND = False

class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)
        self.length = None

    def attach(self, ball):
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        ball.initial_velocity = ball.velocity.length()

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length

    def draw(self, screen, ball, camera_x):
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, WHITE,
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)

class Ball:
    def __init__(self, x, y, radius=10):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(8, 5)
        self.is_attached = False
        self.attached_rope = None
        self.state = ON_GROUND
        self.mass = 1.0


    def update(self, keys, platforms):
        if keys[pygame.K_SPACE]:
            if not self.is_attached:
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)
        else:
            self.is_attached = False
            self.attached_rope = None

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
                self.velocity.y = -self.velocity.y * 1.3
                self.state = ON_GROUND
                self.is_attached = False

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, BLUE, (self.pos.x - camera_x, self.pos.y), self.radius)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, RED, self.rect.move(-camera_x, 0))

def generate_rope_chain():
    return [Rope(WIDTH // 2 + i * SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)) for i in range(2)]

def generate_platforms():
    return [
        Platform(100, 400, 150, 10),
        Platform(300, 400, 200, 20),
        Platform(200, 400, 150, 20),
        Platform(800, 500, 200, 10),
        Platform(1000, 400, 150, 20),
        Platform(3000, 400, 100, 20)
    ]

# Initialisation des objets du jeu
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
platforms = generate_platforms()
camera_x = 0
score = 0
score_increased = False

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    ball.update(keys, platforms)
    camera_x = ball.pos.x - CAMERA_OFFSET

    for rope in ropes:
        rope.update(ball)

    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))

    if ball.is_attached and ball.attached_rope and not score_increased:
        score += 1
        score_increased = True

    if not ball.is_attached:
        score_increased = False

    if ball.pos.y >= HEIGHT - ball.radius:
        running = False
    screen.fill(BLACK)
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)
    for platform in platforms:
        platform.draw(screen, camera_x)

    score_text = small_font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

