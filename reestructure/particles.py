import pygame
from support import *
from settings import *


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': pygame.image.load(MAGIC_DATA['flame']['graphic']).convert_alpha(),
            'heal': pygame.image.load(MAGIC_DATA['heal']['graphic']).convert_alpha(),
            'dust': pygame.image.load('assets/particles/dust.png').convert_alpha(),
            'level_up': pygame.image.load('assets/particles/level_up.png').convert_alpha(),
            'fireball': pygame.image.load('assets/projectiles/fireball.png').convert_alpha(),
        }
    
    # preparar imagem da flecha e carregar ela
    

    def create_particles(self, pos, speed, row, name, groups, sprite_type='generic'):
        animation_frames = self.frames[name]
        
        ParticleEffect(pos, animation_frames, speed, row, name, groups, sprite_type)
    

    def create_projectile(self, pos, projectile_type, damage, speed, direction, row, animation_speed, groups, obstacles_sprites, attackable_sprites, sprite_type='generic'):
        animation_frames = self.frames[projectile_type]

        Projectile(pos, animation_frames, projectile_type, damage, speed, direction, row, animation_speed, groups, obstacles_sprites, attackable_sprites, sprite_type)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, speed, row, name, groups, sprite_type):
        super().__init__(groups)

        self.last_animation_time = pygame.time.get_ticks()
        self.animation_speed = speed
        self.current_frame = 0
        self.row = row
        self.name = name
        self.frames = animation_frames

        self.sprite_type = sprite_type

        self.all_sprites = {self.name: self.frames}

        self.image = self.get_frame(self.current_frame)
        self.total_frames = self.frames.get_width() // 64
        self.rect = self.image.get_rect(center = pos)

        self.z_offset = 0

        self.rounds = 0


    def get_frame(self, frame_index):
        frame_height = 64
        frame_width = 64

        rect = pygame.Rect(
            frame_index * frame_width,
            self.row * frame_height,
            frame_width,
            frame_height
        )

        image = self.all_sprites[self.name]
        frame = image.subsurface(rect)
        if self.name == 'dust':
            frame = pygame.transform.scale(frame, (48, 48))
        elif self.name == 'level_up':
            frame = pygame.transform.scale(frame, (80, 80))

        return frame


    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_animation_time >= self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1

            if self.current_frame < self.total_frames:
                self.image = self.get_frame(self.current_frame)

            else:
                if self.name == 'level_up':
                    self.current_frame = 0
                    self.rounds += 1
                    if self.rounds == 3:
                        self.kill()
                else:
                    self.kill()

    
    def update(self):
        self.animate()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, projectile_type, damage, speed, direction, row, animation_speed, groups, obstacles_sprites, attackable_sprites, sprite_type):
        super().__init__(*groups)

        self.name = projectile_type
        self.damage = damage
        self.speed = speed
        self.direction = direction
        self.row = row

        self.last_animation_time = pygame.time.get_ticks()
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.sprite_type = sprite_type

        self.frames = animation_frames

        self.all_sprites = {self.name: self.frames}

        self.image = self.get_frame(self.current_frame)
        self.total_frames = self.frames.get_width() // 64
        self.rect = self.image.get_rect(center = pos)

        self.obstacles_sprites = obstacles_sprites
        self.attackable_sprites = attackable_sprites

        self.z_offset = 0
    

    def get_frame(self, frame_index):
        frame_height = 64
        frame_width = 64
        
        rect = pygame.Rect(
            frame_index * frame_width,
            self.row * frame_height,
            frame_width,
            frame_height
        )

        image = self.all_sprites[self.name]
        frame = image.subsurface(rect)

        return frame


    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_animation_time >= self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1

            if self.current_frame < self.total_frames:
                self.image = self.get_frame(self.current_frame)

            else:
                self.current_frame = 0
    

    def collision(self):
        for sprite in self.obstacles_sprites:
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'barrel':
                pass
            else:
                if sprite.hitbox.colliderect(self.rect):
                    self.kill()
        
        enemy_sprites = [
            sprite for sprite in self.attackable_sprites 
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'
        ]

        for enemy in enemy_sprites:
            reduced_hitbox = enemy.dmg_hitbox.inflate(-5, -5)

            if reduced_hitbox.colliderect(self.rect):
                self.kill()


    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.collision()

    
    def update(self):
        self.animate()
        self.move()

