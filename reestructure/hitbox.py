import pygame


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, player, groups, size, vector_coordinates):
        super().__init__(groups)
        direction = player.direction_row
        self.image = pygame.Surface(size)
        if direction == 0:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop - pygame.math.Vector2(vector_coordinates[0]))
        elif direction == 1:
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(vector_coordinates[1]))
        elif direction == 2:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(vector_coordinates[2]))
        elif direction == 3:
            self.rect = self.image.get_rect(midleft = player.rect.midright - pygame.math.Vector2(vector_coordinates[3]))

        self.z_offset = 0