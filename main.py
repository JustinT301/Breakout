"""
Breakout Game
"""

import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 600, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FPS = 30

# Initialize Pygame
pygame.init()

# Initialize Pygame fonts
font = pygame.font.Font('freesansbold.ttf', 15)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

# Global variables
lives = 3
score = 0
score_file = "high_scores.txt"

# Function to read high scores from file
def read_scores():
    if os.path.exists(score_file):
        with open(score_file, 'r') as file:
            scores = file.readlines()
            scores = [line.strip().split() for line in scores]
            scores = [(int(score), initials) for score, initials in scores]
            scores.sort(reverse=True, key=lambda x: x[0])
            return scores[:10]  # Return top 10 scores
    else:
        return []

# Function to write high scores to file
def write_score(score, initials):
    scores = read_scores()
    scores.append((score, initials))
    scores.sort(reverse=True, key=lambda x: x[0])
    with open(score_file, 'w') as file:
        for score, initials in scores[:10]:
            file.write(f"{score} {initials}\n")

# Function to display high scores
def display_scores():
    scores = read_scores()
    screen.fill(BLACK)
    title_text = font.render("High Scores", True, WHITE)
    title_rect = title_text.get_rect()
    title_rect.center = (WIDTH // 2, 50)
    screen.blit(title_text, title_rect)

    y_position = 100
    for i, (score, initials) in enumerate(scores, start=1):
        score_text = font.render(f"{i}. {initials}: {score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.center = (WIDTH // 2, y_position)
        screen.blit(score_text, score_rect)
        y_position += 30

    pygame.display.update()

# Collision check
def collision_checker(rect, ball):
    """
    Check if the ball collides with a given rectangle.

    Parameters:
    rect (pygame.Rect): The rectangle to check collision with.
    ball (pygram.Rect): The ball's rectangle.

    Returns:
    bool: True if collision occurs, False otherwise.
    """
    return rect.colliderect(ball)

# Create blocks with different colors and point values
def create_blocks(block_width, block_height, horizontal_gap, vertical_gap):
    """
    Create a list of blocks with random colors and point values.

    Parameters: 
    block_width (int): Width of each block.
    block_height (int): Height of each block.
    horizontal_gap (int): Horizontal gap between blocks.
    vertical_gap (int): Vertical gap between blocks.

    Returns:
    list: List of block objects.
    """
    block_list = []

    colors = [WHITE, GREEN, RED, BLUE, YELLOW]
    points = [10, 5, 15, 20, 25]

    for i in range(0, WIDTH, block_width + horizontal_gap):
        for j in range(0, HEIGHT // 2, block_height + vertical_gap):
            color = random.choice(colors)
            points_value = points[colors.index(color)]
            block_list.append(Block(i, j, block_width, block_height, color, points_value))

    return block_list

# Start menu
def start_menu():
    """
    Display Start menu after booting up the game
    """
    start_menu = True

    while start_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                if event.key == pygame.K_SPACE:
                    return True

        screen.fill(BLACK)
        start_menu_text = font.render("Breakout!", True, WHITE)
        start_menu_rect = start_menu_text.get_rect()
        start_menu_rect.center = (WIDTH // 2, HEIGHT // 2 - 20)
        screen.blit(start_menu_text, start_menu_rect)

        start_text = font.render("Press SPACE to Play", True, WHITE)
        start_rect = start_text.get_rect()
        start_rect.center = (WIDTH // 2, HEIGHT // 2 + 20)
        screen.blit(start_text, start_rect)

        pygame.display.update()
        clock.tick(FPS)

# Game Over screen
def game_over():
    """
    Display the game over screen and handle user input for restarting or quitting.
    """
    global lives, score
    game_over = True
    initials_entered = False
    player_initials = ""

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                if not initials_entered:
                    if event.key == pygame.K_RETURN:
                        # Get player initials and write score
                        write_score(score, player_initials.upper())
                        initials_entered = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_initials = player_initials[:-1]
                    else:
                        player_initials += event.unicode.upper()
                    if len(player_initials) > 3:
                        player_initials = player_initials[:3]

                if initials_entered and event.key == pygame.K_SPACE:
                    # Reset game variables
                    score = 0
                    lives = 3
                    return True

        screen.fill(BLACK)

        if not initials_entered:
            # Display "Enter your initials" screen
            input_text = font.render("Enter your initials:", True, WHITE)
            input_rect = input_text.get_rect()
            input_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(input_text, input_rect)

            initials_text = font.render(player_initials, True, WHITE)
            initials_rect = initials_text.get_rect()
            initials_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
            screen.blit(initials_text, initials_rect)

        else:
            # Display high scores
            display_scores()

            game_over_text = font.render("Game Over!", True, WHITE)
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (WIDTH // 2, HEIGHT // 2 + 180)
            screen.blit(game_over_text, game_over_rect)

            exit_text = font.render("Press SPACE to Play Again", True, WHITE)
            exit_rect = exit_text.get_rect()
            exit_rect.center = (WIDTH // 2, HEIGHT // 2 + 225)
            screen.blit(exit_text, exit_rect)

        pygame.display.update()
        clock.tick(FPS)

    # Display "Game Over" screen
    screen.fill(BLACK)

    pygame.display.update()
    clock.tick(FPS)

# Function to initialize game
def initialize_game(level=1):
    """
    Initialize the game variables and create game objects.
    """
    global paddle, ball, block_list

    wall_sound = pygame.mixer.Sound('sounds/wall.wav')
    lose_life_sound = pygame.mixer.Sound('sounds/lose_life.wav')

    paddle = Paddle(WIDTH // 2 - 50, HEIGHT - 50, 100, 5, 10, WHITE) ##############
    ball = Ball(WIDTH // 2, HEIGHT - 150, 7, 7, WHITE, wall_sound, lose_life_sound)

    block_width, block_height = 40, 15
    horizontal_gap, vertical_gap = 20, 20

    # Create blocks based on current level
    if level == 1:
        block_list = create_blocks(block_width, block_height, horizontal_gap, vertical_gap)
    elif level == 2:
        block_list = create_blocks(block_width, block_height, horizontal_gap, vertical_gap)
        # Creating blocks for level 2
    elif level == 3:
        block_list = create_blocks(block_width, block_height, horizontal_gap, vertical_gap)
        # Creating blocks for level 3

# Class for Paddle
class Paddle:
    """
    Initialize a Paddle Object.

    Parameters:
    posx (int): Initial x position.
    posy (int): Initial y position.
    width (int): Width of the paddle.
    height (int): Height of the paddle.
    speed (int): Speed of the paddle.
    color (tuple): Color of the paddle.
    """
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color
        self.paddle_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.paddle_x_fac = 0  # To store movement direction

    def display(self):
        """
        Draw the paddle on the screen.
        """
        pygame.draw.rect(screen, self.color, self.paddle_rect)

    def update(self):
        """
        Update the paddle's position based on user input.
        """
        self.posx += self.speed * self.paddle_x_fac

        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width
        
        self.paddle_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def set_movement(self, x_fac):
        """
        Set the movement direction of the paddle.

        Parameters:
        x_fac (int): Direction factor (-1 for left, 1 for right, 0 for stop)
        """
        self.paddle_x_fac = x_fac

    def get_rect(self):
        """
        Get the rectangle representation of the paddle.

        Returns: 
        pygame.Rect: The paddle's rectangle
        """
        return self.paddle_rect

# Class for Block
class Block:
    """
    Initialize a block object.

    Parameters:
    posx (int): Initial x position.
    posy (int): Initial y position.
    width (int): Width of the block.
    height (int): Height of the block.
    color (tuple): Color of the block.
    points (int): Point value of the block.
    """
    def __init__(self, posx, posy, width, height, color, points):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.health = 1  # Simple health system for demonstration
        self.points = points
        self.block_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        """
        Draw the block on the screen.
        """
        pygame.draw.rect(screen, self.color, self.block_rect)

    def hit(self):
        """
        Handle the block being hit by the ball.
        """
        self.health -= 1

    def get_rect(self):
        """
        Get the rectangle representation of the block.

        Returns:
        pygame.Rect: The block's rectangle.
        """
        return self.block_rect

    def get_health(self):
        """
        Get the health of the block.

        Returns:
        int: The blocks health.
        """
        return self.health

    def get_points(self):
        """
        Get the point value of the block.

        Returns:
        int: The block's point value.
        """
        return self.points

# Class for Ball
class Ball:
    """
    Initialize a Ball object.

    Parameters:
    posx (int): Initial x position.
    posy (int): Initial y position.
    radius (int): Radius of the ball.
    speed (int): Speed of the ball.
    color (tuple): Color of the ball.
    """
    def __init__(self, posx, posy, radius, speed, color, wall_sound=None, lose_life_sound=None):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.wall_sound = wall_sound
        self.lose_life_sound = lose_life_sound
        self.x_fac, self.y_fac = random.uniform(-1, 1), 1
        self.ball_rect = pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)

    def display(self):
        """
        Draw the ball on the screen.
        """
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        """
        Update the ball's position and handle screen edge collisions.
        """
        self.posx += self.x_fac * self.speed
        self.posy += self.y_fac * self.speed

        if self.posx <= 0 or self.posx >= WIDTH:
            self.x_fac *= -1
            if self.posx <= 0:
                self.posx +=2
            elif self.posx>= WIDTH:
                self.posx -=2
            if self.wall_sound:
                self.wall_sound.play()

        if self.posy <= 0:
            self.y_fac *= -1
            if self.wall_sound:
                self.wall_sound.play()

        # Check if ball goes below the screen
        if self.posy >= HEIGHT:
            self.reset()

        self.ball_rect = pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)

    def reset(self):
        """
        Reset the ball's position after losing a life.
        """
        global lives
        lives -= 1
        if lives > 0:
            self.posx = WIDTH // 2
            self.posy = HEIGHT - 150
            self.x_fac, self.y_fac = random.uniform(-1, 1), 1
            if self.lose_life_sound:
                self.lose_life_sound.play()
        else:
            game_over_screen = game_over()
            if game_over_screen:
                initialize_game()  # Reset game elements
            else:
                pygame.quit()
                return

    def hit_paddle(self, paddle_rect):
        """
        Handle the ball hitting the paddle depending on where on the paddle the ball hits.
        """
        if self.posx < paddle_rect.left:
            self.x_fac = -1
        elif self.posx > paddle_rect.right:
            self.x_fac = 1
        else:
            collision_point = self.posx - paddle_rect.left
            relative_collision = (collision_point / paddle_rect.width) - 0.5
            self.x_fac = relative_collision * 2
            self.y_fac = -1

    def hit_block(self, block_rect):
        """
        Handle the ball hitting a block depending on where on the paddle the ball hits.
        """

        if self.posx < block_rect.left:
            self.x_fac = -1
        elif self.posx > block_rect.right:
            self.x_fac = 1
        else:
            self.y_fac *= -1

    def get_rect(self):
        """
        Get the rectanle position of the ball.

        Returns: 
        pygame.Rect: The ball's rectangle
        """
        return self.ball_rect

def main():
    """
    Main game loop.
    """
    global lives, score, paddle, ball, block_list

    start_menu()
    current_level = 1
    initialize_game(current_level)
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/bgmusic.wav')
    pygame.mixer.music.play(-1)  # Play on repeat


    paddle_sound = pygame.mixer.Sound('sounds/paddle.wav')
    brick_sound = pygame.mixer.Sound('sounds/brick.wav')
    wall_sound = pygame.mixer.Sound('sounds/wall.wav')
    lose_life_sound = pygame.mixer.Sound('sounds/lose_life.wav')

    ball = Ball(WIDTH // 2, HEIGHT - 150, 7, 5, WHITE, wall_sound, lose_life_sound)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.set_movement(-1)
                elif event.key == pygame.K_RIGHT:
                    paddle.set_movement(1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and paddle.paddle_x_fac == -1:
                    paddle.set_movement(0)
                elif event.key == pygame.K_RIGHT and paddle.paddle_x_fac == 1:
                    paddle.set_movement(0)

        screen.fill(BLACK)

        # Update and display paddle
        paddle.update()
        paddle.display()

        # Update and display ball
        ball.update()
        ball.display()

        # Check collisions with paddle and blocks
        if collision_checker(paddle.get_rect(), ball.get_rect()):
            #ball.hit()
            ball.hit_paddle(paddle.get_rect())
            paddle_sound.play() 

        for block in block_list:
            if collision_checker(block.get_rect(), ball.get_rect()):
                ball.hit_block(block.get_rect())
                block.hit()
                if block.get_health() <= 0:
                    block_list.remove(block)
                    score += block.get_points()
                    paddle_sound.play() 

        # Display blocks
        for block in block_list:
            block.display()

        # Check if all blocks are destroyed
        if not block_list:
            current_level += 1
            if current_level > 3:
                game_over_screen = game_over()
                if game_over_screen:
                    current_level = 1
                    initialize_game(current_level)
                else:
                    pygame.quit()
                    return
            else:
                initialize_game(current_level)

        # Display lives and score at the bottom of the screen
        lives_text = font.render("Lives: " + str(lives), True, WHITE)
        screen.blit(lives_text, (10, HEIGHT - 20))
        
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (WIDTH - 100, HEIGHT - 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
