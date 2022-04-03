import pygame
from settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'background.png'))
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(0,0))
        