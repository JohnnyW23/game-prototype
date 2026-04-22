import pygame
from settings import *
from entity import Entity
from debug import debug


class Enemy(Entity):
    def __init__(self, name, id, pos, groups, path, obstacle_sprites, damage_player):
        super().__init__(pos, groups, path, z_offset=0)

        # general setup
        self.sprite_type = 'enemy'
        self.id = id

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.obstacle_sprites = obstacle_sprites
        self.moving = False

        # stats
        self.name = name
        enemy_info = ENEMY_DATA[self.name]
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.speed = self.set_speed()
        self.damage = enemy_info['damage']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.attack_type = enemy_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attacking = False
        self.attack_cooldown = enemy_info['attack_cooldown']
        self.damage_player = damage_player
        self.dying = False

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


        if 'zombie' in self.name:
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 32, 24)
            self.dmg_hitbox = pygame.Rect(self.rect.x, self.rect.y, 32, 52)
        self.rect.bottom = self.hitbox.bottom + 32
        self.rect.right = self.hitbox.right  + 48
        self.dmg_hitbox.bottom = self.hitbox.bottom
        self.dmg_hitbox.right = self.hitbox.right
    

    def set_speed(self):
        import random

        enemy_info = ENEMY_DATA[self.name]
        return random.uniform(enemy_info['speed'] - 1, enemy_info['speed'] + 1)
    

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.hitbox.center)
        player_vec = pygame.math.Vector2(player.hitbox.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 32:
            direction = (player_vec - enemy_vec).normalize()
            self.moving = True
        else:
            self.moving = False
            direction = pygame.math.Vector2()
    

        return (distance, direction)
    

    def get_status(self, player):

        if self.attacking or self.health <= 0 or self.dying:
            return
            
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.set_mode(self.attack_type)
        elif distance <= self.notice_radius:
            self.set_mode('walk')
        else:
            self.set_mode('idle')
    

    def actions(self, player):
        
        if self.mode == 'idle' or self.dying:
            self.direction = pygame.math.Vector2()
        
        else:
            self.direction = self.get_player_distance_direction(player)[1]

            if self.moving:
                if abs(self.direction.x) > abs(self.direction.y):
                    if self.direction.x > 0:
                        self.direction_row = 3  # direita
                    else:
                        self.direction_row = 1  # esquerda
                else:
                    if self.direction.y > 0:
                        self.direction_row = 2  # baixo
                    else:
                        self.direction_row = 0  # cima

            if self.mode == self.attack_type and not self.attacking:
                self.attacking = True
                self.can_attack = False
                self.attack_time = pygame.time.get_ticks()
                self.damage_player(self.damage, self.attack_type)

    
    def set_mode(self, mode):
        if "idle" in mode:
            self.animation_speed = 600
        elif "walk" in mode:
            self.animation_speed = 120
        elif mode == 'thump':
            self.animation_speed = 70
        elif mode == 'hurt':
            self.animation_speed = 150
        elif mode == 'slash':
            self.animation_speed = 150
        
        if mode != self.mode:
            self.current_frame = 0
            self.last_animation_time = pygame.time.get_ticks()

        self.mode = mode


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.bottom = self.hitbox.bottom + 32
        self.rect.right = self.hitbox.right  + 48
        self.dmg_hitbox.bottom = self.hitbox.bottom
        self.dmg_hitbox.right = self.hitbox.right
    

    def hitbox_debug(self, offset):
        display_surface = pygame.display.get_surface()

        offset_hitbox = self.hitbox.copy()
        offset_hitbox.topleft -= offset
        pygame.draw.rect(display_surface, (255, 0, 0), offset_hitbox, 1)

        offset_rect = self.rect.copy()
        offset_rect.topleft -= offset
        pygame.draw.rect(display_surface, (0, 0, 255), offset_rect, 1)

        offset_dmg_hitbox = self.dmg_hitbox.copy()
        offset_dmg_hitbox.topleft -= offset
        pygame.draw.rect(display_surface, (0, 255, 0), offset_dmg_hitbox, 1)

    
    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_animation_time >= self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1

            total_frames = self.get_num_columns()

            # 🔒 chegou no fim da animação
            if self.current_frame >= total_frames:
                if self.mode == self.attack_type:
                    self.attacking = False
                
                if self.mode == 'hurt' and self.dying:
                    self.kill()
                    return

                self.current_frame = 0  # loop normal

        self.image = self.get_frame(self.current_frame)

        if not self.vulnerable and self.health > 0:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)
    

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
            
    

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            elif attack_type == 'flame':
                self.health -= player.get_full_magic_damage()
            
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    

    def check_death(self):
        if self.health <= 0 and not self.dying:
            self.dying = True
            self.attacking = False
            self.set_mode('hurt')
            self.direction_row = 0
    

    def hit_reaction(self, player):
        if not self.vulnerable and not self.dying:
            enemy_vec = pygame.math.Vector2(self.hitbox.center)
            player_vec = pygame.math.Vector2(player.hitbox.center)
            direction = (player_vec - enemy_vec).normalize()
        
            self.direction = direction * -1

            knockback = self.direction * self.resistance * 2

            self.hitbox.x += knockback.x
            self.collision('horizontal')

            self.hitbox.y += knockback.y
            self.collision('vertical')


    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
    

    def enemy_update(self, player):
        self.hit_reaction(player)
        self.get_status(player)
        self.actions(player)
