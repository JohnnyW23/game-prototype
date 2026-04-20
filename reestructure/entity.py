import pygame
from settings import *
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, z_offset=0):
        super().__init__(groups)

        # entity sprite loading
        self.path = path
        self.get_all_sprites()

        # entity animation
        self.animation_speed = 600
        self.direction = pygame.math.Vector2()
        self.direction_row = 3 
        self.last_animation_time = pygame.time.get_ticks()
        self.current_frame = 0

        # entity mode
        self.mode = f'idle'

        # entity surface creation
        self.image = self.get_frame(self.current_frame)
        self.rect = self.image.get_rect(topleft = pos)
        self.z_offset = z_offset
    

    def get_all_sprites(self):
        import os

        sprites = os.listdir(self.path)
        sprite_dict = {}
        for sprite in sprites:
            sprite_dict[sprite[:-4]] = pygame.image.load(f'{self.path}/{sprite}')

        self.all_sprites = sprite_dict
    

    def get_num_columns(self):
        mode = self.mode
        if "_" in mode: key = mode[:mode.find("_")]
        else: key = mode
        return HUMAN_FRAMES[key]


    def get_frame(self, frame_index):
        frame_height = 64
        frame_width = 64

        rect = pygame.Rect(
            frame_index * frame_width,
            self.direction_row * frame_height,
            frame_width,
            frame_height
        )
        big_rect = pygame.Rect(
            frame_index * 128,
            self.direction_row * 128,
            128,
            128
        )

        composed = pygame.Surface((128, 128), pygame.SRCALPHA)
        image = self.all_sprites[self.mode]

        if image.get_height() == 512:
            frame = image.subsurface(big_rect)
            composed.blit(frame, (0, 0))
        else:
            frame = image.subsurface(rect)
            composed.blit(frame, (32, 32))

        return composed

    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
            
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else:return 0
    

    def set_mode(self, mode):
        if "idle" in mode:
            self.animation_speed = 600
        elif mode == "run":
            self.animation_speed = 70
        elif "walk" in mode:
            self.animation_speed = 120
        elif "combat" in mode:
            self.animation_speed = 300
        elif "halfslash" in mode:
            self.animation_speed = 65
        elif "backslash" in mode:
            self.animation_speed = 60
        elif "slash" in mode:
            self.animation_speed = 55
        elif "shoot" in mode:
            self.animation_speed = 50
        elif mode == 'spellcast':
            if self.magic_name == "flame":
                self.animation_speed = 200
            elif self.magic_name == "heal":
                self.animation_speed = 65
        elif mode == 'thump':
            self.animation_speed = 70
        
        if mode != self.mode:
            self.current_frame = 0
            self.last_animation_time = pygame.time.get_ticks()

        self.mode = mode

    