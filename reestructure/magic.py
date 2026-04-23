import pygame
from settings import *


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
    

    def heal(self, player, strenght, cost, groups):
        max_health = player.stats['health']
        player.health += strenght
        player.energy -= cost
        if player.health > max_health:
            player.health = max_health
        
        self.animation_player.create_particles(player.dmg_hitbox.center, 50, 3, 'heal', groups)


    def flame(self, player, cost, groups):
        from random import randint

        player.energy -= cost

        if player.direction_row == 0: direction = pygame.math.Vector2(0, -1)
        elif player.direction_row == 1: direction = pygame.math.Vector2(-1, 0)
        elif player.direction_row == 2: direction = pygame.math.Vector2(0, 1)
        else: direction = pygame.math.Vector2(1, 0)

        for i in range(1, 6):
            if direction.x: # horizontal
                offset_x = (direction.x * i) * TILESIZE
                x = player.dmg_hitbox.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.dmg_hitbox.centery + randint(-TILESIZE // 3, TILESIZE // 3)
            else: # vertical
                offset_y = (direction.y * i) * TILESIZE
                x = player.dmg_hitbox.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.dmg_hitbox.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
            
            self.animation_player.create_particles((x, y), 120, 0, 'flame', groups, 'flame')
    

    def fireball(self, player, cost, groups, obstacles_sprites, attackable_sprites):

        player.energy -= cost

        if player.direction_row == 0: direction = pygame.math.Vector2(0, -1)
        elif player.direction_row == 1: direction = pygame.math.Vector2(-1, 0)
        elif player.direction_row == 2: direction = pygame.math.Vector2(0, 1)
        else: direction = pygame.math.Vector2(1, 0)

        if direction.x: # horizontal
            offset_x = direction.x * TILESIZE
            x = player.dmg_hitbox.centerx + offset_x
            y = player.dmg_hitbox.centery
        else: # vertical
            offset_y = direction.y * TILESIZE
            x = player.dmg_hitbox.centerx
            y = player.dmg_hitbox.centery + offset_y
        
        damage = MAGIC_DATA['fireball']['strenght']

        self.animation_player.create_projectile((x, y), 'fireball', damage, 8, direction, player.direction_row, 50, groups, obstacles_sprites, attackable_sprites, 'fireball')