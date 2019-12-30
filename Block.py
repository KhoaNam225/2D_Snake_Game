from typing import *
import pygame

class Block(object):
    """
    This class representing the pixels used to draw all the objects in the game.
    Each pixels will have its coordinate and its color.

    Attributes:
        _x: the x-coordinate
        _y: the y-coordinate
        color: the color of the block (this will vary between different game objects)
        _size: the size of the block
    """

    def __init__(self, x: int, y: int, color: Tuple[int, int ,int], size: Tuple[int, int]):
        """
        Construct a block given its coordinate and color.

        Args:
            x: the x-coordinate
            y: the y-coordinate
            color: the color of the block
            size: the size of the block, given as a tuple of (width, height)
        """
        self._x = x
        self._y = y
        self._color = color
        self._size = size

    def get_x(self) -> int:
        """
        Returns the x-coordinate of the current block

        Args:
            None

        Returns:
            The x-coordinate of the current block
        """
        return self._x

    def get_y(self) -> int:
        """
        Returns the y-coordinate of the current block

        Args:
            None

        Returns:
            The y-coordinate of the current block
        """
        return self._y

    def get_coordinate(self) -> Tuple[int, int]:
        """
        Returns the coordinate of the current block as a tuple of [int, int]

        Args:
            None

        Returns:
            The coordinate of the current block as a tuple
        """

        return (self._x, self._y)

    def get_color(self) -> Tuple[int, int, int]:
        """
        Returns the color of the current block as a RGB tuple

        Args:
            None

        Returns:
            The color of the current block
        """
        return self._color

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the size of the current block as a tuple of (width, height)

        Args:
            None

        Returns:
            The color of the current block
        """

        return self._size

    def change_x(self, pixels_num: int) -> None:
        """
        Move the current block by a number of pixels horizontally

        Args:
            pixels_num (int): The number of pixels that the block needs to move

        Returns:
            None
        """
        self._x += pixels_num

    def change_y(self, pixels_num: int) -> None:
        """
        Move the current block by a number of pixels vertically

        Args:
            pixels_num (int): The number of pixels that the block needs to move

        Returns:
            None
        """
        self._y += pixels_num

    def draw(self) -> pygame.Surface:
        """
        Draw the current block on a surface and return that surface

        Args:
            None

        Returns:
            A new Surface object on which the current block is drawn on
        """

        width = self._size[0]
        height = self._size[1]
        surface = pygame.Surface((width, height), depth=32)
        surface.fill(self._color)

        return surface