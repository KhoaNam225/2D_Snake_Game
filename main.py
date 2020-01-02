import pygame
from pygame.locals import *
from sys import exit
from Block import Block
from Snake import Snake
from typing import List, Tuple
from random import randint

pygame.init()

SCREEN_SIZE = (1000, 700)
BACKGROUND_COLOR = (0, 0, 0)
UP = 'W'
DOWN = 'S'
LEFT = 'A'
RIGHT = 'D'

DIRECTION = RIGHT
FRUIT_COLOR = (0, 255, 0)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
change = 1
block_size = (10, 10)
block = Block(0, 0, (255, 0, 0), block_size)
snake = Snake(SCREEN_SIZE[0], SCREEN_SIZE[1])
time = 70
screen.fill(BACKGROUND_COLOR)
is_running = True
pygame.display.update(snake.draw(screen))

def generate_fruit(snake: Snake) -> Block:
    """
    Generate a fruit and make sure it is in a valid position

    Args:
        snake (Snake) : The Snake object, to check if the fruit generated is in valid position

    Returns:
        A valid fruit 
    """
    fruit = create_fruit()
    while not is_valid(fruit, snake):
        fruit = create_fruit()

    return fruit

def create_fruit() -> Block:
    """
    Create a fruit at random position on the screen

    Args:
        None

    Returns:
        A Block object representing the fruit
    """
    x = randint(1, SCREEN_SIZE[0] // Snake.SNAKE_BLOCK_SIZE[0] - 1)
    y = randint(1, SCREEN_SIZE[1] // Snake.SNAKE_BLOCK_SIZE[0] - 1)
    fruit_x = x * Snake.SNAKE_BLOCK_SIZE[0]
    fruit_y = y * Snake.SNAKE_BLOCK_SIZE[0]

    return Block(fruit_x, fruit_y, FRUIT_COLOR, Snake.SNAKE_BLOCK_SIZE)

def is_valid(fruit: Block, snake: Snake) -> Block:
    """
    Check if the fruit is in a valid coordinate.
    The coordinate is valid if it does not lie on the body of the snake

    Args:
        fruit (Block): The fruit
        snake (Snake): The snake

    Returns:
        True if the fruit is in valid position or False otherwise
    """
    for block in snake.get_body():
        if fruit.get_x() == block.get_x() and fruit.get_y() == block.get_y():
            return False

    return True

def check_fruit_collision(fruit: Block, snake: Snake) -> bool:
    """
    Checks if the snake has collided with the fruit

    Args:
        fruit (Block): The fruit
        snake (Snake): The Snake

    Returns:
        True if the snake collides with the fruit or False otherwise
    """
    return fruit.get_x() == snake.get_head().get_x() and fruit.get_y() == snake.get_head().get_y()

def erase_block(block: Block, screen: pygame.Surface) -> None:
    """
    Erase the block from the screen and return the Rect object where that block is located (for updating purpose)

    Args:
        block (Block): The block that needs to be erased
        screen: The screen of the game

    Returns:
        The pygame.Rect object where the Block is located
    """
    block.change_color(BACKGROUND_COLOR)
    screen.blit(block.draw(), block.get_coordinate())
    return pygame.Rect(block.get_coordinate(), block.get_size())

def draw_block(block: Block, screen: pygame.Surface) -> None:
    """
    Draw a block on the screen and returns the pygame.Rect object where that block is located (for updating purpose)

    Args:
        block (Block): The block that needs to be drawn

    Returns:
        The pygame.Rect object where the Block is located
    """
    screen.blit(block.draw(), block.get_coordinate())
    return pygame.Rect(block.get_coordinate(), block.get_size())

def move_snake(direction: str, snake: Snake) -> List[pygame.Rect]:
    """
    Move the snake along the given direction and returns a List of pygame.Rect objects
    for updating the screen when the snake has moved.

    Args:
        direction (str): The direction of the snake (UP | DOWN | LEFT | RIGHT)
        snake (Snake): The Snake object

    Returns:
        The List of pyagme.Rect objects for updating the screen purpose
    """
    # When the snake is moving, only its head and tail are changed in terms of displaying on the screen
    # The head and tail will move one step forward
    # Therefore when the snake is moving, we only need to update the first and the last block on the screen
    # A new block will be added and the old_tail will be deleted

    # The new block represent the new head 
    new_block = None 
    # The old tail to be removed
    erased_block = None
    old_tail = None

    # Move the snake along the direction
    if DIRECTION == RIGHT:
        old_tail = snake.move_right()    
    elif DIRECTION == LEFT:
        old_tail = snake.move_left()
    elif DIRECTION == UP:
        old_tail = snake.move_up()
    else:
        old_tail = snake.move_down()

    # Teleport if collides with any edges
    check_edge_collision(snake)

    new_block = draw_block(snake.get_head(), screen)
    erased_block = erase_block(old_tail, screen)
    return [erased_block, new_block]  # The updated areas

def check_edge_collision(snake: Snake) -> None:
    """
    Checks if the snake collides with any edges of the screen.
    If it does, teleport it to the opposite edge.

    Args:
        snake (Snake): The Snake object

    Returns:
        None
    """
    head_x = snake.get_head().get_x()
    head_y = snake.get_head().get_y()

    # The left edge
    if head_x < 0:
        snake.teleport((SCREEN_SIZE[0] - Snake.SNAKE_BLOCK_SIZE[0], head_y))
    # The right edge
    elif head_x >= SCREEN_SIZE[0]:
        snake.teleport((0, head_y))
    # The upper edge
    elif head_y < 0:
        snake.teleport((head_x, SCREEN_SIZE[1] - Snake.SNAKE_BLOCK_SIZE[0]))
    # The lower edge
    elif head_y >= SCREEN_SIZE[1]:
        snake.teleport((head_x, 0))

fruit = generate_fruit(snake)
while is_running:
    update_rects = []
    
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        elif event.type == KEYDOWN:
            if event.key == K_w and DIRECTION != DOWN:
                DIRECTION = UP
            elif event.key == K_s and DIRECTION != UP:
                DIRECTION = DOWN
            elif event.key == K_d and DIRECTION != LEFT:
                DIRECTION = RIGHT
            elif event.key == K_a and DIRECTION != RIGHT:
                DIRECTION = LEFT

    
    if check_fruit_collision(fruit, snake):
        snake.eat_fruit(DIRECTION, fruit)
        fruit = generate_fruit(snake)
        update_rects += snake.draw(screen)

    pygame.time.wait(time)
    
    update_rects += move_snake(DIRECTION, snake)
    update_rects.append(draw_block(fruit, screen))
    
    pygame.display.update(update_rects)