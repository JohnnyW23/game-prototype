import pygame
from settings import *
from debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, z_offset=0):
        super().__init__(groups)

        self.assets = self.create_player_assets()

        self.animation_timer = 0
        self.animation_speed = 200
        self.last_animation_time = pygame.time.get_ticks()
        self.current_frame = 0

        self.direction = pygame.math.Vector2()
        self.speed = 2
        self.attacking = False
        self.attack_cooldown = 400
        self.combat_mode_cooldown = 2500
        self.attack_time = 0

        self.double_tap_delay = 500

        self.last_press_time = {
            pygame.K_a: 0,
            pygame.K_d: 0,
            pygame.K_w: 0,
            pygame.K_s: 0
        }
        
        self.obstacle_sprites = obstacle_sprites

        self.z_offset = z_offset

        self.mode = "Idle"
        self.is_running = False
        self.run_direction = None
        self.direction_row = 3 

        self.image = self.get_frame(self.current_frame)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(
            self.rect.x,   # começa alinhado
            self.rect.y ,   # começa alinhado
            32,
            24
        )
    

    def create_player_assets(self):

        skin_color = "Ivory"
        hair_color = "Black"
        eye_color = "Green"
        torso_color = "Black"
        leg_color = "Red"
        foot_color = "Black"

        hair_style = "Short 03 - Curly"
        facial_hair_type = "Facial Hair 06 - Trimmed Beard"
        torso_type = "Shirt 02 - V-neck Longsleeve Shirt"
        leg_type = "Pants 04 - Cuffed Pants"
        foot_type = "Shoes 01 - Shoes"
        
        
        main_paths = {
            "body": f'assets/characters/body/{skin_color}/',
            "torso": f'assets/characters/torsos/{torso_type}/{torso_color}/',
            "legs": f'assets/characters/legs/{leg_type}/{leg_color}/',
            "feet": f'assets/characters/feet/{foot_type}/{foot_color}/',
            "head": f'assets/characters/heads/{skin_color}/',
            "eyes": f'assets/characters/eyes/{eye_color}/',
            "eyebrows": f'assets/characters/eyebrows/Eyebrows 01 - Thin Eyebrows/{hair_color}/',
            "hair": f'assets/characters/hairs/{hair_style}/{hair_color}/',
            # "facial_hair": f'assets/characters/facial_hair/{facial_hair_type}/{hair_color}/'
            "sword": f'assets/characters/props/Steel Sword/'
        }

        states = ["Combat 1h - Backslash", "Combat 1h - Halfslash", "Combat 1h - Idle", "Combat 1h - Slash", "Emotes", "Idle", "Jump", "Run", "Sitting", "Walk"]

        assets = {}

        for k, v in main_paths.items():
            assets[k] = {}
            for state in states:
                if k == "sword" and "Combat" not in state:
                    assets[k][state] = None
                    continue
                assets[k][state] = pygame.image.load(f'{v}{state}.png').convert_alpha()
        
        return assets


    def get_num_columns(self, sprite):
        return sprite.get_width() // (sprite.get_height() // 4)
    

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

        for asset in self.assets.keys():
            image = self.assets[asset][self.mode]
            if image is None: continue
            if asset == "sword":
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
                self.set_mode("Run")
                self.speed = 4
            else:
                self.set_mode("Walk")
                self.speed = 2
        else:
            if self.mode != "Combat 1h - Idle":
                self.set_mode("Idle")
                self.is_running = False
        
        
        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.set_mode("Combat 1h - Slash")
        
        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.set_mode("Combat 1h - Halfslash")

        if keys[pygame.K_l] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.set_mode("Combat 1h - Backslash")
            
    

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
        if mode == "Combat 1h - Idle":
            self.animation_speed = 300
        elif mode == "Idle":
            self.animation_speed = 200
        elif mode == "Run":
            self.animation_speed = 70
        elif mode == "Walk":
            self.animation_speed = 120
        elif mode == "Combat 1h - Slash":
            self.animation_speed = 40
        elif mode == "Combat 1h - Halfslash":
            self.animation_speed = 40
        elif mode == "Combat 1h - Backslash":
            self.animation_speed = 40
        
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
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.set_mode("Combat 1h - Idle")
        
        if self.mode == "Combat 1h - Idle":
            if current_time - self.attack_time >= self.combat_mode_cooldown:
                self.set_mode("Idle")
    

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

            total_frames = self.get_num_columns(
                self.assets["head"][self.mode]
            )

            if "Combat" in self.mode:
                if self.current_frame >= total_frames:
                    self.current_frame = 0
                    self.attacking = False
                    # quando terminar o ataque, entra em Combat Idle
                    self.set_mode("Combat 1h - Idle")
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

        
