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

# Controlling keys
UP = 'W'
DOWN = 'S'
LEFT = 'A'
RIGHT = 'D'

DIRECTION = RIGHT  # Always start the game with a moving right snake
FRUIT_COLOR = (0, 255, 0)
LEVEL_UP = 5  # Must eat 4  (5 - 1 = 4) fruits to go to the next level

# Setting up the GUI
pygame.display.set_caption("Classic Snake 2D")
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
large_font = pygame.font.Font("font.ttf", 35)
small_font = pygame.font.Font("font.ttf", 18)
screen.fill(BACKGROUND_COLOR)

# The snake of the game
snake = Snake(SCREEN_SIZE[0], SCREEN_SIZE[1], Snake.MIN_LENGTH)
# The fruit
fruit = None

# The boolean flag to tell the reason why the snake is dead
eat_self = False
eat_gate = False

# Open/close the gate flag
gate_open = False
# The gate
gate = None

# Stop the game
is_running = True

# Keep track of the number of fruits eaten
# If the number of fruit eaten reaches a certain number
# Reset it to 1 and speed up the game (level up)
food_count = 1

# Contants controlling the speed of the game
time = 70
time_diff = 5
speed_level = 0

def generate_fruit(snake: Snake) -> Block:
    """
    Generate a fruit and make sure it is in a valid position

    Args:
        snake (Snake) : The Snake object, to check if the fruit generated is in valid position

    Returns:
        A valid fruit 
    """
    fruit = create_fruit()
    # Keep creating the fruit until we have a valid position of the fruit
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
    # Randomize the coordinate
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
    block.change_color(BACKGROUND_COLOR)  # Change the color of the block to the background color
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

    # Checks the coordinate of the head against all the other blocks of the body
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

    """
    The ending message will be in the following format:
    GAME OVER
    <A proper message>
    """
    screen.fill(BACKGROUND_COLOR)
    large_text = "GAME OVER"
    small_text = message

    # Get the surfaces of the text
    large_surf = large_font.render(large_text, True, Snake.SNAKE_COLOR)
    small_surf = small_font.render(small_text, True, Snake.SNAKE_COLOR)

    large_rect = large_surf.get_rect()
    small_rect = small_surf.get_rect()

    # Centering the text
    large_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - large_rect.height)
    small_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 10)

    screen.blit(large_surf, large_rect)
    screen.blit(small_surf, small_rect)
    pygame.display.update()
    pygame.time.wait(200)

def create_gate() -> List[Block]:
    """
    Creates a gate and returns the List of Blocks objects that makes the gate
    The gate will comprise of 5 Blocks and will have the shape like this:
    ###
    # #

    Args:
        None

    Returns:
        The List of Blocks representing the gate
    """
    gate_blocks = []
    x = randint(0, SCREEN_SIZE[0] // Snake.SNAKE_BLOCK_SIZE[0] - 3)
    y = randint(0, SCREEN_SIZE[1] // Snake.SNAKE_BLOCK_SIZE[1] - 3)

    first_block_x = x * Snake.SNAKE_BLOCK_SIZE[0]
    first_block_y = y * Snake.SNAKE_BLOCK_SIZE[1]

    first_block = Block(first_block_x, first_block_y, GATE_COLOR, Snake.SNAKE_BLOCK_SIZE)
    gate_blocks.append(first_block)  #  "#"
    """
    #
    #
    """
    gate_blocks.append(Block(first_block_x, first_block_y + Snake.SNAKE_BLOCK_SIZE[0], GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))
    """
    ##
    #
    """
    gate_blocks.append(Block(first_block_x + Snake.SNAKE_BLOCK_SIZE[0], first_block_y, GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))
    """
    ###
    #
    """
    gate_blocks.append(Block(first_block_x + 2 * Snake.SNAKE_BLOCK_SIZE[0], first_block_y, GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))
    """
    ###
    # #
    """
    gate_blocks.append(Block(first_block_x + 2 * Snake.SNAKE_BLOCK_SIZE[0], first_block_y + Snake.SNAKE_BLOCK_SIZE[0], GATE_COLOR, Snake.SNAKE_BLOCK_SIZE))

    return gate_blocks

def draw_gate(gate: List[Block], screen: pygame.Surface) -> List[pygame.Rect]:
    """
    Draw the gate and returns the areas that need to be updated 

    Args:
        gate (List[Block]): The List of Blocks that make the gate
        screen (pygame.Surface): The screen to draw to gate on

    Returns:
        The pygame.Rect objects represent the area that needs to be updated
    """
    update_areas = []
    for block in gate:
        update_rect = draw_block(block, screen)
        update_areas.append(update_rect)

    return update_areas

def passed_gate(snake: Snake, gate: List[Block]) -> bool:
    """
    Checks if the snake has passed the gate

    Args:
        snake (Snake): The snake
        gate (List[Block]): The List of Blocks object representing the gate

    Returns:
        True if the snake has reached the entrance of the gate and False otherwise        
    """

    
    # Since there is only one way to go throught the gate which is throught the front.
    # We only need to check if the snake has reached the front of the gate (marked * in the figure below)
    # ###
    # #*#
    # If the snake has reached to that position, it can definitely pass the gate
    snake_head = snake.get_head()
    first_block = gate[0]

    if snake_head.get_x() == first_block.get_x() + Snake.SNAKE_BLOCK_SIZE[0] and snake_head.get_y() == first_block.get_y() + Snake.SNAKE_BLOCK_SIZE[0]:
        return True
    else:
        return False

def check_gate_collision(snake: Snake, gate: List[Block]) -> bool:
    """
    Check if the snake has collided with the gate but not going in the gate

    Args:
        snake (Snake): The snake
        gate (List[Block]): The List of Blocks object representing the gate

    Returns:
        True if the snake has collided with the gate but has not reached the entrance of the gate
        and False otherwise
    """
    collided = False

    # Check for every block of the gate to see if the snake has stumbled on that block
    snake_x = snake.get_head().get_x()
    snake_y = snake.get_head().get_y()
    for block in gate:
        if block.get_x() == snake_x and block.get_y() == snake_y:
            collided = True

    return collided

def go_throught_gate(snake: Snake, screen: pygame.Surface) -> None:
    """
    Moves throught the gate to get to the next level and update the action on the screen

    Args:
        snake (Snake): The Snake

    Returns:
        The old length of the snake
    """
    # To create the going throught the gate effect, 
    # we simply just delete the tail of the snake and keep everything the same
    update_rects = []
    length = snake.get_length()
    while snake.get_length() > 0:
        # Get the removed tail and delete it from the screen
        old_tail = snake.remove_tail()  
        update_rects = snake.draw(screen)
        update_rects.append(erase_block(old_tail, screen))
        pygame.display.update(update_rects)
        pygame.time.wait(time - speed_level * time_diff)

    return length

def remove_gate(gate: List[Block], screen: pygame.Surface) -> None:
    """
    After the snake has passed the gate, remove it

    Args:
        gate (List[Block]): The gate
        screen (pygame.Surface): The screen to remove the gate from

    Returns:
        None
    """

    update_rects = []
    for block in gate:
        update_rects.append(erase_block(block, screen))

    pygame.display.update(update_rects)


def greeting(screen: pygame.Surface) -> None:
    """
    Display the greeting screen

    Args:
        screen (pygame.Surface): The screen to display the message on

    Returns:
        None
    """
    welcome = small_font.render("Welcome to", True, (0, 255, 0))
    snake = large_font.render("CLASSIC SNAKE", True, Snake.SNAKE_COLOR)
    press = small_font.render("Press any key to start or ESC to quit...", True, (57, 170, 245))

    welcome_rect = welcome.get_rect()
    snake_rect = snake.get_rect()
    press_rect = press.get_rect()

    welcome_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - snake_rect.height - welcome_rect.height * 5)
    snake_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - snake_rect.height)
    press_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + snake_rect.height + press_rect.height * 5)

    screen.blit(welcome, welcome_rect)
    screen.blit(snake, snake_rect)
    screen.blit(press, press_rect)

    pygame.display.update()

    key_pressed = False
    key = None
    while not key_pressed:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key_pressed = True
                key = event.key
            elif event.type == QUIT:
                key = K_ESCAPE
                key_pressed = True

    return key

def play_again(screen: pygame.Surface) -> bool:
    """
    Asks player if they want to play again when the snake is dead

    Args:
        screen (pygame.Surface): the screen to display the message on

    Returns:
        True if the player wants to play again or False otherwise
    """

    text_surf = small_font.render("Press any key to play again or ESC to quit...", True, (0, 255, 0))
    text_rect = text_surf.get_rect()

    text_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - text_rect.height * 10)
    screen.blit(text_surf, text_rect)
    pygame.display.update(text_rect)

    key_pressed = False
    key = None
    while not key_pressed:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key_pressed = True
                key = event.key
            elif event.type == QUIT:
                key = K_ESCAPE
                key_pressed = True

    return key != K_ESCAPE

def reset_game() -> None:
    """
    Resets the game to the initial state

    Args:
        None

    Returns:
        None
    """
    global snake, fruit, eat_self, eat_gate, gate_open, gate, is_running, food_count, time, time_diff, speed_level, DIRECTION
    # The snake of the game
    snake = Snake(SCREEN_SIZE[0], SCREEN_SIZE[1], Snake.MIN_LENGTH)
    # The fruit
    fruit = generate_fruit(snake)

    # The boolean flag to tell the reason why the snake is dead
    eat_self = False
    eat_gate = False

    # Open/close the gate flag
    gate_open = False
    # The gate
    gate = None

    # Stop the game
    is_running = True

    # Keep track of the number of fruits eaten
    # If the number of fruit eaten reaches a certain number
    # Reset it to 1 and speed up the game (level up)
    food_count = 1

    # Contants controlling the speed of the game
    time = 70
    time_diff = 5
    speed_level = 0

    DIRECTION = RIGHT

fruit = generate_fruit(snake)

if __name__ == "__main__":
    key = greeting(screen)

    if key == K_ESCAPE:
        is_running = False

    if is_running:
        screen.fill(BACKGROUND_COLOR)
        pygame.display.update()
        pygame.display.update(snake.draw(screen))

    while is_running:
        # Has the snake eaten itself?
        if check_eat_self(snake):
            is_running = False
            eat_self = True

        # Has the snake stumbled on the wall of the gate
        if gate_open and check_gate_collision(snake, gate):
            is_running = False
            eat_gate = True

        # If the snake is not dead yet
        if is_running:
            update_rects = []
            
            # Capture the key
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

            # Check if eats fruit
            if not gate_open and check_fruit_collision(fruit, snake):
                snake.eat_fruit(DIRECTION, fruit)
                fruit = generate_fruit(snake)
                update_rects += snake.draw(screen)
                food_count += 1

            # Check for level up
            if food_count % LEVEL_UP == 0:
                gate_open = True
                food_count = 1
                gate = create_gate()

            if gate_open:
                # If the snake passed the gate, make it go throught the gate
                # and after going through it, remove the gate and place the snake
                # at a new random position with the same length
                if passed_gate(snake, gate):
                    snake_length = go_throught_gate(snake, screen)
                    remove_gate(gate, screen)
                    gate = None
                    snake = Snake(SCREEN_SIZE[0], SCREEN_SIZE[1], snake_length)
                    speed_level += 1
                    gate_open = False

            pygame.time.wait(time - speed_level * time_diff)
            
            update_rects += move_snake(DIRECTION, snake)

            # When the gate is opening, the snake will have no fruit to eat
            if not gate_open:
                update_rects.append(draw_block(fruit, screen))
            else:
                update_rects += draw_gate(gate, screen)

            pygame.display.update(update_rects)
        else:
            # Ending the game with a proper message base on the reason for the dead of the snake
            if eat_self:
                end_game("You are not delicous!")
            elif eat_gate:
                end_game("Gate is not delicous!")

            # Ask player if they want to play again
            start_again = play_again(screen)
            if start_again:
                # If they want to play again, reset everything to initial state
                is_running = True
                screen.fill(BACKGROUND_COLOR)
                pygame.display.update()
                reset_game()
