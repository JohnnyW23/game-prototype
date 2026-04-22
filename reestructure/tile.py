import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        id=None,
        surface=pygame.Surface((TILESIZE, TILESIZE)),
        z_offset=0,
        base_y=None
    ):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.id = id
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(0, -10)

        self.z_offset = z_offset

        self.base_y = base_y if base_y is not None else self.rect.centery


    def hitbox_debug(self, offset):
        display_surface = pygame.display.get_surface()
        offset_hitbox = self.hitbox.copy()
        offset_hitbox.topleft -= offset
        pygame.draw.rect(display_surface, (255, 0, 0), offset_hitbox, 1)
