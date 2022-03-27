from select import select
from telnetlib import theNULL
import pygame
import time

from pygame import mixer
from settings import *
import data_manager

pygame.init()
pygame.mixer.init()

done = False
_data_manager = data_manager.Data_Manager()

MUSIC_VOLUME = 0.5
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

class Level:
    def __init__(self, level_data, surface, data_man):
        self.display_surface = surface
        self.data_man = data_man

        self.lvl_data = level_data

        self.world_shift = 0
        self.points = 0
        self.curr_lvl = 0
        self.levitate = False

        self.levels_with_exit_triggered = [0]
        self.mid_air_jumps_allowed = False

        self.font = pygame.font.Font('others/tahoma.ttf', 32)
        
        self.coin_collect_sound = mixer.Sound('sounds/coin sound.wav')
        self.button_press_sound = mixer.Sound('sounds/button.mp3')
        self.achievement_sound = mixer.Sound('sounds/achievement.mp3')

        self.setup_level(self.lvl_data, 2, True) # TODO: change after saving

        mixer.music.load("sounds/music1.mp3")
        mixer.music.set_volume(MUSIC_VOLUME)
        mixer.music.play(-1)

    def setup_level(self, layout, state, player_spawn_higher=False, height=100):
        # saving data
        self.data_man.save_data(self.curr_lvl, self.points)

        # basic setup
        self.menu = pygame.sprite.GroupSingle()
        self.menu.add(Menu((WIDTH / 2 - 114, HEIGHT / 2 - 100))) # size 228x200 px

        self.menu_dot = pygame.sprite.GroupSingle()
        self.menu_dot.add(MenuDot((WIDTH / 2 - 150, HEIGHT / 2 - 100)))

        self.bricks = pygame.sprite.Group()
        self.royalblocks = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.floating_pads = pygame.sprite.Group()

        self.spikesUp = pygame.sprite.Group()
        self.spikesDown = pygame.sprite.Group()
        self.spikesRight = pygame.sprite.Group()
        self.spikesLeft = pygame.sprite.Group()

        self.player = pygame.sprite.GroupSingle() 
        self.exit = pygame.sprite.GroupSingle()
        self.exit_trigger = pygame.sprite.GroupSingle()

        self.achievement1 = pygame.sprite.GroupSingle()

        #self.points = 0

        # loading level
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X': # block
                    brick = Brick((x, y), tile_size)
                    self.bricks.add(brick)
                elif cell == 'C': # coin
                    coin = Coin(x, y)
                    self.coins.add(coin)
                elif cell == 'P': # player
                    player_sprite = Player((x, y)) if not player_spawn_higher else Player((x, y - height))
                    self.player.add(player_sprite)
                elif cell == 'E': # exit
                    exit_tile = Exit_tile((x, y), tile_size, state)
                    self.exit.add(exit_tile)
                elif cell == 'T': # exit trigger
                    exit_trigger_tile = Exit_trigger_tile((x, y), tile_size)
                    self.exit_trigger.add(exit_trigger_tile)
                elif cell == 'F': # floating pad
                    floating_pad = Floating_pad((x, y + tile_size - Floating_pad._height))
                    self.floating_pads.add(floating_pad)
                elif cell == 'R': # royal block
                    royalblock = RoyalBlock((x, y), tile_size)
                    self.royalblocks.add(royalblock)
                elif cell == '1': # Spike up
                    spike = SpikesUp((x, y + tile_size - 32))
                    self.spikesUp.add(spike)
                elif cell == '2': # Spike down
                    spike = SpikesDown((x, y))
                    self.spikesDown.add(spike)
                elif cell == '3': # Spike right
                    spike = SpikesRight((x, y))
                    self.spikesRight.add(spike)
                elif cell == '4': # spike left
                    spike = SpikesLeft((x + 32, y))
                    self.spikesLeft.add(spike)
                elif cell == '!': # mid air achievement
                    achv = Mid_air_jump_achievement((x + 16, y + 16), 16)
                    self.achievement1.add(achv)
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -6
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 6
    
    def coin_collision(self):
        player = self.player.sprite

        for coin in self.coins.sprites():
            if coin.rect.colliderect(player.rect): #if player hits a coin
                self.coin_collect_sound.play()

                self.coins.remove(coin)
                self.points += 1
    
    def achievement_collision(self):
        if self.achievement1:
            player = self.player.sprite
            midairjumpachievement = self.achievement1.sprite

            if player.rect.colliderect(midairjumpachievement.rect):
                self.achievement_sound.play()
                self.achievement1.remove(self.achievement1.sprite)
                self.mid_air_jumps_allowed = True

    
    def floating_pad_collision(self):
        player = self.player.sprite

        for pad in self.floating_pads.sprites():
            if pad.rect.colliderect(player.rect):
                if not pad.pressed:
                    self.button_press_sound.play()
                    self.levitate = True
                    self.timer = time.time()

                pad.pressed = True
            else:
                pad.pressed = False

    def exit_trigger_collision(self):
        if self.exit_trigger: # crash protection
            player = self.player.sprite
            exit_trigger_tile = self.exit_trigger.sprite

            if exit_trigger_tile.rect.colliderect(player.rect):
                self.exit.sprite.state = 2
                self.unlock_exit()
    
    def exit_collision(self):
        if self.exit:
            player = self.player.sprite
            exit_tile = self.exit.sprite

            if exit_tile.rect.colliderect(player.rect) and exit_tile.state == 2:
                if len(levels) >= self.curr_lvl + 2: # check if out of range
                    self.curr_lvl += 1
                    self.setup_level(levels[self.curr_lvl], 1, True) # TODO: change after saving

                    self.lvl_data = levels[self.curr_lvl]
    
    def spike_collision(self):
        player = self.player.sprite

        for spikeu in self.spikesUp.sprites():
            if spikeu.rect.colliderect(player.rect):
                self.death()
                #return
        for spiked in self.spikesDown.sprites():
            if spiked.rect.colliderect(player.rect):
                self.death()
                #return
        for spiker in self.spikesRight.sprites():
            if spiker.rect.colliderect(player.rect):
                self.death()
                #return
        for spikel in self.spikesLeft.sprites():
            if spikel.rect.colliderect(player.rect):
                self.death()
                #return

    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for tile in self.bricks.sprites():
            if tile.rect.colliderect(player.rect): # then flip
                if player.direction.x < 0: # moving left
                    player.rect.left = tile.rect.right
                elif player.direction.x > 0: # moving right
                    player.rect.right = tile.rect.left
        
        for royalblock in self.royalblocks.sprites():
            if royalblock.rect.colliderect(player.rect): # then flip
                if player.direction.x < 0: # moving left
                    player.rect.left = royalblock.rect.right
                elif player.direction.x > 0: # moving right
                    player.rect.right = royalblock.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity(not self.levitate)

        for tile in self.bricks.sprites():
            if tile.rect.colliderect(player.rect): # then flip
                if player.direction.y > 0: # moving/falling down
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0 # glitch protection

                    player.jumped = False # on the ground, allow for jumping
                elif player.direction.y < 0 or self.levitate: # moving up
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0 # hit a block from below = bounce down
            
        for royalblock in self.royalblocks.sprites():
            if royalblock.rect.colliderect(player.rect): # then flip
                if player.direction.y > 0: # moving/falling down
                    player.rect.bottom = royalblock.rect.top
                    player.direction.y = 0 # glitch protection

                    player.jumped = False # on the ground, allow for jumping
                elif player.direction.y < 0 or self.levitate: # moving up
                    player.rect.top = royalblock.rect.bottom
                    player.direction.y = 0 # hit a block from below = bounce down
        
        # if fell down
        if player.direction.y > 0 and player.rect.bottom > HEIGHT:
            self.death()
    
    def death(self):
        self.world_shift = 0
        self.points = 0

        if self.curr_lvl in self.levels_with_exit_triggered:
            self.setup_level(self.lvl_data, 2, True) # false if spawn without fall
        else:
            self.setup_level(self.lvl_data, 1, True) # false if spawn without fall

    def show_text(self, pos, what_to_render):
        self.display_surface.blit(what_to_render, pos)
    
    def unlock_exit(self):
        self.exit_trigger.sprite.image = pygame.image.load("art/exit trigger2.png")
        self.exit.sprite.image = pygame.image.load("art/exit2.png")

    def run(self, keyup_):
        if self.levitate:
            if time.time() - self.timer >= 2:
                self.levitate = False
            else:
                self.player.sprite.jumped = True # disable jumping
                self.player.sprite.lift(2)

        self.scroll_x()

        # menu
        if self.menu_dot.sprite.state_menu:
            if keyup_:
                self.menu_dot.sprite.moved = False
            self.menu_dot.update()

            self.menu.draw(self.display_surface)
            self.menu_dot.draw(self.display_surface)

        if not self.menu_dot.sprite.state_menu:
            # tiles
            self.bricks.update(self.world_shift)
            self.royalblocks.update(self.world_shift)

            self.exit.update(self.world_shift)
            self.exit_trigger.update(self.world_shift)

            #spikes
            self.spikesUp.update(self.world_shift)
            self.spikesDown.update(self.world_shift)
            self.spikesRight.update(self.world_shift)
            self.spikesLeft.update(self.world_shift)

            # buttons
            self.floating_pads.update(self.world_shift)

            # coins
            self.coins.update(self.world_shift)

            # achievements
            self.achievement1.update(self.world_shift)

            # player
            self.player.update(self.mid_air_jumps_allowed)
            self.exit_trigger_collision()
            self.exit_collision()
            self.coin_collision()
            self.spike_collision()
            self.floating_pad_collision()
            self.achievement_collision()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()

            ###### drawing ######
            self.bricks.draw(self.display_surface)
            self.royalblocks.draw(self.display_surface)

            self.exit.draw(self.display_surface)
            self.exit_trigger.draw(self.display_surface)

            self.spikesUp.draw(self.display_surface)
            self.spikesDown.draw(self.display_surface)
            self.spikesRight.draw(self.display_surface)
            self.spikesLeft.draw(self.display_surface)

            self.floating_pads.draw(self.display_surface)

            self.coins.draw(self.display_surface)

            self.achievement1.draw(self.display_surface)

            self.player.draw(self.display_surface)

            # text
            level_txt = self.font.render("Poziom: " + str(self.curr_lvl + 1), True, 'green')
            self.show_text((0, 0), level_txt)

            score = self.font.render("Punkty: " + str(self.points), True, 'white')
            self.show_text((0, level_txt.get_rect().bottom + 5), score)

class Menu(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/menu1.png')
        self.rect = self.image.get_rect(topleft=pos)

class MenuDot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('art/menu dot.png')
        self.rect = self.image.get_rect(topleft=pos)

        self.selected_option = 0
        self.moved = False

        self.state_menu = True # false - game, true - in menu
    
    def get_input(self):
        global done
        keys = pygame.key.get_pressed()

        if not self.moved:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.moved = True
                if self.selected_option == 2:
                    self.selected_option = 0
                    self.rect.y = HEIGHT / 2 - 100
                else:
                    self.selected_option += 1
                    self.rect.y += 75
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.moved = True
                if self.selected_option == 0:
                    self.selected_option = 2
                    self.rect.y = HEIGHT / 2 + 50
                else:
                    self.selected_option -= 1
                    self.rect.y -= 75
            elif keys[pygame.K_RETURN]:
                self.moved = True
                if self.selected_option == 0:
                    self.state_menu = not self.state_menu
                elif self.selected_option == 2:
                    done = True

    def update(self):
        self.get_input()

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

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, size=16):
        super().__init__()
        self.width = size
        self.max_width = size
        self.shrinking = True

        self.image = pygame.Surface((size, size))
        self.size = size
        self.image.fill('yellow')

        self.rect = self.image.get_rect(topleft=self.calculate_pos(x, y))
    
    def calculate_pos(self, x, y):
        return ((tile_size / 2 + x - self.size / 2), (tile_size / 2 + y - self.size / 2))
    
    def animate(self, factor):
        if self.shrinking:
            if self.width == 0:
                self.shrinking = False
            else:
                self.width -= factor
        else:
            if self.width == self.max_width:
                self.shrinking = True
            else:
                self.width += factor
        
        self.image = pygame.transform.scale(self.image, (self.width, self.max_width))
        self.image.fill('yellow')
    
    def update(self, x_shift):
        self.animate(0.5)
        self.rect.x += x_shift

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
        self.image = pygame.image.load('art/mid jump.png')
        self.rect = self.image.get_rect(topleft=pos)

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

class Button(pygame.sprite.Sprite):
    _height = 4

    def __init__(self, pos, width=tile_size, height=4):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=pos)

        self.height = height

        self.pressed = False
    
    def update(self, x_shift):
        self.rect.x += x_shift

        if self.pressed and self.height != 1:
            self.height = 1
            self.image = pygame.transform.scale(self.image, (tile_size, self.height))
            self.timer = time.time()

            self.rect.y += 3 # max height - pressed height
        elif not self.pressed and self.height != 4:
            if time.time() - self.timer >= 0.5:
                self.height = 4
                self.image = pygame.transform.scale(self.image, (tile_size, self.height))
                self.rect.y -= 3 # back to normal position

class Floating_pad(Button):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('art/floating pad.png')

level = Level(levels[0], screen, _data_manager)

keyup = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        keyup = True if event.type == pygame.KEYUP else False
    
    screen.fill('black')

    level.run(keyup)

    pygame.display.update()
    clock.tick(60)
