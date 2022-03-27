import pygame
import time
from pygame import mixer

from settings import *
from level import *
from tile import *
from player import *
from coin import *
from achievement import *

import data_manager

pygame.init()
pygame.mixer.init()

done = False
_data_manager = data_manager.Data_Manager()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

level = Level(levels[0], screen, _data_manager)

keyup = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        keyup = True if event.type == pygame.KEYUP else False
    
    screen.fill('black')

    level.run(keyup)

    pygame.display.update()
    clock.tick(60)
