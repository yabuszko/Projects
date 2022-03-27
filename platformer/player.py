import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = 6
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16 # x0y0 top left, so -

        self.jumped = False
    
    def get_input(self, allowed):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE]:
            self.jump(allowed) # arg: false if mid-air jumps not allowed
    
    def apply_gravity(self, on=True):
        if on:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def jump(self, can_jump_mid_air=True):
        if not self.jumped and (self.direction.y == 0 or can_jump_mid_air):
            self.direction.y = self.jump_speed
            self.jumped = True
    
    def lift(self, lift_force):
        self.direction.y = -lift_force
    
    def update(self, allowed):
        self.get_input(allowed)