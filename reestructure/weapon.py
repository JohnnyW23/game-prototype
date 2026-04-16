import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.direction_row

        self.image = pygame.Surface((34, 36))
        if direction == 3:
            self.rect = self.image.get_rect(midleft = player.rect.midright - pygame.math.Vector2(44, -12))
        elif direction == 0:
            self.rect = self.image.get_rect(top = player.rect.bottom)
        elif direction == 1:
            self.rect = self.image.get_rect(right = player.rect.left)
        else:
            self.rect = self.image.get_rect(bottom = player.rect.top)
        self.z_offset = 0