import pygame
import random
import math

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game Configuration
GRAVITY = 0.2
MOVE_FORCE = 0.2
DAMPING = 0.98
CAMERA_OFFSET = WIDTH // 3
JUMP_FORCE = -10
ON_GROUND = 1
IN_AIR = 0

# Load images
try:
    spider_image = pygame.image.load("9109569.jpg")
    spider_image = pygame.transform.scale(spider_image, (40, 40))
except:
    spider_image = pygame.Surface((40, 40))
    spider_image.fill((255, 255, 255))

try:
    background_image = pygame.image.load("144340-graphiques_vectoriels-symetrie-ligne-graphique-toile_daraignee-x750.jpg")
    background_width = background_image.get_width()
except:
    background_image = pygame.Surface((800, 600))
    background_image.fill((0, 0, 0))
    background_width = 800

# Game State
score = 0
game_over = False

class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)
        self.length = None

    def attach(self, ball):
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached = True
        ball.attached_rope = self

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length

    def draw(self, screen, ball, camera_x):
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, (255, 255, 255), (self.anchor.x - camera_x, self.anchor.y), (ball.pos.x - camera_x, ball.pos.y), 2)
        pygame.draw.circle(screen, (0, 255, 0), (int(self.anchor.x - camera_x), int(self.anchor.y)), 5)

class Platform:
    def __init__(self, x, y, width, height, shape_type='rectangle'):
        self.rect = pygame.Rect(x, y, width, height)
        self.shape_type = shape_type
        self.color = [random.randint(0, 255) for _ in range(3)]  # Couleur aléatoire

    def draw(self, screen, camera_x):
        if self.shape_type == 'rectangle':
            pygame.draw.rect(screen, self.color, self.rect.move(-camera_x, 0), border_radius=15)  # Rectangle arrondi
        elif self.shape_type == 'circle':
            # Correction ici, avec un tuple pour le centre (x, y)
            pygame.draw.circle(screen, self.color, (self.rect.centerx - camera_x, self.rect.centery), self.rect.width // 2)

class Ball:
    def __init__(self, x, y, radius=10):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.is_attached = False
        self.attached_rope = None
        self.state = IN_AIR

    def update(self, keys, platforms):
        if self.is_attached:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocity.x -= MOVE_FORCE
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocity.x += MOVE_FORCE
            self.velocity.y += GRAVITY * 0.3
        else:
            self.velocity.y += GRAVITY

        if self.state == ON_GROUND and (keys[pygame.K_SPACE] or keys[pygame.K_w]):
            self.velocity.y = JUMP_FORCE
            self.state = IN_AIR

        self.pos += self.velocity
        self.velocity *= DAMPING

        # Collision
        for platform in platforms:
            if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)):
                if platform.shape_type == 'circle':
                    if self.velocity.y > 0 and (self.pos - pygame.Vector2(platform.rect.centerx, platform.rect.centery)).length() < self.radius + platform.rect.width // 2:
                        self.velocity.y *= -1.2
                        self.velocity.x += random.uniform(-2, 2)
                        self.pos.y = platform.rect.top - self.radius
                        self.state = ON_GROUND
                else:
                    if self.velocity.y > 0:
                        self.velocity.y *= -1.4  # Augmentation du rebond
                        self.velocity.x += random.uniform(-2, 2)
                        self.pos.y = platform.rect.top - self.radius
                        self.state = ON_GROUND

        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.velocity.y = 0
            self.state = ON_GROUND

    def toggle_attachment(self, ropes):
        if self.is_attached:
            self.is_attached = False
            self.attached_rope = None
        else:
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)

    def draw(self, screen, camera_x):
        screen.blit(spider_image, (self.pos.x - camera_x - 20, self.pos.y - 20))

def generate_rope_chain():
    return [Rope(WIDTH // 2 + i * 300, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]

def generate_platforms():
    platforms = []
    for i in range(20):
        x = i * 400 + 100
        if i % 3 == 0:
            platforms.append(Platform(x, random.randint(300, 500), 40, 40, shape_type='circle'))  # Cercles
        else:
            platforms.append(Platform(x, random.randint(300, 500), random.randint(100, 200), 20, shape_type='rectangle'))  # Rectangles arrondis
    return platforms

def draw_background(screen, camera_x):
    scroll_x = camera_x % background_width
    screen.blit(background_image, (-scroll_x, 0))
    if scroll_x != 0:
        screen.blit(background_image, (background_width - scroll_x, 0))

# Initialisation
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
platforms = generate_platforms()
camera_x = 0

running = True
while running:
    screen.fill((0, 0, 0))
    draw_background(screen, camera_x)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball.toggle_attachment(ropes)

    ball.update(keys, platforms)

    for rope in ropes:
        rope.update(ball)

    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + 300, HEIGHT // 4 + random.randint(-50, 50)))

    camera_x = max(camera_x, ball.pos.x - CAMERA_OFFSET)

    for rope in ropes:
        rope.draw(screen, ball, camera_x)

    for platform in platforms:
        platform.draw(screen, camera_x)

    ball.draw(screen, camera_x)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {int(ball.pos.x / 100)}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
