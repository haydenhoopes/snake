import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('Helvetica.ttf', 25)
food_sound = pygame.mixer.Sound('./sounds/mixkit-arcade-game-jump-coin-216.wav')

# reset
# reward
# play(action) => direction
# frame/game iteration
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", "x, y")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20

class Snake:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # step 1 - get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction is not Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction is not Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_DOWN and self.direction is not Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_UP and self.direction is not Direction.DOWN:
                    self.direction = Direction.UP
                

        # step 2 - move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # step 3 - check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # step 4 - place new food or just move
        if self.head == self.food:
            pygame.mixer.Sound.play(food_sound)
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # step 5 - update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # step 6 - return game over and score
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x+4, point.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f"Score: {str(self.score)}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        elif self.head in self.snake[1:]:
            return True
        else:
            return False


if __name__ == '__main__':
    game = Snake()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print(f'Your final score was {score}')
    pygame.quit()