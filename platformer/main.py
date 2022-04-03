import pygame

from settings import *
from level import *
from tile import *
from player import *
from coin import *
from achievement import *
#print(ROOT_DIR)
import data_manager
pygame.init()
pygame.mixer.init()

_data_manager = data_manager.Data_Manager()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

level = Level(screen, _data_manager)

keyup = None
mousedown = None

while not level.done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                level.run_menu()
        keyup = True if event.type == pygame.KEYUP else False
        mousedown = True if event.type == pygame.MOUSEBUTTONDOWN else False
    
    screen.fill('black')

    level.run(keyup, mousedown)

    pygame.display.update()
    clock.tick(60)
