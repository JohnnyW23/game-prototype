import pygame
from settings import *
from debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, z_offset=0):
        super().__init__(groups)
        
        # map interaction
        self.obstacle_sprites = obstacle_sprites
        self.z_offset = z_offset

        # loads all sprites for player
        self.all_sprites = self.get_all_sprites()

        # animation
        self.animation_timer = 0
        self.animation_speed = 600
        self.last_animation_time = pygame.time.get_ticks()
        self.current_frame = 0
        self.direction = pygame.math.Vector2()
        self.is_running = False
        self.run_direction = None
        self.direction_row = 3 

        # attacking data
        self.attacking = False
        self.attack_type = None
        self.attack_start = 30
        self.attack_cooldown = 350
        self.combat_mode_cooldown = 2500
        self.attack_time = 0
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # weapon data
        self.weapons = {
            "sword": ["brass_sword", "silver_sword"],
            "bow": ["normal_bow"]
        }
        self.selected_weapon_type = "sword"
        self.weapon_index = 0
        self.weapon = self.weapons[self.selected_weapon_type][self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # run system
        self.double_tap_delay = 200
        self.last_press_time = {
            pygame.K_a: 0,
            pygame.K_d: 0,
            pygame.K_w: 0,
            pygame.K_s: 0
        }

        # player mode
        self.mode = f"idle_{self.weapon}"

        # player surface creation
        self.image = self.get_frame(self.current_frame)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(
            self.rect.x,   # começa alinhado
            self.rect.y ,   # começa alinhado
            32,
            24
        )

        # player stats
        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 2
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.attack = self.stats['attack']
        self.magic = self.stats['magic']
        self.speed = self.stats['speed']
        self.exp = 123


    def get_all_sprites(self):
        import os

        path = "assets/characters/sprites"
        sprites = os.listdir(path)
        sprite_dict = {}
        for sprite in sprites:
            sprite_dict[sprite[:-4]] = pygame.image.load(f'{path}/{sprite}')

        return sprite_dict
    

    def get_num_columns(self):
        mode = self.mode
        if "_" in mode: key = mode[:mode.find("_")]
        else: key = mode
        return PLAYER_FRAMES[key]
    

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


    def input(self):
        if self.attacking:
            self.direction.x, self.direction.y = 0, 0
            if self.is_running:
                self.is_running = False
            return
        
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.direction_row = 0
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.direction_row = 2

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.direction_row = 1
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.direction_row = 3

        if self.direction.length_squared() > 0:
            if self.is_running:
                self.set_mode(f"run")
                self.speed = 4
            else:
                self.set_mode(f"walk_{self.weapon}")
                self.speed = 2
        else:
            if self.mode != f"combat_{self.weapon}":
                self.set_mode(f"idle_{self.weapon}")
                self.is_running = False
        
        if self.selected_weapon_type == "sword":
            if keys[pygame.K_j]:
                self.attacking = True
                self.attack_type = "slash"
                self.attack_time = pygame.time.get_ticks()
                self.attack_cooldown = 350
                self.attack_start = 30
                self.attack_triggered = True
                self.set_mode(f"slash_{self.weapon}")
                
            
            if keys[pygame.K_k]:
                self.attacking = True
                self.attack_type = "halfslash"
                self.attack_time = pygame.time.get_ticks()
                self.attack_cooldown = 475
                self.attack_start = 30
                self.attack_triggered = True
                self.set_mode(f"halfslash_{self.weapon}")


            if keys[pygame.K_l]:
                self.attacking = True
                self.attack_type = "backslash"
                self.attack_time = pygame.time.get_ticks()
                self.attack_cooldown = 800
                self.attack_start = 30
                self.attack_triggered = True
                self.set_mode(f"backslash_{self.weapon}")

        
        if self.selected_weapon_type == "bow":
            if keys[pygame.K_j] or keys[pygame.K_k] or keys[pygame.K_l]:
                self.attacking = True
                self.attack_type = "shoot"
                self.attack_time = pygame.time.get_ticks()
                self.attack_cooldown = 600
                self.attack_start = 0
                self.attack_triggered = True
                self.set_mode(f"shoot_{self.weapon}")


        if keys[pygame.K_o] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            if len(self.weapons[self.selected_weapon_type]) - 1 == self.weapon_index:
                self.weapon_index = 0
            else:
                self.weapon_index += 1
            
            self.weapon = self.weapons[self.selected_weapon_type][self.weapon_index]
        
        if keys[pygame.K_u] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index = 0
            if self.selected_weapon_type == "sword":
                self.selected_weapon_type = "bow"
            else:
                self.selected_weapon_type = "sword"
        
            self.weapon = self.weapons[self.selected_weapon_type][self.weapon_index]
            
    

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.bottom = self.hitbox.bottom + 32
        self.rect.right = self.hitbox.right  + 48
    

    def set_mode(self, mode):
        if mode == f"idle_{self.weapon}":
            self.animation_speed = 600
        elif mode == "run":
            self.animation_speed = 70
        elif mode == f"walk_{self.weapon}":
            self.animation_speed = 120
        elif mode == f"combat_{self.weapon}":
            self.animation_speed = 300
        elif mode == f"slash_{self.weapon}":
            self.animation_speed = 55
        elif mode == f"halfslash_{self.weapon}":
            self.animation_speed = 65
        elif mode == f"backslash_{self.weapon}":
            self.animation_speed = 60
        elif mode == f"shoot_{self.weapon}":
            self.animation_speed = 50
        
        if mode != self.mode:
            self.current_frame = 0
            self.last_animation_time = pygame.time.get_ticks()

        self.mode = mode


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
    

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        # ===== COOLDOWN DE ATAQUE =====
        if self.attacking:
            attack_data =  ATTACK_TYPES_DATA[self.attack_type]
            attack_start = attack_data["start"]
            if current_time - self.attack_time >= attack_start and self.attack_triggered and self.selected_weapon_type == "sword":
                self.create_attack(
                    attack_data["size"],
                    attack_data["vector_coordinates"]
                )
                self.attack_triggered = False

            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
                self.last_attack_time = current_time
                self.set_mode(f"combat_{self.weapon}")


        if self.mode == f"combat_{self.weapon}":
            if current_time - self.attack_time >= self.combat_mode_cooldown:
                self.set_mode(f"idle_{self.weapon}")
        

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
    

    def handle_running(self, event):
        current_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:
            if event.key in self.last_press_time:
                delta = current_time - self.last_press_time[event.key]

                if delta <= self.double_tap_delay:
                    self.is_running = True
                    self.run_direction = event.key

            self.last_press_time[event.key] = current_time

    
    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_animation_time >= self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1

            total_frames = self.get_num_columns()

            if "slash" in self.mode:
                if self.current_frame >= total_frames:
                    self.current_frame = 0
                    self.attacking = False
                    self.destroy_attack()
                    # quando terminar o ataque, entra em Combat Idle
                    self.set_mode(f"combat_{self.weapon}")
            else:
                self.current_frame %= total_frames

        self.image = self.get_frame(self.current_frame)
    
    def hitbox_debug(self, offset):
        display_surface = pygame.display.get_surface()
        offset_hitbox = self.hitbox.copy()
        offset_hitbox.topleft -= offset
        pygame.draw.rect(display_surface, (255, 0, 0), offset_hitbox, 1)

        offset_rect = self.rect.copy()
        offset_rect.topleft -= offset
        pygame.draw.rect(display_surface, (0, 0, 255), offset_rect, 1)


    def update(self):
        self.cooldowns()
        self.input()
        self.move(self.speed)
        self.animate()
        debug(self.attacking, y=50)