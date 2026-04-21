import pygame
from entity import Entity
from settings import *
from debug import debug

class Player(Entity):
    def __init__(self, pos, groups, path, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(pos, groups, path, z_offset=0)
        
        # map interaction
        self.obstacle_sprites = obstacle_sprites

        # attacking data
        self.attacking = False
        self.attack_type = 'slash'
        self.combat_mode_cooldown = 2500
        self.attack_time = {
            'slash': -400,
            'halfslash': -200,
            'backslash': -1500,
            'shoot': -800,
            'fireball': -5000,
            'heal': -500
        }
        self.attack_cooldown = {
            'slash': 400,
            'halfslash': 200,
            'backslash': 1500,
            'shoot': 800,
            'fireball': 5000,
            'heal': 500
        }

        # weapon data
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapons = {
            "sword": ["brass_sword", "silver_sword"],
            "bow": ["normal_bow"]
        }
        self.selected_weapon_type = "sword"
        self.weapon_index = 0
        self.weapon_name = self.weapons[self.selected_weapon_type][self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None

        # magic
        self.create_magic = create_magic
        # self.destroy_magic = destroy_magic
        self.magic_index = 0
        self.magic_name = list(MAGIC_DATA.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # player mode
        self.mode = f"idle_{self.weapon_name}"

        # switch cooldown
        self.switch_duration_cooldown = 200

        # run system
        self.is_running = False
        self.run_direction = None
        self.double_tap_delay = 200
        self.last_press_time = {
            pygame.K_a: 0,
            pygame.K_d: 0,
            pygame.K_w: 0,
            pygame.K_s: 0
        }

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
        self.exp = 0

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # player hitbox
        self.hitbox = pygame.Rect(
            self.rect.x,
            self.rect.y,
            32,
            24
        )
        self.dmg_hitbox = pygame.Rect(
                                self.rect.x,
                                self.rect.y,
                                32,
                                52
                            )
        
        self.rect.bottom = self.hitbox.bottom + 32
        self.rect.right = self.hitbox.right  + 48
        self.dmg_hitbox.bottom = self.hitbox.bottom
        self.dmg_hitbox.right = self.hitbox.right


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
                self.set_mode(f"walk_{self.weapon_name}")
                self.speed = 2
        else:
            if self.mode != f"combat_{self.weapon_name}":
                self.set_mode(f"idle_{self.weapon_name}")
                self.is_running = False
        
        multiplier = 1
        
        if self.selected_weapon_type == "sword":
            if keys[pygame.K_j] and self.can_use('slash', pygame.time.get_ticks()):
                self.attacking = True
                self.attack_type = "slash"
                self.attack_time[self.attack_type] = pygame.time.get_ticks()
                self.attack_start = 30
                self.attack_triggered = True
                self.set_mode(f"slash_{self.weapon_name}")
                
            
            elif keys[pygame.K_k] and self.can_use('halfslash', pygame.time.get_ticks()):
                self.attacking = True
                self.attack_type = "halfslash"
                self.attack_time[self.attack_type] = pygame.time.get_ticks()
                self.attack_start = 30
                self.attack_triggered = True
                self.set_mode(f"halfslash_{self.weapon_name}")

                multiplier -= 0.2


            elif keys[pygame.K_l] and self.can_use('backslash', pygame.time.get_ticks()):
                self.attacking = True
                self.attack_type = "backslash"
                self.attack_time[self.attack_type] = pygame.time.get_ticks()
                self.attack_start = 30
                self.attack_triggered = True
                self.set_mode(f"backslash_{self.weapon_name}")

                multiplier += 0.2

        
        elif self.selected_weapon_type == "bow" and self.can_use('shoot', pygame.time.get_ticks()):
            if keys[pygame.K_j] or keys[pygame.K_k] or keys[pygame.K_l]:
                self.attacking = True
                self.attack_type = "shoot"
                self.attack_time[self.attack_type] = pygame.time.get_ticks()
                self.attack_start = 0
                self.attack_triggered = True
                self.set_mode(f"shoot_{self.weapon_name}")
        
        self.damage_point = WEAPON_DATA[self.weapon_name]['damage'] * multiplier
        
        if keys[pygame.K_i] and self.can_use(self.magic_name, pygame.time.get_ticks()):
            self.attacking = True
            self.attack_type = self.magic_name
            self.attack_time[self.attack_type] = pygame.time.get_ticks()
            self.attack_start = 0
            self.attack_triggered = True
            self.set_mode('spellcast')
            style = list(MAGIC_DATA.keys())[self.magic_index]
            strenght = MAGIC_DATA[style]['strenght'] + self.stats['magic']
            cost = MAGIC_DATA[style]['cost']

            self.create_magic(style, strenght, cost)
        
            self.spell_point = MAGIC_DATA[self.magic_name]['strenght']


        if keys[pygame.K_h] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            if len(self.weapons[self.selected_weapon_type]) - 1 == self.weapon_index:
                self.weapon_index = 0
            else:
                self.weapon_index += 1
            
            self.weapon_name = self.weapons[self.selected_weapon_type][self.weapon_index]
        
        if keys[pygame.K_u] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index = 0
            if self.selected_weapon_type == "sword":
                self.selected_weapon_type = "bow"
            else:
                self.selected_weapon_type = "sword"
        
            self.weapon_name = self.weapons[self.selected_weapon_type][self.weapon_index]

        if keys[pygame.K_o] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            if self.magic_index < len(list(MAGIC_DATA.keys())) - 1:
                self.magic_index += 1
            else:
                self.magic_index = 0
            
            self.magic_name = list(MAGIC_DATA.keys())[self.magic_index]
    

    def can_use(self, attack_type, current_time):
        if attack_type in MAGIC_DATA:
            cd = MAGIC_DATA[attack_type]['cooldown']
            if attack_type == 'heal':
                max_health = self.stats['health']
                if self.energy < MAGIC_DATA['heal']['cost'] or self.health == max_health:
                    return False
                
        else:
            cd = self.attack_cooldown[attack_type] + WEAPON_DATA[self.weapon_name]['cooldown']

        return current_time - self.attack_time[attack_type] >= cd


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
    

    def set_mode(self, mode):
        if "_" in mode: key = mode[:mode.find("_")]
        else: key = mode

        if key == 'spellcast':
            self.animation_speed = MODES[key]['animation_speed'][self.magic_name]
            
        else:
            self.animation_speed = MODES[key]['animation_speed']

        if mode != self.mode:
            self.current_frame = 0
            self.last_animation_time = pygame.time.get_ticks()

        self.mode = mode
    

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        # ===== COOLDOWN DE ATAQUE =====
        if self.attacking and self.attack_type not in ['shoot'] + list(MAGIC_DATA.keys()):
            attack_data =  ATTACK_TYPES_DATA[self.attack_type]
            attack_start = attack_data["start"]

            if current_time - self.attack_time[self.attack_type] >= attack_start and self.attack_triggered:
                self.create_attack(
                    attack_data["size"],
                    attack_data["vector_coordinates"]
                )
                self.attack_triggered = False
            

        if self.mode == f"combat_{self.weapon_name}":
            if current_time - self.attack_time[self.attack_type] >= self.combat_mode_cooldown:
                self.set_mode(f"idle_{self.weapon_name}")

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
    

    def handle_running(self, event):
        current_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:
            if event.key in self.last_press_time:
                delta = current_time - self.last_press_time[event.key]

                if delta <= self.double_tap_delay:
                    self.is_running = True
                    self.run_direction = event.key

            self.last_press_time[event.key] = current_time


    def hitbox_debug(self, offset):
        display_surface = pygame.display.get_surface()

        offset_hitbox = self.hitbox.copy()
        offset_hitbox.topleft -= offset
        pygame.draw.rect(display_surface, (255, 0, 0), offset_hitbox, 1)

        offset_rect = self.rect.copy()
        offset_rect.topleft -= offset
        pygame.draw.rect(display_surface, (0, 0, 255), offset_rect, 1)

        offset_dmg_hitbox = self.dmg_hitbox
        offset_dmg_hitbox.topleft -= offset
        pygame.draw.rect(display_surface, (0, 255, 0), offset_dmg_hitbox, 1)
    

    def animate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_animation_time >= self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1

            total_frames = self.get_num_columns()

            if self.attack_type in self.mode or "spellcast" in self.mode:
                if self.current_frame >= total_frames:
                    self.current_frame = 0
                    self.attacking = False
                    self.destroy_attack()
                    # quando terminar o ataque, entra em Combat Idle
                    self.set_mode(f"combat_{self.weapon_name}")
            else:
                self.current_frame %= total_frames

        self.image = self.get_frame(self.current_frame)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    

    def get_full_weapon_damage(self):
        from math import ceil
        base_damage = self.attack
        weapon_damage = ceil(self.damage_point)

        return base_damage + weapon_damage


    def update(self):
        self.cooldowns()
        self.input()
        self.move(self.speed)
        self.animate()
