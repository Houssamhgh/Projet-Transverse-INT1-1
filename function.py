import pygame
import random

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game Configuration
GRAVITY = 0.5
MOVE_FORCE = 0.5  # Left/right movement force
DAMPING = 0.98  # Velocity damping for realistic motion
SPACE_BETWEEN_ROPES = 300  # Distance between ropes
CAMERA_OFFSET = WIDTH // 3  # Camera follows the player smoothly


class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)
        self.length = None  # Will be set when attached

    def attach(self, ball):
        """ Sets the rope length dynamically based on ball position."""
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        ball.velocity = pygame.Vector2(0, 0)  # Reset velocity

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            direction = ball.pos - self.anchor
            distance = direction.length()
            if distance > self.length:
                ball.pos = self.anchor + direction.normalize() * self.length

    def draw(self, screen, ball, camera_x):
        if ball.is_attached and ball.attached_rope == self:
            pygame.draw.line(screen, (255, 255, 255),
                             (self.anchor.x - camera_x, self.anchor.y),
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)


class Ball:
    def __init__(self, x, y, radius=10):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)
        self.is_attached = False
        self.attached_rope = None

    def update(self, keys):
        if self.is_attached and self.attached_rope:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocity.x -= MOVE_FORCE
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocity.x += MOVE_FORCE
            self.velocity.y += GRAVITY * 0.3  # Light gravity effect while swinging
        else:
            self.velocity.y += GRAVITY  # Normal gravity when detached

        self.pos += self.velocity
        self.velocity *= DAMPING  # Apply damping for smooth motion

    def toggle_attachment(self, ropes):
        if self.is_attached:
            self.is_attached = False
            self.attached_rope = None
        else:
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, (0, 0, 255), (self.pos.x - camera_x, self.pos.y), self.radius)


def generate_rope_chain():
    """ Creates an initial set of ropes."""
    return [Rope(WIDTH // 2 + i * SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]


# Initialize game objects
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
camera_x = 0

running = True
while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball.toggle_attachment(ropes)

    # Update game state
    ball.update(keys)
    camera_x = max(camera_x, ball.pos.x - CAMERA_OFFSET)
    for rope in ropes:
        rope.update(ball)

    # Generate new ropes dynamically
    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))

    # Remove out-of-view ropes
    ropes = [rope for rope in ropes if rope.anchor.x - camera_x > -150]

    # Render objects
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
