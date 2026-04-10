import pygame

class TileSet:
    def __init__(self, image_path, tile_size):
        self.tile_size = tile_size
        self.image = pygame.image.load(image_path).convert_alpha()

        self.tiles = []
        self._slice_tiles()

    def _slice_tiles(self):
        image_width, image_height = self.image.get_size()
        columns = image_width // self.tile_size
        rows = image_height // self.tile_size

        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(
                    col * self.tile_size,
                    row * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                tile = self.image.subsurface(rect)
                self.tiles.append(tile)