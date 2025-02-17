import random
import pygame

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Configuration
MASS = 0.008
GRAVITATIONAL_CONST = 9.81
GRAVITY = MASS * GRAVITATIONAL_CONST
MOVE_FORCE = 0.3  # Left/right movement force
SPACE_BETWEEN_ROPES = 300  # Distance between ropes
CAMERA_OFFSET = WIDTH // 3  # Camera follows the player smoothly

# Game States
game_over = False


class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)
        self.length = None  # Will be set when attached

    def attach(self, ball):
        """ Sets the rope length dynamically based on ball position."""
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self

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
                             (ball.pos.x - camera_x, ball.pos.y), 1)
        pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)


class Ball:
    def __init__(self, x, y, radius=10):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(5, 0)
        self.is_attached = False
        self.attached_rope = None

    def update(self, keys, ropes):
        if keys[pygame.K_SPACE]:  # Attach to rope when space is pressed
            if not self.is_attached:  # If not already attached
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)
        else:
            self.is_attached = False
            self.attached_rope = None

        if not self.is_attached:
            self.velocity.y += GRAVITY  # Gravity

        self.pos += self.velocity

        # Collision with the ground (game over condition)
        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.velocity.y = 0

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, (0, 0, 255), (self.pos.x - camera_x, self.pos.y), self.radius)


def generate_rope_chain():
    """ Creates an initial set of ropes."""
    return [Rope(WIDTH // 2 + i * SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]


# Initialize game objects
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
camera_x = 0

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black background

    # Check if the game is over
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))  # Render 'Game Over' text
        screen.blit(text, (WIDTH // 3, HEIGHT // 3))  # Display text
        pygame.display.flip()
        pygame.time.delay(2000)  # Show the message for 2 seconds
        running = False
        continue

    # Check for events
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    ball.update(keys, ropes)
    camera_x = ball.pos.x - CAMERA_OFFSET  # Camera follows the ball

    # Check for ball hitting the bottom (game over condition)
    if ball.pos.y >= HEIGHT - ball.radius:
        game_over = True

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

    # Update the display
    pygame.display.flip()

    # Limiting frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
