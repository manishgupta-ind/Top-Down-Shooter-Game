import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Set up colors
BACKGROUND = (20, 20, 30)  # Dark blue-ish background
BLUE = (0, 100, 255)       # Player color
RED = (255, 0, 0)          # Enemy/Bullet color
WHITE = (255, 255, 255)    # Text color

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 10

# Enemy settings
ENEMY_SIZE = 50
ENEMY_SPEED = 2
ENEMY_SPAWN_TIME = 1500  # milliseconds (1.5 seconds)

# Font setup
pygame.font.init()
font_large = pygame.font.SysFont('Arial', 64)  # For game over text
font_small = pygame.font.SysFont('Arial', 24)  # For score display

# Player class
class Player:
    def __init__(self):
        # Start at the center-bottom of the screen
        self.x = WIDTH // 2 - PLAYER_SIZE // 2
        self.y = HEIGHT - PLAYER_SIZE - 50
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shoot_cooldown = 0

    def update(self, keys):
        # Handle movement based on key presses
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Limit movement to window boundaries
        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            # Create a bullet at the center-top of the player
            bullet_x = self.x + (self.width // 2) - (BULLET_WIDTH // 2)
            bullet_y = self.y
            self.shoot_cooldown = 10  # Add a small cooldown between shots
            return Bullet(bullet_x, bullet_y)
        return None

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        # Move bullet upward
        self.y -= self.speed
        self.rect.y = self.y

        # Check if bullet is off screen
        if self.y + self.height < 0:
            return True  # Return True if bullet should be removed
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# Enemy class
class Enemy:
    def __init__(self):
        # Start at a random x position at the top of the screen
        self.width = ENEMY_SIZE
        self.height = ENEMY_SIZE
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height  # Start just above the screen
        self.speed_y = ENEMY_SPEED

        # Random horizontal movement parameters
        self.speed_x = random.uniform(0.5, 2.0) * random.choice([-1, 1])
        self.amplitude = random.randint(20, 100)  # How far it moves side to side
        self.frequency = random.uniform(0.01, 0.05)  # How fast it oscillates
        self.time = random.uniform(0, 6.28)  # Random starting phase (0 to 2π)

        # Starting position for oscillation
        self.center_x = self.x

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        # Move enemy downward
        self.y += self.speed_y

        # Calculate horizontal position with sinusoidal movement
        self.time += self.frequency
        self.x = self.center_x + math.sin(self.time) * self.amplitude

        # Keep enemy within screen boundaries
        self.x = max(0, min(self.x, WIDTH - self.width))

        # Update rectangle position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Check if enemy is off screen
        if self.y > HEIGHT:
            return True  # Return True if enemy should be removed
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# Function to display game over text
def show_game_over(score):
    game_over_text = font_large.render("GAME OVER", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(game_over_text, text_rect)

    # Display final score
    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 70))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    # Wait for a moment before quitting
    pygame.time.wait(2000)

# Create player
player = Player()

# Create lists for bullets and enemies
bullets = []
enemies = []

# Set up enemy spawning timer
enemy_spawn_timer = pygame.time.get_ticks()

# Game state
game_over = False
running = True
clock = pygame.time.Clock()
score = 0  # Initialize score

# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Handle shooting
        if keys[pygame.K_SPACE]:
            bullet = player.shoot()
            if bullet:
                bullets.append(bullet)

        # Update player
        player.update(keys)

        # Update bullets
        for bullet in bullets[:]:
            if bullet.update():
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies[:]:
            if enemy.update():
                enemies.remove(enemy)

        # Check for collisions between bullets and enemies
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet not in bullets_to_remove:
                        bullets_to_remove.append(bullet)
                    if enemy not in enemies_to_remove:
                        enemies_to_remove.append(enemy)

        # Remove collided bullets and enemies
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)

        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)
                score += 10  # Increase score by 10 for each enemy destroyed

        # Check for collisions between player and enemies
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                game_over = True
                break

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer > ENEMY_SPAWN_TIME:
            enemies.append(Enemy())
            enemy_spawn_timer = current_time

        # Fill the background
        screen.fill(BACKGROUND)

        # Draw player
        player.draw(screen)

        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Display score
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        # Update the display
        pygame.display.flip()

    else:
        # Show game over screen
        show_game_over(score)
        running = False

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
