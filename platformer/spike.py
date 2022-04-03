import pygame
import time
from settings import *

class Spike(pygame.sprite.Sprite):
    def __init__(self, type, pos, time_arg):
        super().__init__()

        self.type = type
        self.pos_x, self.pos_y = pos
        self.time_counter = time_arg

        self.load_image_and_rect()

        # angry
        self.states = {
            'closed': 0,
            'angry': 1
        }
        self.state = self.states["closed"]

        self.width = 32

        self.angryspikes_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, 'sounds', 'angry spikes.mp3'))
        self.timer = time.time()

    def load_image_and_rect(self):
        if self.type == 'spike_up':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'spikes up.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'spike_down':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'spikes down.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'spike_right':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'spikes right.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'spike_left':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'spikes left.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'angry_spike_up':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'angry spikes up.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'angry_spike_down':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'angry spikes down.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'angry_spike_right':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'angry spikes right.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        elif self.type == 'angry_spike_left':
            self.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'angry spikes left.png'))
            self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))


    def update(self, x_shift):
        if not x_shift == 0:
            self.rect.x += x_shift
            self.pos_x += x_shift
        
        if 'angry' in self.type: # only for angry spikes
            if time.time() - self.timer >= self.time_counter:
                self.rect.x = self.pos_x
                self.rect.y = self.pos_y

                self.state = self.states["closed"] if self.state == self.states["angry"] else self.states["angry"]
                self.timer = time.time()

                if self.pos_x > -64 and self.pos_x < WIDTH:
                    self.angryspikes_sound.play()

                self.resize(2)
    
    def resize(self, factor):
        if self.state == self.states["angry"]:
            self.width = factor * tile_size

            if self.type == 'angry_spike_up':
                self.image = pygame.transform.scale(self.image, (self.rect.width, factor * tile_size))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y - factor * tile_size + 32)) # height - something = 32
            elif self.type == 'angry_spike_down':
                self.image = pygame.transform.scale(self.image, (self.rect.width, factor * tile_size))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
            elif self.type == 'angry_spike_right':
                self.image = pygame.transform.scale(self.image, (factor * tile_size, self.rect.height))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
            else: # left
                self.image = pygame.transform.scale(self.image, (factor * tile_size, self.rect.height))
                self.rect = self.image.get_rect(topleft=(self.pos_x - factor * tile_size + 32, self.pos_y))
        elif self.state == self.states["closed"]:
            self.width = 32

            if self.type == 'angry_spike_up':
                self.image = pygame.transform.scale(self.image, (self.rect.width, 32))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
            elif self.type == 'angry_spike_down':
                self.image = pygame.transform.scale(self.image, (self.rect.width, 32))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
            elif self.type == 'angry_spike_right':
                self.image = pygame.transform.scale(self.image, (32, self.rect.height))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
            else: # left
                self.image = pygame.transform.scale(self.image, (32, self.rect.height))
                self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
