import pygame
from settings import *

class Achievement(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift

class Mid_air_jump_achievement(Achievement):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'mid jump.png'))
        self.rect = self.image.get_rect(topleft=pos)
