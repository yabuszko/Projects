import pygame
from settings import *

class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'locked door.png'))
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift