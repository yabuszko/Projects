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
from turtle import *

class Level:
    def __init__(self, surface, data_man):
        self.display_surface = surface
        self.data_man = data_man

        self.done = False

        ### DOT ###
        self.dot_image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'menu dot.png'))
        self.dot_rect = self.dot_image.get_rect(topleft=(WIDTH / 2 - 150, HEIGHT / 2 - 100))

        self.selected_option = 0
        self.moved = False

        self.curr_lvl = 0
        self.game_state = 'menu' # false - game, true - in menu

        ### LEVEL ###
        self.world_shift = 0

        self.static_player_pos_x = 6 * tile_size
        self.player_shift = 0

        self.spike_time = 2.5
        self.trigger_state = None

        self.temp_points = 0 # collected during a level
        self.keys_collected = 0

        ### OTHERS ###
        self.touches_trigger = False
        self.frame = 1

        self.data = {
            'levels_completed': 0,
            'coins': 0
        }

        if os.stat(os.path.join(ROOT_DIR, 'others','data.txt')).st_size == 0:
            self.clear_data()

        with open(os.path.join(ROOT_DIR, 'others','data.txt')) as datafile:
            self.data = json.load(datafile)

        self.curr_lvl = self.data["levels_completed"]
        self.lvl_data = levels[self.data["levels_completed"]]

        self.levitate = False

        self.levels_with_exit_triggered = [0, 4]
        self.mid_air_jumps_allowed = False

        self.font = pygame.font.Font(os.path.join(ROOT_DIR, 'others', 'tahoma.ttf'), 32)
        self.cop_font = pygame.font.Font(os.path.join(ROOT_DIR, 'others', 'tahoma.ttf'), 10)
        
        self.coin_collect_sound = mixer.Sound(os.path.join(ROOT_DIR,'sounds', 'coin sound.wav'))
        self.button_press_sound = mixer.Sound(os.path.join(ROOT_DIR,'sounds', 'button.mp3'))
        self.death_sound = mixer.Sound(os.path.join(ROOT_DIR,'sounds', 'death.mp3'))
        self.achievement_sound = mixer.Sound(os.path.join(ROOT_DIR,'sounds', 'achievement.mp3'))
        self.key_sound = mixer.Sound(os.path.join(ROOT_DIR,'sounds', 'key.mp3'))
        self.door_sound = mixer.Sound(os.path.join(ROOT_DIR,'sounds', 'button.mp3'))
        self.switch_sound = mixer.Sound(os.path.join(ROOT_DIR, 'sounds', 'switch.mp3'))

        self.level_tiles = pygame.sprite.Group()
        self.setup_level_tiles()

        if self.curr_lvl in self.levels_with_exit_triggered:
            self.setup_level(self.lvl_data, 'triggered', True) # TODO: change after saving, DONE
        else:
            self.setup_level(self.lvl_data, 'not_triggered', True)

        mixer.music.load(os.path.join(ROOT_DIR,'sounds', 'music1.mp3'))
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
        self.trigger_state = state

        # saving data
        self.data_man.save_data(self.data["levels_completed"], self.data["coins"])

        self.setup_level_tiles()

        # menu
        self.menu = pygame.sprite.GroupSingle()
        self.menu.add(Menu((WIDTH / 2 - 114, HEIGHT / 2 - 100))) # size 228x200 px

        self.bckg = pygame.sprite.GroupSingle()
        self.bckg.add(Background((WIDTH, HEIGHT)))

        # mobs
        self.turtles = pygame.sprite.Group()

        # blocks
        self.tiles = pygame.sprite.Group()

        self.coins = pygame.sprite.Group()
        self.floating_pads = pygame.sprite.Group()

        # spikes
        self.spikes = pygame.sprite.Group()

        # mechanisms
        self.doors = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()

        # player
        self.player = pygame.sprite.GroupSingle() 

        # achievements
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
                    self.tiles.add(Tile('brick', (x, y)))
                elif cell == 'C': # coin
                    self.coins.add(Coin(x, y))
                elif cell == 'P': # player
                    player_sprite = Player((x, y)) if not spawn_player_higher else Player((x, y - height))
                    self.player.add(player_sprite)
                elif cell == 'E': # exit
                    self.tiles.add(Tile('exit_tile', (x, y), state))
                elif cell == 'T': # exit trigger
                    self.tiles.add(Tile('exit_trigger', (x, y)))
                elif cell == 'F': # floating pad
                    self.floating_pads.add(Floating_pad((x, y + tile_size - Floating_pad._height)))
                elif cell == 'R': # royal block
                    self.tiles.add(Tile('royal_block', (x, y)))
                elif cell == 'D': # door
                    self.doors.add(Door((x, y)))
                elif cell == 'K': # key
                    self.keys.add(Key((x + 16, y + 16)))
                elif cell == 'Q': # cart
                    self.turtles.add(Turtle((x, y + tile_size - 50)))
                elif cell == 'g': # green trigger
                    self.tiles.add(Tile('green_trigger', (x, y)))
                elif cell == 'r': # red trigger
                    self.tiles.add(Tile('red_trigger', (x, y)))
                elif cell == '@': # green inactivated
                    self.tiles.add(Tile('green_block', (x, y), None, 'off'))
                elif cell == '#': # green activated
                    self.tiles.add(Tile('green_block', (x, y), None, 'on'))
                elif cell == '$': # red inactivated
                    self.tiles.add(Tile('red_block', (x, y), None, 'off'))
                elif cell == '^': # red activated
                    self.tiles.add(Tile('red_block', (x, y), None, 'on'))
                elif cell == '1': # Spike up
                    self.spikes.add(Spike('spike_up', (x, y + tile_size - 32), None))
                elif cell == '2': # Spike down
                    self.spikes.add(Spike('spike_down', (x, y), None))
                elif cell == '3': # Spike right
                    self.spikes.add(Spike('spike_right', (x, y), None))
                elif cell == '4': # spike left
                    self.spikes.add(Spike('spike_left', (x + 32, y), None))
                elif cell == '5': # Angry spike up
                    self.spikes.add(Spike('angry_spike_up', (x, y + tile_size - 32), self.spike_time))
                elif cell == '6': # Angry spike down
                    self.spikes.add(Spike('angry_spike_down', (x, y), self.spike_time))
                elif cell == '7': # Angry spike right
                    self.spikes.add(Spike('angry_spike_right', (x, y), self.spike_time))
                elif cell == '8': # Angry spike left
                    self.spikes.add(Spike('angry_spike_left', (x + 32, y), self.spike_time))
                elif cell == '!': # mid air achievement
                    self.achievement1.add(Mid_air_jump_achievement((x + 16, y + 16), 16))
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 3.5 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
        elif player_x > screen_width - (screen_width / 3.5) and direction_x > 0:
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
        for tile in self.tiles.sprites():
            if tile.type == 'exit_trigger' and not self.trigger_state == 'triggered':
                if tile.rect.colliderect(self.player.sprite.rect):
                    tile.state = tile.states['triggered']
                    self.trigger_state = 'triggered'

                    self.unlock_exit()
                    return

    def exit_collision(self):
        for tile in self.tiles.sprites():
            if tile.type == 'exit_tile':
                if tile.rect.colliderect(self.player.sprite.rect) and self.trigger_state == 'triggered':
                    if len(levels) >= self.curr_lvl + 2: # check if out of range
                        self.curr_lvl += 1
                        self.lvl_data = levels[self.curr_lvl]

                        if self.curr_lvl in self.levels_with_exit_triggered:
                            self.setup_level(self.lvl_data, 'triggered', True)
                        else:
                            self.setup_level(self.lvl_data, 'not_triggered', True)

    def spike_collision(self):
        for spike in self.spikes.sprites():
            if spike.rect.colliderect(self.player.sprite.rect):
                self.death()

    def turtle_collision(self):
        for turtle in self.turtles.sprites():
            if turtle.rect.colliderect(self.player.sprite.rect):
                self.death()
    
    def turtle_bounce_collision(self):
        for turtle in self.turtles.sprites():
            for tile in self.tiles.sprites():
                if not ((tile.type == 'red_block' and tile.state_block == 'off') or (
                    tile.type == 'green_block' and tile.state_block == 'off'
                )):
                    if tile.rect.y == turtle.rect.y - 14:
                        if tile.rect.colliderect(turtle.rect):
                            turtle.dir = turtle.dirs["right"] if turtle.dir == turtle.dirs["left"] else turtle.dirs["left"]
                            return
            for spike in self.spikes.sprites():
                # 32                   50
                if (spike.type == 'spike_up' or (spike.type == 'angry_spike_up' and spike.state == spike.states['closed'])):
                    if spike.rect.y  == turtle.rect.y + 18: # TODO: change to height
                        if spike.rect.colliderect(turtle.rect):
                            turtle.dir = turtle.dirs["right"] if turtle.dir == turtle.dirs["left"] else turtle.dirs["left"]
                            return
                # 64                   50
                elif (spike.type == 'spike_down' or spike.type == 'spike_left' or spike.type == 'angry_spike_right' or 
                spike.type == 'angry_spike_left' or spike.type == 'spike_right' or 
                spike.type == 'angry_spike_down'):
                    if spike.rect.y  == turtle.rect.y - 14:
                        if spike.rect.colliderect(turtle.rect):
                            turtle.dir = turtle.dirs["right"] if turtle.dir == turtle.dirs["left"] else turtle.dirs["left"]
                            return
                # tile_size * factor    50
                elif (spike.type == 'angry_spike_up' and spike.state == spike.states["angry"]):
                    if spike.rect.y == turtle.rect.y - 78: #TODO: change to spike height
                        if spike.rect.colliderect(turtle.rect):
                            turtle.dir = turtle.dirs["right"] if turtle.dir == turtle.dirs["left"] else turtle.dirs["left"]
                            return

    def horizontal_movement_collision(self):
        self.player.sprite.rect.x += self.player.sprite.direction.x * self.player.sprite.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(self.player.sprite.rect) and not (
                 tile.type == 'exit_tile' or tile.type == 'exit_trigger' or
                 (tile.type == 'green_block' and tile.state_block == 'off') or
                 (tile.type == 'red_block' and tile.state_block == 'off')
            ): # then flip
                if self.player.sprite.direction.x < 0: # moving left
                    self.player.sprite.rect.left = tile.rect.right
                elif self.player.sprite.direction.x > 0: # moving right
                    self.player.sprite.rect.right = tile.rect.left
        
        if self.doors and self.keys_collected == 0:
            for door in self.doors.sprites():
                if door.rect.colliderect(self.player.sprite.rect):  # then flip
                    if self.player.sprite.direction.x < 0: # moving left
                        self.player.sprite.rect.left = door.rect.right
                    elif self.player.sprite.direction.x > 0: # moving right
                        self.player.sprite.rect.right = door.rect.left

    def vertical_movement_collision(self):
        self.player.sprite.apply_gravity(not self.levitate)
        if self.player.sprite.jumped:
            self.touches_trigger = False

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(self.player.sprite.rect) and not (
                 tile.type == 'exit_tile' or tile.type == 'exit_trigger' or
                 (tile.type == 'green_block' and tile.state_block == 'off') or
                 (tile.type == 'red_block' and tile.state_block == 'off')
            ):  # then flip
                if self.player.sprite.direction.y > 0: # moving/falling down
                        self.player.sprite.rect.bottom = tile.rect.top
                        self.player.sprite.direction.y = 0 # glitch protection

                        self.player.sprite.jumped = False # on the ground, allow for jumping
                elif self.player.sprite.direction.y < 0 or self.levitate: # moving up
                        self.player.sprite.rect.top = tile.rect.bottom
                        self.player.sprite.direction.y = 0 # hit a block from below = bounce down
                
                if (tile.type == 'green_trigger' or tile.type == 'red_trigger'):
                    if not self.touches_trigger:
                        col = 'green' if tile.type == 'green_trigger' else 'red'
                        self.switch_sound.play()

                        for tile_ in self.tiles.sprites():
                            if tile_.type == f'{col}_block':
                                tile_.switch(col)
                        
                        self.touches_trigger = True
                else:
                    self.touches_trigger = False

        if self.doors and self.keys_collected == 0:
            for door in self.doors.sprites():
                if door.rect.colliderect(self.player.sprite.rect):  # then flip
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
            self.setup_level(self.lvl_data, 'triggered', True) # false if spawn without fall
        else:
            self.setup_level(self.lvl_data, 'not_triggered', True) # false if spawn without fall

    def show_text(self, pos, what_to_render):
        self.display_surface.blit(what_to_render, pos)
    
    def unlock_exit(self):
        unlocked1, unlocked2 = False, False
        for tile in self.tiles.sprites():
            if tile.type == 'exit_trigger':
                tile.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'exit trigger2.png'))
                unlocked1 = True
            elif tile.type == 'exit_tile':
                tile.image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'exit2.png'))
                unlocked2 = True
            if unlocked1 and unlocked2:
                return 

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
            self.tiles.update(self.world_shift)

            # mobs
            self.turtles.update(self.world_shift)
            self.turtle_bounce_collision()

            # spikes
            self.spikes.update(self.world_shift)

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
            self.turtle_collision()
            self.key_collision()
            self.door_collision()
            self.spike_collision()
            self.floating_pad_collision()
            self.achievement_collision()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()

            ###### drawing ######
            self.bckg.draw(self.display_surface)

            for tile in self.tiles.sprites():
                if tile.rect.x > -tile_size and tile.rect.x < WIDTH:
                    self.display_surface.blit(tile.image, (tile.rect.x, tile.rect.y))

            for coin in self.coins.sprites():
                if coin.rect.x > -16 and coin.rect.x < WIDTH:
                    self.display_surface.blit(coin.image, (coin.rect.x, coin.rect.y))

            for spike in self.spikes.sprites():
                if (((spike.type == 'spike_right' or spike.type == 'spike_left' 
                or spike.type == 'angry_spike_left' or spike.type == 'angry_spike_right') and
                (spike.rect.x > -spike.width and spike.rect.x < WIDTH)) or ((spike.type == 'spike_up' or spike.type == 'spike_down' 
                or spike.type == 'angry_spike_down' or spike.type == 'angry_spike_up') and
                (spike.rect.x > -tile_size and spike.rect.x < WIDTH))):
                    self.display_surface.blit(spike.image, (spike.rect.x, spike.rect.y))

            for turtle in self.turtles.sprites():
                if turtle.rect.x > -tile_size and turtle.rect.x < WIDTH:
                    self.display_surface.blit(turtle.image, (turtle.rect.x, turtle.rect.y))
            
            for floating_pad in self.floating_pads.sprites():
                if floating_pad.rect.x > -tile_size and floating_pad.rect.x < WIDTH:
                    self.display_surface.blit(floating_pad.image, (floating_pad.rect.x, floating_pad.rect.y))

            for door in self.doors.sprites():
                if door.rect.x > -tile_size and door.rect.x < WIDTH:
                    self.display_surface.blit(door.image, (door.rect.x, door.rect.y))

            for key in self.keys.sprites():
                if key.rect.x > -16 and key.rect.x < WIDTH:
                    self.display_surface.blit(key.image, (key.rect.x, key.rect.y))        

            self.achievement1.draw(self.display_surface)

            self.player.draw(self.display_surface)

            if self.keys_collected > 0:
                self.blit_keys(self.keys_collected)

            # text
            level_txt = self.font.render("Poziom: " + str(self.curr_lvl + 1), True, 'green')
            self.show_text((0, 0), level_txt)

            score = self.font.render("Punkty: " + str(self.data["coins"] + self.temp_points), True, 'white')
            self.show_text((0, level_txt.get_rect().bottom + 5), score)

            cop = self.cop_font.render("by Oliwier Moskalewicz 2022", True, 'white')
            self.show_text((5, HEIGHT - 15), cop)
    
    def blit_keys(self, number):
        key_image = pygame.image.load(os.path.join(ROOT_DIR, 'art', 'key.png'))

        x = WIDTH - 37
        y = 5
        for i in range(number):
            self.display_surface.blit(key_image, (x, y))
            x -= 37

    def clear_data(self):
        with open(os.path.join(ROOT_DIR, 'others', 'data.txt'), 'w') as file:
            self.data = {
                'levels_completed': 0,
                'coins': 0
            }
            json.dump(self.data, file)
