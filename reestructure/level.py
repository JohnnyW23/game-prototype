import pygame
from settings import *
from tile import Tile
from player import Player
from generator import FloorGenerator


class Level:
    def __init__(self):
        

        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.tilesets = {
            "dirt": self.slice_tiles("map_assets/tiles/dirt.png"),
            "grass": self.slice_tiles("map_assets/tiles/grass.png"),
            "house": self.slice_tiles("map_assets/tiles/house.png")
        }

        self.create_floor_map()
        self.create_map()
    

    def create_floor_map(self):
        import random
        
        maps = {
            "chunk1": MAPS["chunk_1"]["model_1"],
            "chunk2": MAPS["chunk_2"]["model_1"],
            "chunk3": MAPS["chunk_3"]["model_1"],
            "chunk4": MAPS["chunk_4"]["model_1"],
            "chunk5": MAPS["chunk_5"]["model_1"],
            "chunk6": MAPS["chunk_6"]["model_1"],
            "chunk7": MAPS["chunk_7"]["model_1"],
            "chunk8": MAPS["chunk_8"]["model_1"],
            "chunk9": MAPS["chunk_9"]["model_1"],
        }

        def concat_horizontal(chunks):
            result = {}
            for chunk in chunks:
                for k, v in maps[chunk].items():
                    if k not in result:
                        result[k] = [[] for _ in range(len(v))]
                    for i, row in enumerate(v):
                        result[k][i].extend(row)
            return result

        # junta horizontalmente 1-2-3 e 4-5-6
        top = concat_horizontal(["chunk1", "chunk2", "chunk3"])
        middle = concat_horizontal(["chunk4", "chunk5", "chunk6"])
        bottom = concat_horizontal(["chunk7", "chunk8", "chunk9"])

        # agora une verticalmente top + bottom
        self.map_layers = {}

        for part in [top, middle, bottom]:
            for k, v in part.items():
                if k not in self.map_layers:
                    self.map_layers[k] = []
                self.map_layers[k].extend(v)

        dirt = self.map_layers["dirt"]
        height = len(dirt)
        width = len(dirt[0])

        grass = [[-1 for _ in range(width)] for _ in range(height)]

        def get_tile(grid, x, y):
            if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
                return 10
            return grid[y][x]

        for y in range(height):
            for x in range(width):

                top = get_tile(dirt, x, y - 1)
                bottom = get_tile(dirt, x, y + 1)
                left = get_tile(dirt, x - 1, y)
                right = get_tile(dirt, x + 1, y)

                tl = get_tile(dirt, x - 1, y - 1)
                tr = get_tile(dirt, x + 1, y - 1)
                bl = get_tile(dirt, x - 1, y + 1)
                br = get_tile(dirt, x + 1, y + 1)

                if dirt[y][x] != 10:
                    grass[y][x] = 10
                    continue

                tile = -1

                # ───── BORDAS ─────
                if top == -1:
                    tile = 13  # borda superior

                elif bottom == -1:
                    tile = 7  # borda inferior

                elif left == -1:
                    tile = 11  # borda esquerda

                elif right == -1:
                    tile = 9  # borda direita

                # ───── CANTOS ─────
                if top == -1 and left == -1:
                    tile = 1  # canto sup esquerdo

                elif top == -1 and right == -1:
                    tile = 2  # canto sup direito

                elif bottom == -1 and left == -1:
                    tile = 4  # canto inf esquerdo

                elif bottom == -1 and right == -1:
                    tile = 5  # canto inf direito
                
                # ───── CANTOS INTERNOS (detalhe fino) ─────
                if top == 10 and left == 10 and tl == -1:
                    tile = 14  # canto interno sup esquerdo

                elif top == 10 and right == 10 and tr == -1:
                    tile = 12  # canto interno sup direito

                elif bottom == 10 and left == 10 and bl == -1:
                    tile = 8  # canto interno inf esquerdo

                elif bottom == 10 and right == 10 and br == -1:
                    tile = 6  # canto interno inf direito

                grass[y][x] = tile

        self.map_layers["grass"] = grass

        for layer_name, layer in self.map_layers.items():
            for y, row in enumerate(layer):
                for x, value in enumerate(row):
                    if value == 10 and random.random() < 0.1:
                        if layer_name == "grass":
                            layer[y][x] = random.randint(15, 17)
                        else:
                            layer[y][x] = random.randint(16, 17)

    
    def create_map(self):
        boundary = []
        complete_row = [0 for _ in range(75)]
        border_row = [0] + [-1 for _ in range(73)] + [0]

        boundary.append(complete_row)
        for _ in range(73):
            boundary.append(border_row)
        boundary.append(complete_row)

        layouts = {
            "boundary" : boundary,
            "dirt": self.map_layers["dirt"],
            "grass": self.map_layers["grass"]
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                
                        if style == "boundary":
                            Tile((x, y), [self.obstacles_sprites], "invisible")

                        if style == "dirt":
                            Tile((x, y), [self.visible_sprites], "floor", self.tilesets["dirt"][col], z_offset=-1000)
                        
                        if style == "grass":
                            Tile((x, y), [self.visible_sprites], "floor", self.tilesets["grass"][col],  z_offset=-1000)
                
        self.player = Player((75 * 16 - 32, 75 * 16 - 32), [self.visible_sprites], self.obstacles_sprites)


    def slice_tiles(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()
        image_width, image_height = image.get_size()
        columns = image_width // TILESIZE
        rows = image_height // TILESIZE

        tilesets = []

        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(
                    col * TILESIZE,
                    row * TILESIZE,
                    TILESIZE,
                    TILESIZE
                )
                tile = image.subsurface(rect)
                tilesets.append(tile)
        
        return tilesets
    

    def layout_check(self, map):
        terrain_map = []
        for row in map:
            terrain_map.append(list(row))
        return terrain_map
        

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
    

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery + sprite.z_offset):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
