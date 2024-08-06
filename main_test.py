import unittest
import pygame
from pygame.locals import KEYDOWN, QUIT, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE
from unittest.mock import patch, MagicMock
from main import Ball, Paddle, Block, collision_checker, initialize_game, main, game_over


# Define the color constants used in the game
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class TestBreakoutGame(unittest.TestCase):
    """Unit test case forthe Breakout game implementation."""

    def setUp(self):
        """Initialize Pygame and create objects for testing."""
        pygame.init()
        self.screen = pygame.display.set_mode((600, 500))
        # Now including speed and color when initializing Paddle
        self.paddle = Paddle(275, 490, 100, 20, 10, WHITE)  # Speed and color added
        self.ball = Ball(300, 250, 7, 5, WHITE)
        self.blocks = [Block(i * 100, 30, 80, 30, RED, 5) for i in range(5)]
        initialize_game()

    @patch('pygame.event.get')
    def test_ball_movement(self, mock_get):
        """Test that the ball moves correctly."""
        mock_get.return_value = []  # No user input
        initial_x = self.ball.posx
        initial_y = self.ball.posy
        self.ball.update()
        self.assertNotEqual((initial_x, initial_y), (self.ball.posx, self.ball.posy))

    def test_collision_detection_true(self):
        """Test collision between ball and paddle."""
        rect1 = pygame.Rect(100, 100, 50, 50)
        rect2 = pygame.Rect(120, 120, 50, 50)  # Overlapping rect1
        self.assertTrue(collision_checker(rect1, rect2))

    def test_collision_detection_false(self):
        """Test collision detection between non-overlapping rectangles."""
        rect1 = pygame.Rect(100, 100, 50, 50)
        rect2 = pygame.Rect(200, 200, 50, 50)  # Not overlapping rect1
        self.assertFalse(collision_checker(rect1, rect2))

    def test_paddle_movement(self):
        """Test that the paddle moves correctly in response to left and right key presses."""
        initial_posx = self.paddle.posx

        # Simulate left movement
        self.paddle.set_movement(-1)
        self.paddle.update()
        self.assertTrue(self.paddle.posx < initial_posx, "Paddle should move left")

        # Reset position and simulate right movement
        self.paddle.posx = initial_posx  # Reset position
        self.paddle.set_movement(1)
        self.paddle.update()
        self.assertTrue(self.paddle.posx > initial_posx, "Paddle should move right")

        # Reset movement to neutral
        self.paddle.set_movement(0)

    @patch('pygame.event.get')
    def test_game_over_display(self, mock_get):
        """Test if game over screen is displayed correctly."""
        # Mock run of the game
        mock_event = MagicMock()
        mock_event.type = KEYDOWN
        mock_event.key = K_SPACE
        mock_get.return_value = [mock_event]

        # Run game_over and capture return value and assert True
        # to restart game
        result = game_over()
        self.assertTrue(result)

    @patch('pygame.event.get')
    def test_game_over_quit(self, mock_get):
        """Test if game over screen quits the game correctly."""
        # Mock run of the game
        mock_event = MagicMock()
        mock_event.type = KEYDOWN
        mock_event.key = K_ESCAPE
        mock_get.return_value = [mock_event]

        # Run game_over and capture return value and assert False
        #to quit game
        result = game_over()
        self.assertFalse(result)

    @patch('pygame.event.get')
    def test_game_over_close(self, mock_get):
        """Test if closing the game over screen quits the game correctly."""
        # Mock run of the game
        mock_event = MagicMock()
        mock_event.type = QUIT # Change ()= pygame.QUIT) to ()= QUIT)
        mock_get.return_value = [mock_event] # was (pygame.event.get = MagicMock(return_value=[mock_event]))

        # Run game_over and capture return value and assert False
        #to quit game
        result = game_over()
        self.assertFalse(result)

    # where it says Team_Beta_Phase_1, user needs to substitute with their file name for the game
    @patch('Team_Beta_Phase_1.lives', 3)
    def test_ball_reset(self):
        """Test if the ball resets correctly after losing a life."""
        # where it says Team_Beta_Phase_1, user needs to substitute with their file name for the game
        from main import lives
        self.ball.reset()
        self.assertEqual(lives, 3)

    # where it says Team_Beta_Phase_1, user needs to substitute with their file name for the game
    @patch.dict('Team_Beta_Phase_1.__dict__', {'score': 0, 'block_list': []})
    def test_scoring(self):
        """Test if the scoring is updated correctly when the ball hits a block."""
        # where it says Team_Beta_Phase_1, user needs to substitute with their file name for the game
        from main import score, block_list
        block = Block(100, 100, 40, 15, RED, 10)
        block_list.append(block)
        initial_score = score

        #simulate ball hitting the block
        self.ball.posx, self.ball.posy = block.posx + 20, block.posy + 10
        self.ball.update()
        if collision_checker(block.get_rect(), self.ball.get_rect()):
            block.hit()
            if block.get_health() <= 0:
                block_list.remove(block)
                score += block.get_points()
        
        self.assertEqual(score, initial_score + block.get_points())
   
    def tearDown(self):
        """Quit Pygame."""
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
