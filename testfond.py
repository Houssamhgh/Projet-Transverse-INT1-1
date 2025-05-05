import pygame
import random
import time
import math

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game Configuration
GRAVITY = 0.2
MOVE_FORCE = 0.2   # Left/right movement force
DAMPING = 0.98  # Velocity damping for realistic motion
SPACE_BETWEEN_ROPES = 300  # Distance between ropes
CAMERA_OFFSET = WIDTH // 3  # Camera follows the player smoothly
JUMP_FORCE = -10  # Jumping force when the player presses space
ON_GROUND = 1  # Represents the state of the player being on the ground
IN_AIR = 0  # Represents the state of the player being in the air

# Game States
game_over = False
score = 0  # Initialize the score
score_increased = False  # Flag to track if the score has been increased

# Charger l'image de la balle
try:
    ball_image = pygame.image.load("9109569.jpg")  # Chargez l'image de la balle
    print("Image de la balle chargée avec succès!")
    ball_image = pygame.transform.scale(ball_image, (40, 40))  # Redimensionner l'image si nécessaire
except Exception as e:
    print(f"Erreur lors du chargement de l'image: {e}")

# Charger l'image de l'araignée
try:
    spider_image = pygame.image.load("9109569.jpg")  # Remplacez par le chemin de l'image de l'araignée
    spider_image = pygame.transform.scale(spider_image, (40, 40))  # Redimensionner si nécessaire
    print("Image de l'araignée chargée avec succès!")
except Exception as e:
    print(f"Erreur lors du chargement de l'image de l'araignée: {e}")

# Charger l'image du fond
background_image = pygame.image.load("144340-graphiques_vectoriels-symetrie-ligne-graphique-toile_daraignee-x750.jpg")  # Remplacez "background.jpg" par le chemin de votre image de fond
background_width = background_image.get_width()

# Fonctions de jeu et classes

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
                             (ball.pos.x - camera_x, ball.pos.y), 3)
        pygame.draw.circle(screen, (0, 255, 0), (self.anchor.x - camera_x, self.anchor.y), 6)


class Ball:
    def __init__(self, x, y, radius=10):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)
        self.is_attached = False
        self.attached_rope = None
        self.state = ON_GROUND  # Start on the ground

    def update(self, keys, platforms):
        if self.is_attached and self.attached_rope:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.velocity.x -= MOVE_FORCE
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.velocity.x += MOVE_FORCE
            self.velocity.y += GRAVITY * 0.3  # Light gravity effect while swinging
        else:
            self.velocity.y += GRAVITY  # Normal gravity when detached

        # Handle jumping
        if self.state == ON_GROUND and (keys[pygame.K_SPACE] or keys[pygame.K_w]):
            self.velocity.y = JUMP_FORCE  # Apply a jump force
            self.state = IN_AIR  # The ball is in the air now

        self.pos += self.velocity
        self.velocity *= DAMPING  # Apply damping for smooth motion

        # Check for ground collision (bottom of the screen)
        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius  # Stop at the bottom
            self.velocity.y = 0  # Stop downward velocity
            self.state = ON_GROUND  # Back to the ground

        # Collision with platforms (bounce)
        for platform in platforms:
            if platform.rect.colliderect(pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)):
                if self.velocity.y > 0:  # Only bounce when falling
                    self.velocity.y = -self.velocity.y * 0.8  # Reverse velocity and apply some dampening
                    self.pos.y = platform.rect.top - self.radius  # Move ball on top of the platform
                    self.state = ON_GROUND  # The ball is on the ground again

    def toggle_attachment(self, ropes):
        if self.is_attached:
            self.is_attached = False
            self.attached_rope = None
        else:
            closest_rope = min(ropes, key=lambda rope: abs(rope.anchor.x - self.pos.x))
            closest_rope.attach(self)

    def draw(self, screen, camera_x):
        screen.blit(spider_image, (self.pos.x - camera_x - 20, self.pos.y - 20))  # Afficher l'araignée


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, (255, 0, 0), self.rect.move(-camera_x, 0))  # Draw red platform


# Fonctions pour générer des éléments du jeu

def generate_rope_chain():
    """ Creates an initial set of ropes."""
    return [Rope(WIDTH // 2 + i * SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)) for i in range(5)]


def generate_platforms():
    """ Creates some platforms in the game."""
    return [
        Platform(100, 400, 150, 20),
        Platform(300, 400, 200, 20),
        Platform(200, 400, 150, 20),
        Platform(500, 300, 100, 20),
        Platform(700, 300, 100, 20),
        Platform(2000, 500, 200, 20),
        Platform(2300, 400, 150, 20),
        Platform(3000, 400, 100, 20),
        Platform(3500, 400, 100, 20),
        Platform(4000, 400, 100, 20),
        Platform(4500, 400, 150, 20),
        Platform(5000, 400, 100, 20),
        Platform(5500, 500, 150, 20),
        Platform(6000, 400, 100, 20),
        Platform(6500, 400, 150, 20),
        Platform(7000, 500, 150, 20),
        Platform(7500, 400, 100, 20)
    ]


# Fonction pour dessiner le fond
def draw_background(screen, camera_x):
    # Calculer la position du fond en fonction de la position de la caméra
    scroll_x = camera_x % background_width  # La position de l'image défilera

    # Dessiner le fond à la position calculée, en deux parties pour créer l'effet de boucle
    screen.blit(background_image, (-scroll_x, 0))  # Partie gauche
    if scroll_x != 0:  # Pour éviter un espace vide lorsque l'image est alignée à gauche
        screen.blit(background_image, (background_width - scroll_x, 0))  # Partie droite


# Initialisation des objets du jeu
ball = Ball(WIDTH // 2, HEIGHT // 2)
ropes = generate_rope_chain()
platforms = generate_platforms()
camera_x = 0

# Boucle principale du jeu
running = True
while running:
    screen.fill((0, 0, 0))  # Effacer l'écran

    # Dessiner le fond qui défile
    draw_background(screen, camera_x)

    # Vérification si le jeu est terminé
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))  # Rendre le texte 'Game Over'
        screen.blit(text, (WIDTH // 3, HEIGHT // 3))  # Afficher le texte
        pygame.display.flip()
        pygame.time.delay(2000)  # Afficher le message pendant 2 secondes
        running = False
        continue

    # Vérification des événements
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball.toggle_attachment(ropes)

    # Mise à jour de l'état du jeu
    ball.update(keys, platforms)
    camera_x = max(camera_x, ball.pos.x - CAMERA_OFFSET)

    # Vérifier si la balle touche le bas (condition de fin de jeu)
    if ball.pos.y >= HEIGHT - ball.radius:
        game_over = True

    for rope in ropes:
        rope.update(ball)

    # Générer de nouvelles cordes dynamiquement
    if ropes[-1].anchor.x - camera_x < WIDTH:
        ropes.append(Rope(ropes[-1].anchor.x + SPACE_BETWEEN_ROPES, HEIGHT // 4 + random.randint(-50, 50)))

    # Supprimer les cordes hors de la vue
    ropes = [rope for rope in ropes if rope.anchor.x - camera_x > -150]

    # Incrémenter le score seulement quand la balle se fixe à une corde
    if ball.is_attached and ball.attached_rope and not score_increased:
        score += 1  # Augmenter le score
        score_increased = True  # Empêcher les incréments multiples

    if not ball.is_attached:
        score_increased = False

    # Rendre les objets
    for rope in ropes:
        rope.draw(screen, ball, camera_x)
    ball.draw(screen, camera_x)

    # Rendre les plateformes
    for platform in platforms:
        platform.draw(screen, camera_x)

    # Afficher le score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # Afficher le score en haut à gauche

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la fréquence des images à 60 FPS
    clock.tick(60)

pygame.quit()
