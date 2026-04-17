import pygame
from settings import *
from tile import Tile
from player import Player
from hitbox import Hitbox


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.tilesets = {
            "dirt": self.slice_tiles("map_assets/tiles/dirt.png"),
            "grass": self.slice_tiles("map_assets/tiles/grass.png"),
            "house": self.slice_tiles("map_assets/tiles/house.png"),
            "tree": self.slice_tiles("map_assets/tiles/tree.png")
        }

        self.create_floor_map()
        self.building_grid = [
            [False for _ in range(len(self.map_layers["dirt"][0]))]
            for _ in range(len(self.map_layers["dirt"]))
        ]
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

        max_y = len(dirt)
        max_x = len(dirt[0])

        for yy in range(y - margin, y + h + margin):
            for xx in range(x - margin, x + w + margin):
                # fora do mapa
                if yy < 0 or yy >= max_y or xx < 0 or xx >= max_x:
                    return False

                # precisa ser terreno vazio
                if dirt[yy][xx] != -1:
                    return False

                # NÃO pode existir outra construção
                if self.building_grid[yy][xx]:
                    return False

        return True


    def generate_buildings(self):
        import random
        from buildings import buildings

        for building in buildings.keys():
            print(building)

            overlayed = f'{building}_top'
            outside = f'{building}_base'
            ornaments = f'{building}_bottom'

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

            # percorre o mapa
            for y in range(map_h):
                for x in range(map_w):

                    # sorteia modelo a cada tentativa
                    model_name = random.choice(list(buildings[building].keys()))
                    model = buildings[building][model_name]
                    chance = model["chance"]

                    if random.random() > chance:
                        continue

                    model = buildings[building][model_name]

                    base_tiles = model[outside]
                    top_tiles = model[overlayed]
                    ornament_tiles = model[ornaments]

                    h = len(base_tiles)
                    w = len(base_tiles[0])

                    # checa se cabe no mapa
                    if y + h > map_h or x + w > map_w:
                        continue

                    # valida posição usando apenas as células do outside que não são -1
                    valid = True
                    for yy in range(h):
                        for xx in range(w):
                            if base_tiles[yy][xx] != -1:
                                if not self.can_place_building(x + xx, y + yy, 1, 1):
                                    valid = False
                                    break
                        if not valid:
                            break

                    if not valid:
                        continue

                    # aplica base
                    
                    for yy in range(h):
                        for xx in range(w):
                            tile = base_tiles[yy][xx]
                            if tile != -1:
                                self.building_grid[y + yy][x + xx] = True

                                if base_layer[y + yy][x + xx] == -1:
                                    base_layer[y + yy][x + xx] = []

                                if isinstance(base_layer[y + yy][x + xx], list):
                                    base_layer[y + yy][x + xx].append(tile)
                                else:
                                    base_layer[y + yy][x + xx] = [
                                        base_layer[y + yy][x + xx],
                                        tile
                                    ]


                    # aplica overlay
                    for yy in range(len(top_tiles)):
                        for xx in range(len(top_tiles[0])):
                            tile = top_tiles[yy][xx]
                            if tile != -1:
                                if top_layer[y + yy][x + xx] == -1:
                                    top_layer[y + yy][x + xx] = []
                                if isinstance(top_layer[y + yy][x + xx], list):
                                    top_layer[y + yy][x + xx].append(tile)
                                else:
                                    top_layer[y + yy][x + xx] = [top_layer[y + yy][x + xx], tile]

                    # aplica ornamentos
                    for yy in range(len(ornament_tiles)):
                        for xx in range(len(ornament_tiles[0])):
                            tile = ornament_tiles[yy][xx]
                            if tile != -1:
                                if ornament_layer[y + yy][x + xx] == -1:
                                    ornament_layer[y + yy][x + xx] = []
                                if isinstance(ornament_layer[y + yy][x + xx], list):
                                    ornament_layer[y + yy][x + xx].append(tile)
                                else:
                                    ornament_layer[y + yy][x + xx] = [ornament_layer[y + yy][x + xx], tile]

    
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
            "grass": self.map_layers["grass"]
        }
        sufixes = ["_top", "_base", "_bottom"]
        objects = ["house", "tree"]
        for object in objects:
            for sufix in sufixes:
                layouts[f'{object}{sufix}'] = self.map_layers[f'{object}{sufix}']
        
        for style, layout in layouts.items():
            if style == "boundary":
                for row_index, row in enumerate(layout):
                    for col_index, col in enumerate(row):
                        if col != -1:
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            Tile((x - 32, y - 32), [self.obstacles_sprites], "invisible")
                continue

            config = STYLE_CONFIG.get(style)
            if not config:
                continue

            tileset = self.tilesets[config["tileset"]]
            groups_fn = config["groups"]
            z = config["z"]
            sprite_type = config["type"]

            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell == -1:
                        continue

                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    for tile_index in self.normalize_cell(cell):
                        Tile(
                            (x, y),
                            groups_fn(self),
                            sprite_type,
                            tileset[tile_index],
                            z_offset=z
                        )

                        
                
        self.player = Player(
            (
                75 * (TILESIZE / 2) - 32,
                75 * (TILESIZE / 2) - 32
            ),
            [
                self.visible_sprites
            ],
            self.obstacles_sprites,
            self.create_attack,
            self.destroy_attack
        )
    

    def normalize_cell(self, cell):
        if isinstance(cell, list):
            result = []
            for item in cell:
                if isinstance(item, list):
                    result.extend(item)
                else:
                    result.append(item)
            return result
        return [cell]


    def slice_tiles(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()
        image_width, image_height = image.get_size()
        columns = image_width // 32
        rows = image_height // 32

        tilesets = []

        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(
                    col * 32,
                    row * 32,
                    32,
                    32
                )
                tile = image.subsurface(rect)
                tilesets.append(tile)
        
        return tilesets
    

    def layout_check(self, map):
        terrain_map = []
        for row in map:
            terrain_map.append(list(row))
        return terrain_map
        

    def create_attack(self, size, vector_coordinates):
        self.current_attack = Hitbox(self.player, [self.visible_sprites], size, vector_coordinates)
    

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


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
            
            '''
            if isinstance(sprite, Tile):
                if sprite.sprite_type == "tree":
                    sprite.hitbox_debug(offset=self.offset)
            '''
            