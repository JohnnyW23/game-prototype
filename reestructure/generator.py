import pygame


class FloorTiles:
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


class FloorGenerator:
    def __init__(self):
        from settings import MAPS

        pygame.init()
        pygame.display.set_mode((800, 600))

        self.TILE_SIZE = 32

        self.maps = {
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
                for k, v in self.maps[chunk].items():
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
            
        self.generate_grass_from_dirt()
        self.randomizar_tiles(self.map_layers)

        self.tilesets = {
            "dirt": FloorTiles("map_assets/tiles/dirt.png", self.TILE_SIZE),
            "grass": FloorTiles("map_assets/tiles/grass.png", self.TILE_SIZE)
        }

        self.map_width = 75 * self.TILE_SIZE
        self.map_height = 75 * self.TILE_SIZE


    def get_tile(self, grid, x, y):
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
            return 10
        return grid[y][x]


    def generate_grass_from_dirt(self):
        dirt = self.map_layers["dirt"]
        height = len(dirt)
        width = len(dirt[0])

        grass = [[-1 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):

                top = self.get_tile(dirt, x, y - 1)
                bottom = self.get_tile(dirt, x, y + 1)
                left = self.get_tile(dirt, x - 1, y)
                right = self.get_tile(dirt, x + 1, y)

                tl = self.get_tile(dirt, x - 1, y - 1)
                tr = self.get_tile(dirt, x + 1, y - 1)
                bl = self.get_tile(dirt, x - 1, y + 1)
                br = self.get_tile(dirt, x + 1, y + 1)

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


    def randomizar_tiles(self, map_layers, chance=0.15):
        import random

        for layer_name, layer in map_layers.items():
            for y, row in enumerate(layer):
                for x, value in enumerate(row):
                    if value == 10 and random.random() < chance:
                        if layer_name == "grass":
                            layer[y][x] = random.randint(15, 17)
                        else:
                            layer[y][x] = random.randint(16, 17)
    

    def save_generated_map(self, filename="map_floor.png"):
        # cria superfície do tamanho do mapa
        surface = pygame.Surface((self.map_width, self.map_height))

        # desenha todas as camadas
        for layer in ["dirt", "grass"]:
          if layer in self.map_layers:
            tileset = self.tilesets[layer]
            for row_index, row in enumerate(self.map_layers[layer]):
              for col_index, tile_index in enumerate(row):
                if tile_index == -1:
                  continue
                tile = tileset.tiles[tile_index]
                x = col_index * self.TILE_SIZE
                y = row_index * self.TILE_SIZE
                surface.blit(tile, (x, y))

        # salva em arquivo
        pygame.image.save(surface, filename)

        return filename