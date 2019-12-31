import pygame
from pygame.locals import *
from sys import exit
from Block import Block
from Snake import Snake
from typing import List, Tuple

pygame.init()

SCREEN_SIZE = (1024, 768)
BACKGROUND_COLOR = (0, 0, 0)
UP = 'W'
DOWN = 'S'
LEFT = 'A'
RIGHT = 'D'

DIRECTION = RIGHT

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
change = 1
block_size = (10, 10)
block = Block(0, 0, (255, 0, 0), block_size)
snake = Snake(SCREEN_SIZE[0], SCREEN_SIZE[1])
time = 70
screen.fill(BACKGROUND_COLOR)
is_running = True
pygame.display.update(snake.draw(screen))

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
    if head_x <= 0:
        snake.teleport((SCREEN_SIZE[0] - Snake.SNAKE_BLOCK_SIZE[0], head_y))
    # The right edge
    elif head_x >= SCREEN_SIZE[0]:
        snake.teleport((0, head_y))
    # The upper edge
    elif head_y <= 0:
        snake.teleport((head_x, SCREEN_SIZE[1] - Snake.SNAKE_BLOCK_SIZE[0]))
    # The lower edge
    elif head_y >= SCREEN_SIZE[1]:
        snake.teleport((head_x, 0))

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

    pygame.time.wait(time)
    
    update_rects = move_snake(DIRECTION, snake)
    
    pygame.display.update(update_rects)