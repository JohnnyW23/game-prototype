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


    def fireball(self):
        pass