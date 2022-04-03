import pygame
from settings import *

class Level_tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, lvl):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ROOT_DIR,'art', 'levels', f'lvl{lvl}.png'))
        self.image = pygame.transform.scale(self.image, size) # 100, 58  prop 12:7
        self.rect = self.image.get_rect(topleft=pos)

        self.unlocked = True
        self.hovered = False

        self.level = lvl
    
    def update(self):
        # checking if hovered
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
    
    def click_check(self, mousedown):
        return self.hovered and mousedown
