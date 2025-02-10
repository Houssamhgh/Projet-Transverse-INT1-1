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
SPACE_BETWEEN_ROPES = 300  # Distance between ropes
camera_x = 0  # Camera position


class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)  # Fixed point
        self.length = None  # Dynamic length (set when attaching)

    def attach(self, ball):
        """ Sets the rope length to the ball's current distance when attached. """
        self.length = (ball.pos - self.anchor).length()

    def update(self, ball):
        if ball.is_attached and ball.attached_rope == self:
            # Keep ball at fixed rope length
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
        self.attached_rope = None
        self.is_attached = False
        self.velocity = pygame.Vector2(0, 0)

    def update(self, keys):
        if self.is_attached and self.attached_rope:
            # Swinging physics
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocity.x -= MOVE_FORCE
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocity.x += MOVE_FORCE

            # Apply motion with slight gravity effect
            self.velocity.y += GRAVITY * 0.3
            self.pos += self.velocity
            self.velocity *= 0.98  # Damping for realistic motion
        else:
            # Gravity when detached
            self.velocity.y += GRAVITY
            self.pos += self.velocity

    def toggle_attachment(self, ropes):
        if self.is_attached:
            self.is_attached = False
            self.attached_rope = None
        else:
            # Attach to the closest rope
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)  # Set rope length dynamically
            self.attached_rope = closest_rope
            self.is_attached = True
            self.velocity = pygame.Vector2(0, 0)  # Reset velocity for smooth swinging

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, (0, 0, 255), (self.pos.x - camera_x, self.pos.y), self.radius)


# Create Objects
ball = Ball(WIDTH // 10, HEIGHT // 10)
ropes = [Rope(WIDTH // 2 + i * SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]

running = True
while running:
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()  # Get keys for movement

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.toggle_attachment(ropes)

    # Update Ball
    ball.update(keys)

    # Move the camera smoothly to follow the ball
    camera_x = max(camera_x, ball.pos.x - WIDTH // 3)

    # Update Ropes
    for rope in ropes:
        rope.update(ball)

    # Generate new ropes dynamically
    if ropes[-1].anchor.x - camera_x < WIDTH:
        new_rope_x = ropes[-1].anchor.x + SPACE_BETWEEN_ROPES
        new_rope_y = HEIGHT // 4 + random.randint(-50, 50)
        ropes.append(Rope(new_rope_x, new_rope_y))

    # Remove ropes that move out of view
    ropes = [rope for rope in ropes if rope.anchor.x - camera_x > -150]

    # Draw everything
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
