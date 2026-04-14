import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        spritesheet = pygame.image.load('map_assets/tiles/rock.png').convert_alpha()
        self.image = spritesheet.subsurface((0, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)