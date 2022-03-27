import pygame

class Tile(pygame.sprite.Sprite): # a wall and in general
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift

class Brick(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load('art/brick.png')

class RoyalBlock(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load('art/royal block.png')

class Exit_tile(Tile):
    def __init__(self, pos, size, state=1):
        super().__init__(pos, size)
        self.state = state
        self.change_image()

        # STATES
        # not_triggered = 1
        # triggered = 2
    
    def change_image(self):
        self.image = pygame.image.load('art/exit.png') if self.state == 1 else pygame.image.load('art/exit2.png')

class Exit_trigger_tile(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.image.load('art/exit trigger.png')