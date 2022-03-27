import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/menu1.png')
        self.rect = self.image.get_rect(topleft=pos)
