import pygame
from settings import *

class Turtle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'cart.png'))

        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 1

        self.dirs = {
            'right': 1,
            'left': 2
        }
        self.dir = self.dirs['left']
    
    def update(self, x_shift):
        self.rect.x += x_shift

        if self.dir == self.dirs['right']:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed