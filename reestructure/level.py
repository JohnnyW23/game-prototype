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
        self.generate_buildings()
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
    

    def can_place_building(self, x, y, w, h, margin=1):
        dirt = self.map_layers["dirt"]
        house = self.map_layers.get("house_outside")

        max_y = len(dirt)
        max_x = len(dirt[0])

        for yy in range(y - margin, y + h + margin):
            for xx in range(x - margin, x + w + margin):
                if yy < 0 or yy >= max_y or xx < 0 or xx >= max_x:
                    return False

                # terreno precisa ser vazio
                if dirt[yy][xx] != -1:
                    return False

                # NÃO pode ter outra casa ali
                if house and house[yy][xx] != -1:
                    return False

        return True


    def generate_buildings(self, chance=0.1):
        import random
        from buildings import buildings

        for building in buildings.keys():
            
            model_name = random.choice(list(buildings[building].keys()))
            model = buildings[building][model_name]

            overlayed = f'{building}_overlayed'
            outside = f'{building}_outside'
            ornaments = f'{building}_ornaments'

            top_tiles = model[overlayed]
            base_tiles = model[outside]
            ornament_tiles = model[ornaments]

            h = len(base_tiles)
            w = len(base_tiles[0])

            dirt = self.map_layers["dirt"]
            map_h = len(dirt)
            map_w = len(dirt[0])

            # cria layers se não existirem
            if overlayed not in self.map_layers:
                self.map_layers[overlayed] = [[-1 for _ in range(map_w)] for _ in range(map_h)]
            if outside not in self.map_layers:
                self.map_layers[outside] = [[-1 for _ in range(map_w)] for _ in range(map_h)]
            if ornaments not in self.map_layers:
                self.map_layers[ornaments] = [[-1 for _ in range(map_w)] for _ in range(map_h)]

            top_layer = self.map_layers[overlayed]
            base_layer = self.map_layers[outside]
            ornament_layer = self.map_layers[ornaments]

            for y in range(map_h - h):
                for x in range(map_w - w):

                    if random.random() > chance:
                        continue

                    if not self.can_place_building(x, y, w, h, margin=1):
                        continue

                    # aplica estrutura
                    for yy in range(h):
                        for xx in range(w):
                            tile = top_tiles[yy][xx]
                            if tile != -1:
                                top_layer[y + yy][x + xx] = tile

                    for yy in range(h):
                        for xx in range(w):
                            tile = base_tiles[yy][xx]
                            if tile != -1:
                                base_layer[y + yy][x + xx] = tile

                    # aplica ornamentos
                    for yy in range(h):
                        for xx in range(w):
                            tile = ornament_tiles[yy][xx]
                            if tile != -1:
                                ornament_layer[y + yy][x + xx] = tile

    
    def create_map(self):
        boundary = []
        complete_row = [0 for _ in range(77)]
        border_row = [0] + [-1 for _ in range(75)] + [0]

        boundary.append(complete_row)
        for _ in range(74):
            boundary.append(border_row)
        boundary.append(complete_row)

        layouts = {
            "boundary" : boundary,
            "dirt": self.map_layers["dirt"],
            "grass": self.map_layers["grass"],
            "house_overlayed": self.map_layers["house_overlayed"], 
            "house_outside": self.map_layers["house_outside"],
            "house_ornaments": self.map_layers["house_ornaments"]
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                
                        if style == "boundary":
                            Tile((x - 32, y - 32), [self.obstacles_sprites], "invisible")

                        if style == "dirt":
                            Tile((x, y), [self.visible_sprites], "floor", self.tilesets["dirt"][col], z_offset=-1000)
                        
                        if style == "grass":
                            Tile((x, y), [self.visible_sprites], "floor", self.tilesets["grass"][col], z_offset=-1000)
                        
                        if style == "house_overlayed":
                            Tile((x, y), [self.visible_sprites], "house", self.tilesets["house"][col], z_offset=1000)
                        
                        if style == "house_outside":
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], "house", self.tilesets["house"][col])
                        
                        if style == "house_ornaments":
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], "house", self.tilesets["house"][col])
                
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
        offset_x = player.rect.centerx - self.half_width
        offset_y = player.rect.centery - self.half_height

        max_x = 75 * TILESIZE - self.display_surface.get_width()
        max_y = 75 * TILESIZE - self.display_surface.get_height()

        self.offset.x = max(0, min(offset_x, max_x))
        self.offset.y = max(0, min(offset_y, max_y))

        screen_rect = pygame.Rect(0, 0, self.display_surface.get_width(), self.display_surface.get_height())

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery + s.z_offset):
            offset_pos = sprite.rect.topleft - self.offset
            sprite_rect = pygame.Rect(offset_pos, sprite.image.get_size())

            if screen_rect.colliderect(sprite_rect):
                self.display_surface.blit(sprite.image, offset_pos)
