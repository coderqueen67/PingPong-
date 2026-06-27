import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 6

# Ball dimensions
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PingPong Mouse Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Font for displaying scores
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
    
    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, 
                               SCREEN_HEIGHT // 2 - BALL_SIZE // 2, 
                               BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1
        
        # Keep ball in bounds vertically
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def check_paddle_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            if self.speed_x > 0:
                self.rect.right = paddle.rect.left
            else:
                self.rect.left = paddle.rect.right
            self.speed_x *= -1
            # Add variation to ball trajectory
            self.speed_y += random.randint(-2, 2)
    
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
    
    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])

def draw_center_line():
    """Draw the center dashed line"""
    for y in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 2, y), 
                        (SCREEN_WIDTH // 2, y + 10), 2)

def main():
    # Create paddles
    paddle1 = Paddle(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    
    # Create ball
    ball = Ball()
    
    # Scores
    score1 = 0
    score2 = 0
    
    # Game running flag
    running = True
    
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    # Reset game
                    ball.reset()
                    score1 = 0
                    score2 = 0
        
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (W/S keys)
        if keys[pygame.K_w]:
            paddle1.move_up()
        if keys[pygame.K_s]:
            paddle1.move_down()
        
        # Player 2 controls (UP/DOWN arrow keys)
        if keys[pygame.K_UP]:
            paddle2.move_up()
        if keys[pygame.K_DOWN]:
            paddle2.move_down()
        
        # Update ball
        ball.update()
        
        # Check paddle collisions
        ball.check_paddle_collision(paddle1)
        ball.check_paddle_collision(paddle2)
        
        # Check if ball is out of bounds
        if ball.rect.left < 0:
            score2 += 1
            ball.reset()
        elif ball.rect.right > SCREEN_WIDTH:
            score1 += 1
            ball.reset()
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw center line
        draw_center_line()
        
        # Draw paddles
        paddle1.draw(screen)
        paddle2.draw(screen)
        
        # Draw ball
        ball.draw(screen)
        
        # Draw scores
        score_text1 = font_large.render(str(score1), True, WHITE)
        score_text2 = font_large.render(str(score2), True, WHITE)
        screen.blit(score_text1, (SCREEN_WIDTH // 4, 50))
        screen.blit(score_text2, (3 * SCREEN_WIDTH // 4 - 50, 50))
        
        # Draw instructions
        instructions = font_small.render("W/S - P1 | UP/DOWN - P2 | R - Reset | ESC - Quit", True, GRAY)
        screen.blit(instructions, (50, SCREEN_HEIGHT - 50))
        
        # Update display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
