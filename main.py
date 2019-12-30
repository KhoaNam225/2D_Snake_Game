import pygame
from pygame.locals import *
from sys import exit
from Block import Block

pygame.init()

SCREEN_SIZE = (1024, 768)
BACKGROUND_COLOR = (0, 0, 0)

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
x = 0
y = 0
change = 1
block_size = (10, 10)
block = Block(0, 0, (255, 0, 0), block_size)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
            
    screen.fill(BACKGROUND_COLOR)


    pygame.time.wait(1)
    
    screen.blit(block.draw(), block.get_coordinate())

    block.change_x(5 * change)
    if block.get_x() >= SCREEN_SIZE[0] or block.get_x() <= 0:
        change = -1 * change
    
    pygame.display.update()