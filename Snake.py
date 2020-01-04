from Block import Block
from random import randint
from typing import *
import pygame

class Snake(object):
    """
    The Snake in the game. The snake will consist of a number of blocks

    Constants:
        MIN_LENGTH = 5: The minimum length of the snake
        MAX_LENGTH = 15: The maximum lenght of the snake, if the snake get over this length
                        the game will jump to the next level and the length will come back to minimum
        BLOCK_SNAKE_SIZE = (20, 20): The size of each block making the body of the Snake
        SNAKE_COLOR = (255, 0, 0): The color of the Snake (Red)

    Attributes:
        length (int): The current length of the snake
        body (List[Block]): The body of the snake, which contains several Blocks object
        dead (bool): Is the Snake dead or alive
    """
    MIN_LENGTH = 5
    MAX_LENGTH = 15
    SNAKE_BLOCK_SIZE = (20, 20)
    SNAKE_COLOR = (255, 0, 0)
    SCREEN_SIZE = (1000, 700)

    def __init__(self, board_width, board_height):
        """
        Create a snake with the minimum length and at random position in the board.

        Attributes:
            board_width (int): The width of the window
            board_height (int): The height of the window
        """
        x = randint(Snake.MIN_LENGTH + 1, Snake.SCREEN_SIZE[0] // Snake.SNAKE_BLOCK_SIZE[0] - 1)
        y = randint(1, Snake.SCREEN_SIZE[1] // Snake.SNAKE_BLOCK_SIZE[0] - 1)
        head_x = Snake.SNAKE_BLOCK_SIZE[0] * x
        head_y = Snake.SNAKE_BLOCK_SIZE[0] * y
        self._length = Snake.MIN_LENGTH
        self._dead = False
        self._body = []
        self._body.append(Block(head_x, head_y, Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE))
        for i in range(1, 5):
            block = Block(head_x - i * Snake.SNAKE_BLOCK_SIZE[0], head_y, Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)
            self._body.append(block)

    def get_body(self) -> List[Tuple[int, int]]:
        """
        Return the body of the Snake, which is a List of Block objects

        Args:
            None

        Returns:
            The list containing all the blocks making the Snake 
        """
        return self._body

    def get_length(self) -> int:
        """
        Returns the current length of the Snake

        Args:
            None

        Returns:   
            The current length of the Snake
        """
        return self._length

    def get_head(self) -> Block:
        """
        Returns the Block representing the head of the Snake
        """

        return self._body[0]

    def is_dead(self) -> bool:
        """
        Is the Snake dead or alive?
        """
        return self._dead

    def move_left(self) -> None:
        """
        Turns the current direction of the Snake to the left and returns the old tail

        Args:
            None

        Returns:
            The block representing the old tail of the snake. This block will be erase when the 
            snake moves
        """
        # Move all the blocks except for the head forward
        head_x = self._body[0].get_x()
        head_y = self._body[0].get_y()

        tail = self._body[self._length - 1]  # Get the old tail
        
        for i in range(self._length - 1, 0, -1):
            self._body[i] = self._body[i - 1]

        self._body[0] = Block(head_x - Snake.SNAKE_BLOCK_SIZE[0], head_y, Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)

        return tail
    
    def move_right(self) -> None:
        """
        Turn the current direction of the Snake to the right and returns the old tail

        Args:
            None

        Returns:
            The block representing the old tail of the snake. This block will be erase when the 
            snake moves
        """
        head_x = self._body[0].get_x()
        head_y = self._body[0].get_y()

        tail = self._body[self._length - 1]  # Get the old tail

        # Move all the blocks except for the head forward
        for i in range(self._length - 1, 0, -1):
            self._body[i] = self._body[i - 1]

        self._body[0] = Block(head_x + Snake.SNAKE_BLOCK_SIZE[0], head_y, Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)

        return tail

    def move_up(self) -> None:
        """
        Turn the current direction of the Snake to go up and return the old tail

        Args:
            None

        Returns:
            The block representing the old tail of the snake. This block will be erase when the 
            snake moves
        """
        head_x = self._body[0].get_x()
        head_y = self._body[0].get_y()

        tail = self._body[self._length - 1] # Get the old tail

        # Move all the blocks except for the head forward
        for i in range(self._length - 1, 0, -1):
            self._body[i] = self._body[i - 1]

        self._body[0] = Block(head_x, head_y - Snake.SNAKE_BLOCK_SIZE[1], Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)

        return tail

    def move_down(self) -> None:
        """
        Turn the current direction of the Snake to go down

        Args:
            None

        Returns:
            The block representing the old tail of the snake. This block will be erase when the 
            snake moves
        """
        head_x = self._body[0].get_x()
        head_y = self._body[0].get_y()

        tail = self._body[self._length - 1] # Get the old tail

        # Move all the blocks except for the head forward
        for i in range(self._length - 1, 0, -1):
            self._body[i] = self._body[i - 1]

        self._body[0] = Block(head_x, head_y + Snake.SNAKE_BLOCK_SIZE[1], Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)

        return tail

    def die(self) -> None:
        """
        Makes the current Snake die

        Args:
            None

        Returns:
            None
        """
        self._dead = True


    def teleport(self, new_coordinate: Tuple[int, int]) -> None:
        """
        Teleport the snake to the given position (used when the snake go to the edge of the screen)

        Args:
            new_coordinate (Tuple[int, int]): The new coordinate of the snake

        Returns:
            None
        """
        self._body[0].set_x(new_coordinate[0])
        self._body[0].set_y(new_coordinate[1])

    def eat_fruit(self, direction: str, fruit: Block) -> None:
        """
        Eat the fruit and increase the size of the snake

        Args:
            direction (str): The direction the snake is moving in 
            fruit (Block): The fruit

        Returns:
            None
        """
        new_block = None
        if direction == 'W':
            new_block = Block(fruit.get_x(), fruit.get_y() - Snake.SNAKE_BLOCK_SIZE[0], Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)
        elif direction == 'S':
            new_block = Block(fruit.get_x(), fruit.get_y() + Snake.SNAKE_BLOCK_SIZE[0], Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)
        elif direction == 'A':
            new_block = Block(fruit.get_x() - Snake.SNAKE_BLOCK_SIZE[0], fruit.get_y(), Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)
        elif direction == 'D':
            new_block =  Block(fruit.get_x() + Snake.SNAKE_BLOCK_SIZE[0], fruit.get_y(), Snake.SNAKE_COLOR, Snake.SNAKE_BLOCK_SIZE)

        self._body = [new_block] + self._body
        self._length += 1


    def draw(self, screen: pygame.Surface) -> List[pygame.Rect]:
        """
        Draw the whole Snake on the screen and returns the updated areas (for updating purpose)

        Args:
            The screen the the snake will be drawn on

        Returns:
            The List of pygame.Rect objects where the snake is drawn
        """
        rect = []
        for block in self._body:
            surface = block.draw()
            screen.blit(surface, block.get_coordinate())
            rect.append(pygame.Rect(block.get_coordinate(), Snake.SNAKE_BLOCK_SIZE))

        return rect
