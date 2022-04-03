import pygame

from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, size=16):
        super().__init__()
        self.width = size
        self.max_width = size
        self.shrinking = True

        self.image = pygame.Surface((size, size))
        self.size = size
        self.image.fill('yellow')

        self.rect = self.image.get_rect(topleft=self.calculate_pos(x, y))
    
    def calculate_pos(self, x, y):
        self.x = x
        self.y = y
        return ((tile_size / 2 + x - self.size / 2), (tile_size / 2 + y - self.size / 2))
    
    def animate(self, factor):
        if self.shrinking:
            if self.width == 0:
                self.shrinking = False
            else:
                self.width -= factor
        else:
            if self.width == self.max_width:
                self.shrinking = True
            else:
                self.width += factor
        
        self.image = pygame.transform.scale(self.image, (self.width, self.max_width))
        self.image.fill('yellow')
    
    def update(self, x_shift):
        self.animate(0.5)
        self.rect.x += x_shift