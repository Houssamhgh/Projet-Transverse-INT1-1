import pygame
import random
import math

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game Configuration
MASS = 0.05
GRAVITATIONAL_CONST = 9.81
GRAVITY = MASS * GRAVITATIONAL_CONST
SPACE_BETWEEN_ROPES = 300  # Distance between ropes
CAMERA_OFFSET = WIDTH // 3  # Camera follows the player smoothly
ON_GROUND = False

# Game States
game_over = False
score = 0  # Initialize the score
score_increased = False  # Flag to track if the score has been increased


class Rope:
    def __init__(self, x, y):
        self.anchor = pygame.Vector2(x, y)
        self.length = None  # Will be set when attached

    def attach(self, ball):
        """ Sets the rope length dynamically based on ball position."""
        self.length = (ball.pos - self.anchor).length()
        ball.is_attached, ball.attached_rope = True, self
        # Store the initial velocity magnitude when attached
        ball.initial_velocity = ball.velocity.length()

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
        self.velocity = pygame.Vector2(8 , 5)  # Start with zero velocity
        self.is_attached = False
        self.attached_rope = None
        self.state = ON_GROUND  # Start on the ground
        self.mass = 1.0  # Mass of the ball (for physics)

    def update(self, keys, platforms):
        if keys[pygame.K_SPACE]:  # Attach to rope when space is pressed
            if not self.is_attached:  # If not already attached
                closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
                closest_rope.attach(self)
        else:
            self.is_attached = False
            self.attached_rope = None

        if self.is_attached:
            # Pendulum physics
            direction = self.pos - self.attached_rope.anchor
            distance = direction.length()
            if distance > 0:
                direction.normalize_ip()
                # Calculate the angle theta between the rope and the vertical
                theta = math.atan2(direction.x, direction.y)
                # Calculate the tangential force (F_t = m * g * sin(theta))
                force_tangential = self.mass * GRAVITY * math.sin(theta)
                # Update velocity based on the tangential force
                tangent = pygame.Vector2(-direction.y, direction.x)
                self.velocity += tangent * force_tangential
                # Update position
                self.pos += self.velocity
                # Correct the position to maintain rope length
                current_distance = (self.pos - self.attached_rope.anchor).length()
                if abs(current_distance - self.attached_rope.length) > 1:  # Allow a small tolerance
                    correction = direction * (self.attached_rope.length - current_distance)
                    self.pos += correction
                    # Adjust velocity to prevent drifting
                    self.velocity -= direction * direction.dot(self.velocity)
        else:
            self.velocity.y += GRAVITY  # Gravity
            self.pos += self.velocity

        # Check for ground collision (bottom of the screen)
        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius  # Stop at the bottom
            self.velocity.y = 0  # Stop downward velocity
            self.state = ON_GROUND  # Back to the ground

        # Collision with platforms (bounce)
        for platform in platforms:
            if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)):
                self.velocity.y = -self.velocity.y * 1.3  # Reverse velocity and apply some dampening
                #self.pos.y = platform.rect.top - self.radius  # Move ball on top of the platform
                self.state = ON_GROUND  # The ball is on the ground again
                ball.is_attached = False



    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, (0, 0, 255), (self.pos.x - camera_x, self.pos.y), self.radius)


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, 0))  # Draw red platform


def generate_rope_chain():
    """ Creates an initial set of ropes."""
    return [Rope(WIDTH // 2 + i * SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]


def generate_platforms():
    """ Creates some platforms in the game."""
    return [
        Platform(100, 400, 150, 10),
        Platform(300, 400, 200, 20),
        Platform(200, 400, 150, 20),
        Platform(800, 500, 200, 10),
        Platform(1000, 400, 150, 20),
        Platform(3000, 400, 100, 20)
    ]


# Initialize game objects
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
platforms = generate_platforms()
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
    ball.update(keys, platforms)
    camera_x = ball.pos.x - CAMERA_OFFSET

    # Check for ball hitting the bottom (game over condition)
    if ball.pos.y >= HEIGHT - ball.radius :
        game_over = True

    for rope in ropes:
        rope.update(ball)

    # Generate new ropes dynamically
    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))


    # Increment score only when ball attaches to a rope and hasn't been increased yet
    if ball.is_attached and ball.attached_rope and not score_increased:
        score += 1  # Increase the score
        score_increased = True  # Set flag to prevent multiple increments

    # Reset the score flag if the ball gets detached
    if not ball.is_attached:
        score_increased = False

    # Render objects
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)

    # Render platforms
    for platform in platforms:
        platform.draw(screen, camera_x)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Display score at top-left corner

    # Update the display
    pygame.display.flip()

    # Limiting frame rate
    clock.tick(60)

pygame.quit()