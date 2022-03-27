import pygame
import time

from settings import *

class Button(pygame.sprite.Sprite):
    _height = 4

    def __init__(self, pos, width=tile_size, height=4):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=pos)

        self.height = height

        self.pressed = False
    
    def update(self, x_shift):
        self.rect.x += x_shift

        if self.pressed and self.height != 1:
            self.height = 1
            self.image = pygame.transform.scale(self.image, (tile_size, self.height))
            self.timer = time.time()

            self.rect.y += 3 # max height - pressed height
        elif not self.pressed and self.height != 4:
            if time.time() - self.timer >= 0.5:
                self.height = 4
                self.image = pygame.transform.scale(self.image, (tile_size, self.height))
                self.rect.y -= 3 # back to normal position

class Floating_pad(Button):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('art/floating pad.png')