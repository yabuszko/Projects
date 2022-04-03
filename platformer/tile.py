import pygame
from settings import *

class Tile(pygame.sprite.Sprite): # a wall and in general
    def __init__(self, type, pos, state='not_triggered', state_block='on'):
        super().__init__()
        self.type = type

        self.position = pos

        # Exit tile
        self.states = {
            'not_triggered': 1,
            'triggered': 2
        }
        self.state = state

        # switch on-off blocks
        self.state_block = state_block

        # switch on-off trigger

        self.load_image_and_rect()
        if self.type == 'exit_tile':
            self.set_image_exit()

        self.rect = self.image.get_rect(topleft=self.position)
        
    def load_image_and_rect(self):
        if self.type == 'brick':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art','brick.png'))
        elif self.type == 'royal_block':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'royal block.png'))
        elif self.type == 'exit_trigger':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'exit trigger.png'))
        elif self.type == 'green_block' and self.state_block == 'on':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'green block.png'))
        elif self.type == 'green_block' and self.state_block == 'off':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'green frame.png'))
        elif self.type == 'red_block' and self.state_block == 'on':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'red block.png'))
        elif self.type == 'red_block' and self.state_block == 'off':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'red frame.png'))
        elif self.type == 'green_trigger':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'green trigger.png'))
        elif self.type == 'red_trigger':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'red trigger.png'))
                

    # exit
    def set_image_exit(self):
        self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 
        'exit.png')) if self.state == 'not_triggered' else pygame.image.load(os.path.join(ROOT_DIR, 'art', 'exit2.png'))

    def update(self, x_shift):
        self.rect.x += x_shift

    # on-off
    def switch(self, colour):
        if self.state_block == 'on':
            self.image = pygame.image.load(
                os.path.join(ROOT_DIR, 'art', f'{colour} frame.png'))
            self.state_block = 'off'
        else:
            self.image = pygame.image.load(
                os.path.join(ROOT_DIR, 'art', f'{colour} block.png'))
            self.state_block = 'on'