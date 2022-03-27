import pygame

class Spikes(pygame.sprite.Sprite):
    def update(self, x_shift):
        self.rect.x += x_shift

class SpikesUp(Spikes):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/spikes up.png')
        self.rect = self.image.get_rect(topleft=pos)

class SpikesDown(Spikes):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/spikes down.png')
        self.rect = self.image.get_rect(topleft=pos)

class SpikesLeft(Spikes):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/spikes left.png')
        self.rect = self.image.get_rect(topleft=pos)

class SpikesRight(Spikes):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/spikes right.png')
        self.rect = self.image.get_rect(topleft=pos)