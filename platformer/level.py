import pygame
from pygame import mixer

from settings import *
from tile import *
from player import *
from menu import *
from coin import *
from achievement import *
from spike import *
from button import *

class Level:
    def __init__(self, level_data, surface, data_man):
        self.display_surface = surface
        self.data_man = data_man

        self.lvl_data = level_data

        ### DOT ###
        self.dot_image = pygame.image.load('art/menu dot.png')
        self.dot_rect = self.dot_image.get_rect(topleft=(WIDTH / 2 - 150, HEIGHT / 2 - 100))

        self.selected_option = 0
        self.moved = False

        self.state_menu = True # false - game, true - in menu

        ### LEVEL ###
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

    def get_input_dot(self):
        global done
        keys = pygame.key.get_pressed()

        if not self.moved:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.moved = True
                if self.selected_option == 2:
                    self.selected_option = 0
                    self.dot_rect.y = HEIGHT / 2 - 100
                else:
                    self.selected_option += 1
                    self.dot_rect.y += 75
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.moved = True
                if self.selected_option == 0:
                    self.selected_option = 2
                    self.dot_rect.y = HEIGHT / 2 + 50
                else:
                    self.selected_option -= 1
                    self.dot_rect.y -= 75
            elif keys[pygame.K_RETURN]:
                self.moved = True
                if self.selected_option == 0:
                    self.state_menu = not self.state_menu
                elif self.selected_option == 2:
                    done = True

    def update_dot(self):
            self.get_input_dot()

    def setup_level(self, layout, state, player_spawn_higher=False, height=100):
        # saving data
        self.data_man.save_data(self.curr_lvl, self.points)

        # basic setup
        self.menu = pygame.sprite.GroupSingle()
        self.menu.add(Menu((WIDTH / 2 - 114, HEIGHT / 2 - 100))) # size 228x200 px

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
        if self.state_menu:
            if keyup_:
                self.moved = False
            self.update_dot()

            self.menu.draw(self.display_surface)
            self.display_surface.blit(self.dot_image, (self.dot_rect.x, self.dot_rect.y))

        if not self.state_menu:
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