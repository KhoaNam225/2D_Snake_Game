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
GATE_COLOR = (144, 99, 255)
UP = 'W'
DOWN = 'S'
LEFT = 'A'
RIGHT = 'D'

DIRECTION = RIGHT
FRUIT_COLOR = (0, 255, 0)
LEVEL_UP = 5
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
font = pygame.font.Font("font.ttf", 20)
change = 1
block_size = (10, 10)
block = Block(0, 0, (255, 0, 0), block_size)
snake = Snake(SCREEN_SIZE[0], SCREEN_SIZE[1])
time = 70
screen.fill(BACKGROUND_COLOR)
is_running = True
food_count = 1
time_diff = 5
speed_level = 0
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

def check_eat_self(snake: Snake) -> bool:
    """
    Checks if the snake eat itself.

    Args:
        snake: The Snake

    Returns:
        True if the snake has eaten itself or False otherwise
    """
    eaten = False
    head_x = snake.get_head().get_x()
    head_y = snake.get_head().get_y()
    body = snake.get_body()
    curr = 1
    while curr < len(body) and not eaten:
        eaten = head_x == body[curr].get_x() and head_y == body[curr].get_y()
        curr += 1

    return eaten

def end_game(message: str) -> None:
    """
    Display a proper message when the game ends (when the snake is dead)

    Args:
        message (str): The message to be displayed on the screen. Depends on the reason for the 
                        snake to die that the message will differ.

    Returns:
        None
    """
    screen.fill(BACKGROUND_COLOR)
    final_message = "GAME OVER\n" + message
    text_surface = font.render(final_message, True, Snake.SNAKE_COLOR)
    text_size = font.size(final_message)
    screen.blit(text_surface, (SCREEN_SIZE[0] // 2 - text_size[0] // 2, SCREEN_SIZE[1] // 2 - text_size[1] // 2))
    pygame.display.update()
    pygame.time.wait(5000)

def create_gate() -> List[Block]:
    gate_blocks = []
    x = randint(0, SCREEN_SIZE[0] // Snake.SNAKE_BLOCK_SIZE[0] - 3)
    y = randint(0, SCREEN_SIZE[1] // Snake.SNAKE_BLOCK_SIZE[1] - 3)

    first_block_x = x * Snake.SNAKE_BLOCK_SIZE[0]
    first_block_y = y * Snake.SNAKE_BLOCK_SIZE[1]

    first_block = Block(first_block_x, first_block_y, GATE_COLOR, Snake.SNAKE_BLOCK_SIZE)
    gate_blocks.append(first_block)
    gate_blocks.append(Block(first_block_x, first_block_y + Snake.SNAKE_BLOCK_SIZE[0], GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))
    gate_blocks.append(Block(first_block_x + Snake.SNAKE_BLOCK_SIZE[0], first_block_y, GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))
    gate_blocks.append(Block(first_block_x + 2 * Snake.SNAKE_BLOCK_SIZE[0], first_block_y, GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))
    gate_blocks.append(Block(first_block_x + 2 * Snake.SNAKE_BLOCK_SIZE[0], first_block_y + Snake.SNAKE_BLOCK_SIZE[0], GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))

    return gate_blocks

def draw_gate(gate: List[Block], screen: pygame.Surface) -> List[pygame.Rect]:
    update_areas = []
    for block in gate:
        update_rect = draw_block(block, screen)
        update_areas.append(update_rect)

    return update_areas

fruit = generate_fruit(snake)
eat_self = False
gate_open = False
gate = None
while is_running:
    if check_eat_self(snake):
        is_running = False
        eat_self = True

    if is_running:
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
            food_count += 1

        if food_count % LEVEL_UP == 0:
            gate_open = True
            speed_level += 1
            food_count = 1
            gate = create_gate()
            if time < 10:
                time = 10

        pygame.time.wait(time - speed_level * time_diff)
        
        update_rects += move_snake(DIRECTION, snake)
        if not gate_open:
            update_rects.append(draw_block(fruit, screen))
        else:
            update_rects += draw_gate(gate, screen)

        pygame.display.update(update_rects)
    else:
        if eat_self:
            end_game("You ate your self!")