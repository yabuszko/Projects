import pygame
import json
import os
from pygame import mixer

from settings import *
from tile import *
from player import *
from menu import *
from coin import *
from achievement import *
from spike import *
from button import *
from level_menu import *
from background import *
from door import *
from key import *

class Level:
    def __init__(self, surface, data_man):
        self.display_surface = surface
        self.data_man = data_man

        self.done = False

        ### DOT ###
        self.dot_image = pygame.image.load('art/menu dot.png')
        self.dot_rect = self.dot_image.get_rect(topleft=(WIDTH / 2 - 150, HEIGHT / 2 - 100))

        self.selected_option = 0
        self.moved = False

        self.curr_lvl = 0
        self.game_state = 'menu' # false - game, true - in menu

        ### LEVEL ###
        self.world_shift = 0

        self.static_player_pos_x = 6 * tile_size
        self.player_shift = 0

        self.temp_points = 0 # collected during a level
        self.keys_collected = 0

        self.data = {
            'levels_completed': 0,
            'coins': 0,
        }

        if os.stat('others/data.txt').st_size == 0:
            self.clear_data()

        with open('others/data.txt') as datafile:
            self.data = json.load(datafile)

        self.curr_lvl = self.data["levels_completed"]
        self.lvl_data = levels[self.data["levels_completed"]]

        self.levitate = False

        self.levels_with_exit_triggered = [0]
        self.mid_air_jumps_allowed = False

        self.font = pygame.font.Font('others/tahoma.ttf', 32)
        
        self.coin_collect_sound = mixer.Sound('sounds/coin sound.wav')
        self.button_press_sound = mixer.Sound('sounds/button.mp3')
        self.death_sound = mixer.Sound('sounds/death.mp3')
        self.achievement_sound = mixer.Sound('sounds/achievement.mp3')
        self.key_sound = mixer.Sound('sounds/key.mp3')
        self.door_sound = mixer.Sound('sounds/door.mp3')

        self.level_tiles = pygame.sprite.Group()
        self.setup_level_tiles()

        if self.curr_lvl in self.levels_with_exit_triggered:
            self.setup_level(self.lvl_data, 2, True) # TODO: change after saving, DONE
        else:
            self.setup_level(self.lvl_data, 1, True)

        mixer.music.load("sounds/music1.mp3")
        mixer.music.set_volume(MUSIC_VOLUME)
        mixer.music.play(-1)

    def get_input_dot(self):
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
                    self.game_state = 'game'
                elif self.selected_option == 1:
                    self.game_state = 'level_menu'
                elif self.selected_option == 2:
                    self.done = True

    def update_dot(self):
            self.get_input_dot()

    def setup_level_tiles(self):
        self.level_tiles.empty()

        for i in range(self.data["levels_completed"] + 1):
            self.level_tiles.add(Level_tile((0+100*i, 0), (100, 58), i))

    def setup_level(self, layout, state, spawn_player_higher=False, height=100):
        # basic setup
        if self.curr_lvl > self.data["levels_completed"]:
            self.data["levels_completed"] = self.curr_lvl
        
        self.keys_collected = 0
        # saving data
        self.data_man.save_data(self.data["levels_completed"], self.data["coins"])

        self.setup_level_tiles()

        self.menu = pygame.sprite.GroupSingle()
        self.menu.add(Menu((WIDTH / 2 - 114, HEIGHT / 2 - 100))) # size 228x200 px

        self.bckg = pygame.sprite.GroupSingle()
        self.bckg.add(Background((WIDTH, HEIGHT)))

        # things
        self.bricks = pygame.sprite.Group()
        self.royalblocks = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.floating_pads = pygame.sprite.Group()

        self.spikesUp = pygame.sprite.Group()
        self.spikesDown = pygame.sprite.Group()
        self.spikesRight = pygame.sprite.Group()
        self.spikesLeft = pygame.sprite.Group()

        self.doors = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()

        self.player = pygame.sprite.GroupSingle() 
        self.exit = pygame.sprite.GroupSingle()
        self.exit_trigger = pygame.sprite.GroupSingle()

        self.achievement1 = pygame.sprite.GroupSingle()

        self.data["coins"] += self.temp_points
        self.temp_points = 0

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'P':
                    self.player_shift = -(col_index * tile_size) + self.static_player_pos_x # -(col*tl - static_x) = -col*tl + static_x
                    break

        # loading level
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = (col_index * tile_size) + self.player_shift
                y = row_index * tile_size

                if cell == 'X': # block
                    self.bricks.add(Brick((x, y), tile_size))
                elif cell == 'C': # coin
                    self.coins.add(Coin(x, y))
                elif cell == 'P': # player
                    player_sprite = Player((x, y)) if not spawn_player_higher else Player((x, y - height))
                    self.player.add(player_sprite)
                elif cell == 'E': # exit
                    self.exit.add(Exit_tile((x, y), tile_size, state))
                elif cell == 'T': # exit trigger
                    self.exit_trigger.add(Exit_trigger_tile((x, y), tile_size))
                elif cell == 'F': # floating pad
                    self.floating_pads.add(Floating_pad((x, y + tile_size - Floating_pad._height)))
                elif cell == 'R': # royal block
                    self.royalblocks.add(RoyalBlock((x, y), tile_size))
                elif cell == 'D': # door
                    self.doors.add(Door((x, y)))
                elif cell == 'K':
                    self.keys.add(Key((x + 16, y + 16)))
                elif cell == '1': # Spike up
                    self.spikesUp.add(SpikesUp((x, y + tile_size - 32)))
                elif cell == '2': # Spike down
                    self.spikesDown.add(SpikesDown((x, y)))
                elif cell == '3': # Spike right
                    self.spikesRight.add(SpikesRight((x, y)))
                elif cell == '4': # spike left
                    self.spikesLeft.add(SpikesLeft((x + 32, y)))
                elif cell == '!': # mid air achievement
                    self.achievement1.add(Mid_air_jump_achievement((x + 16, y + 16), 16))
    
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
        for coin in self.coins.sprites():
            if coin.rect.colliderect(self.player.sprite.rect): #if player hits a coin
                self.coin_collect_sound.play()

                self.coins.remove(coin)
                self.temp_points += 1
                #self.total_points += 1
    
    def key_collision(self):
        for key in self.keys.sprites():
            if key.rect.colliderect(self.player.sprite.rect):
                self.key_sound.play()
                self.keys.remove(key)

                self.keys_collected += 1
                #self.data["keys"] += 1
    
    def door_collision(self):
        for door in self.doors.sprites():
            if door.rect.colliderect(self.player.sprite.rect):
                if self.keys_collected > 0:
                    self.door_sound.play()
                    self.keys_collected -= 1

                    self.doors.remove(door)

    def achievement_collision(self):
        if self.achievement1:
            player = self.player.sprite
            midairjumpachievement = self.achievement1.sprite

            if player.rect.colliderect(midairjumpachievement.rect):
                self.achievement_sound.play()
                self.achievement1.remove(self.achievement1.sprite)
                self.mid_air_jumps_allowed = True

    
    def floating_pad_collision(self):
        for pad in self.floating_pads.sprites():
            if pad.rect.colliderect(self.player.sprite.rect):
                if not pad.pressed:
                    self.button_press_sound.play()
                    self.levitate = True
                    self.timer = time.time()

                pad.pressed = True
            else:
                pad.pressed = False

    def exit_trigger_collision(self):
        if self.exit_trigger: # crash protection
            if self.exit_trigger.sprite.rect.colliderect(self.player.sprite.rect):
                self.exit.sprite.state = 2
                self.unlock_exit()
    
    def exit_collision(self):
        if self.exit:
            if self.exit.sprite.rect.colliderect(self.player.sprite.rect) and self.exit.sprite.state == 2:
                #self.temp_points = 0

                if len(levels) >= self.curr_lvl + 2: # check if out of range
                    self.curr_lvl += 1            
                    self.lvl_data = levels[self.curr_lvl]

                    self.setup_level(self.lvl_data, 1, True) # TODO: change after saving

    def spike_collision(self):
        for spikeu in self.spikesUp.sprites():
            if spikeu.rect.colliderect(self.player.sprite.rect):
                self.death()
                #return
        for spiked in self.spikesDown.sprites():
            if spiked.rect.colliderect(self.player.sprite.rect):
                self.death()
                #return
        for spiker in self.spikesRight.sprites():
            if spiker.rect.colliderect(self.player.sprite.rect):
                self.death()
                #return
        for spikel in self.spikesLeft.sprites():
            if spikel.rect.colliderect(self.player.sprite.rect):
                self.death()
                #return

    
    def horizontal_movement_collision(self):
        self.player.sprite.rect.x += self.player.sprite.direction.x * self.player.sprite.speed

        if self.bricks:
            for brick in self.bricks.sprites():
                if brick.rect.colliderect(self.player.sprite.rect): # then flip
                    if self.player.sprite.direction.x < 0: # moving left
                        self.player.sprite.rect.left = brick.rect.right
                    elif self.player.sprite.direction.x > 0: # moving right
                        self.player.sprite.rect.right = brick.rect.left
        
        if self.royalblocks:
            for royalblock in self.royalblocks.sprites():
                if royalblock.rect.colliderect(self.player.sprite.rect): # then flip
                    if self.player.sprite.direction.x < 0: # moving left
                        self.player.sprite.rect.left = royalblock.rect.right
                    elif self.player.sprite.direction.x > 0: # moving right
                        self.player.sprite.rect.right = royalblock.rect.left
        
        if self.doors and self.keys_collected == 0:
            for door in self.doors.sprites():
                if door.rect.colliderect(self.player.sprite.rect): # then flip
                    if self.player.sprite.direction.x < 0: # moving left
                        self.player.sprite.rect.left = door.rect.right
                    elif self.player.sprite.direction.x > 0: # moving right
                        self.player.sprite.rect.right = door.rect.left

    def vertical_movement_collision(self):
        self.player.sprite.apply_gravity(not self.levitate)

        if self.bricks:
            for tile in self.bricks.sprites():
                if tile.rect.colliderect(self.player.sprite.rect): # then flip
                    if self.player.sprite.direction.y > 0: # moving/falling down
                        self.player.sprite.rect.bottom = tile.rect.top
                        self.player.sprite.direction.y = 0 # glitch protection

                        self.player.sprite.jumped = False # on the ground, allow for jumping
                    elif self.player.sprite.direction.y < 0 or self.levitate: # moving up
                        self.player.sprite.rect.top = tile.rect.bottom
                        self.player.sprite.direction.y = 0 # hit a block from below = bounce down

        if self.royalblocks:   
            for royalblock in self.royalblocks.sprites():
                if royalblock.rect.colliderect(self.player.sprite.rect): # then flip
                    if self.player.sprite.direction.y > 0: # moving/falling down
                        self.player.sprite.rect.bottom = royalblock.rect.top
                        self.player.sprite.direction.y = 0 # glitch protection

                        self.player.sprite.jumped = False # on the ground, allow for jumping
                    elif self.player.sprite.direction.y < 0 or self.levitate: # moving up
                        self.player.sprite.rect.top = royalblock.rect.bottom
                        self.player.sprite.direction.y = 0 # hit a block from below = bounce down
        if self.doors and self.keys_collected == 0:
            for door in self.doors.sprites():
                if door.rect.colliderect(self.player.sprite.rect): # then flip
                    if self.player.sprite.direction.y > 0: # moving/falling down
                        self.player.sprite.rect.bottom = door.rect.top
                        self.player.sprite.direction.y = 0 # glitch protection

                        self.player.sprite.jumped = False # on the ground, allow for jumping
                    elif self.player.sprite.direction.y < 0 or self.levitate: # moving up
                        self.player.sprite.rect.top = door.rect.bottom
                        self.player.sprite.direction.y = 0 # hit a block from below = bounce down
        
        # if fell down
        if self.player.sprite.direction.y > 0 and self.player.sprite.rect.bottom > HEIGHT:
            self.death()
    
    def death(self):
        self.death_sound.play()

        self.world_shift = 0
        self.temp_points = 0
        self.temp_keys = 0

        if self.curr_lvl in self.levels_with_exit_triggered:
            self.setup_level(self.lvl_data, 2, True) # false if spawn without fall
        else:
            self.setup_level(self.lvl_data, 1, True) # false if spawn without fall

    def show_text(self, pos, what_to_render):
        self.display_surface.blit(what_to_render, pos)
    
    def unlock_exit(self):
        self.exit_trigger.sprite.image = pygame.image.load("art/exit trigger2.png")
        self.exit.sprite.image = pygame.image.load("art/exit2.png")

    def run_menu(self):
        self.game_state = 'menu'

    def run(self, keyup_, mousedown_):
        if self.levitate:
            if time.time() - self.timer >= 2:
                self.levitate = False
            else:
                self.player.sprite.jumped = True # disable jumping
                self.player.sprite.lift(2)

        self.scroll_x()

        # menu
        if self.game_state == 'menu':
            if keyup_:
                self.moved = False
            self.update_dot()

            self.menu.draw(self.display_surface)
            self.display_surface.blit(self.dot_image, (self.dot_rect.x, self.dot_rect.y))
        elif self.game_state == 'level_menu':
            self.level_tiles.update()
            self.level_tiles.draw(self.display_surface)

            for lvl_tile in self.level_tiles.sprites():
                if lvl_tile.click_check(mousedown_):
                    self.temp_points = 0 # prevention
                    self.temp_keys = 0
                    
                    self.curr_lvl = lvl_tile.level
                    self.lvl_data = levels[self.curr_lvl]
                    self.game_state = 'game'

                    if lvl_tile.level in self.levels_with_exit_triggered:
                        self.setup_level(self.lvl_data, 2, True)
                    else:
                        self.setup_level(self.lvl_data, 1, True)
                    
                    return
        elif self.game_state == 'game':
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

            # doors and keys
            self.doors.update(self.world_shift)
            self.keys.update(self.world_shift)

            # coins
            self.coins.update(self.world_shift)

            # achievements
            self.achievement1.update(self.world_shift)

            # player
            self.player.update(self.mid_air_jumps_allowed)
            self.exit_trigger_collision()
            self.exit_collision()
            self.coin_collision()
            self.key_collision()
            self.door_collision()
            self.spike_collision()
            self.floating_pad_collision()
            self.achievement_collision()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()

            ###### drawing ######
            self.bckg.draw(self.display_surface)

            self.bricks.draw(self.display_surface)
            self.royalblocks.draw(self.display_surface)

            self.exit.draw(self.display_surface)
            self.exit_trigger.draw(self.display_surface)

            self.spikesUp.draw(self.display_surface)
            self.spikesDown.draw(self.display_surface)
            self.spikesRight.draw(self.display_surface)
            self.spikesLeft.draw(self.display_surface)

            self.floating_pads.draw(self.display_surface)

            self.doors.draw(self.display_surface)
            self.keys.draw(self.display_surface)

            self.coins.draw(self.display_surface)

            self.achievement1.draw(self.display_surface)

            self.player.draw(self.display_surface)

            if self.keys_collected > 0:
                self.blit_keys(self.keys_collected)

            # text
            level_txt = self.font.render("Poziom: " + str(self.curr_lvl + 1), True, 'green')
            self.show_text((0, 0), level_txt)

            score = self.font.render("Punkty: " + str(self.data["coins"] + self.temp_points), True, 'white')
            self.show_text((0, level_txt.get_rect().bottom + 5), score)
    
    def blit_keys(self, number):
        key_image = pygame.image.load('art/key.png')

        x = WIDTH - 37
        y = 5
        for i in range(number):
            self.display_surface.blit(key_image, (x, y))
            x -= 37

    def clear_data(self):
        with open('others/data.txt', 'w') as file:
            self.data = {
                'levels_completed': 0,
                'coins': 0
            }
            json.dump(self.data, file)
