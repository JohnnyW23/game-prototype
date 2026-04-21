import pygame
from support import *
from settings import *


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'fireball': pygame.image.load(MAGIC_DATA['fireball']['graphic']).convert_alpha(),
            'heal': pygame.image.load(MAGIC_DATA['heal']['graphic']).convert_alpha(),
            
            'dust': pygame.image.load('assets/particles/dust.png').convert_alpha()
        }
    

    def create_particles(self, pos, speed, row, name, groups):
        animation_frames = self.frames[name]
        
        ParticleEffect(pos, animation_frames, speed, row, name, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, speed, row, name, groups, offset=0):
        super().__init__(groups)

        self.last_animation_time = pygame.time.get_ticks()
        self.animation_speed = speed
        self.current_frame = 0
        self.direction_row = row
        self.name = name
        self.frames = animation_frames

        self.all_sprites = {self.name: self.frames}

        self.image = self.get_frame(self.current_frame)
        self.total_frames = self.frames.get_width() // 64
        self.rect = self.image.get_rect(center = pos)
        self.rect.y += offset

        self.z_offset = 0


    def get_frame(self, frame_index):
        frame_height = 64
        frame_width = 64

        rect = pygame.Rect(
            frame_index * frame_width,
            self.direction_row * frame_height,
            frame_width,
            frame_height
        )

        image = self.all_sprites[self.name]
        frame = image.subsurface(rect)
        if self.name == 'dust':
            frame = pygame.transform.scale(frame, (48, 48))

        return frame


    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_animation_time >= self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1

            if self.current_frame < self.total_frames:
                self.image = self.get_frame(self.current_frame)

            else:
                self.kill()
    
    def update(self):
        self.animate()
        