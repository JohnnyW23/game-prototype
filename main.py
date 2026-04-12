import pygame


class Game:
    def __init__(self):
        from character import generate_character
        from tileset import TileSet
        from map_models.maps import maps

        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.TILE_SIZE = 32

        self.maps = {
            "chunk1": maps["chunk_1"]["model_1"],
            "chunk2": maps["chunk_2"]["model_1"],
            "chunk3": maps["chunk_3"]["model_1"],
            "chunk4": maps["chunk_4"]["model_1"],
            "chunk5": maps["chunk_5"]["model_1"],
            "chunk6": maps["chunk_6"]["model_1"]
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
        bottom = concat_horizontal(["chunk4", "chunk5", "chunk6"])

        # agora une verticalmente top + bottom
        self.map_layers = {}

        for part in [top, bottom]:
            for k, v in part.items():
                if k not in self.map_layers:
                    self.map_layers[k] = []
                self.map_layers[k].extend(v)
            
        self.generate_grass_from_dirt()

        self.randomizar_tiles(self.map_layers)

        self.tilesets = {
            "grass": TileSet("map_assets/tiles/grass.png", self.TILE_SIZE),
            "dirt": TileSet("map_assets/tiles/dirt.png", self.TILE_SIZE)
        }

        self.map_width = 75 * self.TILE_SIZE
        self.map_height = 50 * self.TILE_SIZE

        self.camera_x = 0
        self.camera_y = 0

        self.last_press_time = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_UP: 0,
            pygame.K_DOWN: 0
        }

        self.double_tap_delay = 200

        self.character = generate_character()

        self.character.is_running = False
        self.character.run_direction = None

        self.running = True

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
    

    
    def randomizar_tiles(self, map_layers, chance=0.3):
        import random

        for layer_name, layer in map_layers.items():
            for y, row in enumerate(layer):
                for x, value in enumerate(row):
                    if value == 10 and random.random() < chance:
                        if layer_name == "grass":
                            layer[y][x] = random.randint(15, 17)
                        else:
                            layer[y][x] = random.randint(16, 17)


    def draw_map(self, tile_type):

        tileset = self.tilesets[tile_type]

        for row_index, row in enumerate(self.map_layers[tile_type]):
            for col_index, tile_index in enumerate(row):

                if tile_index < 0:
                    continue

                tile = tileset.tiles[tile_index]

                x = col_index * self.TILE_SIZE - self.camera_x
                y = row_index * self.TILE_SIZE - self.camera_y

                # só desenha o que aparece na tela (performance)
                if -32 < x < 800 and -32 < y < 600:
                    self.screen.blit(tile, (x, y))
    

    def draw_maps(self):
        for tile_type in self.map_layers.keys():
            self.draw_map(tile_type)
    

    def map_row(self, mode, length, value):
        import random

        if mode == "random":
            return [random.randint(*value) for _ in range(length)]
        
        elif mode == "fixed":
            return [value] * length
        
        elif mode == "mixed":
            return [random.choice(value) for _ in range(length)]

    def run(self):
        while self.running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    now = pygame.time.get_ticks()

                    if event.key in self.last_press_time:
                        if now - self.last_press_time[event.key] <= self.double_tap_delay:

                            # ativa corrida
                            self.character.is_running = True
                            self.character.run_direction = event.key

                    self.last_press_time[event.key] = now

            keys = pygame.key.get_pressed()

            moving = False

            speed = 75  # walk

            dx = 0
            dy = 0

            speed = 75
            if self.character.is_running:
                speed = 200

            if keys[pygame.K_LEFT]:
                dx -= 1
                self.character.direction_row = 1

            if keys[pygame.K_RIGHT]:
                dx += 1
                self.character.direction_row = 3

            if keys[pygame.K_UP]:
                dy -= 1
                self.character.direction_row = 0

            if keys[pygame.K_DOWN]:
                dy += 1
                self.character.direction_row = 2
            
            if dx != 0 or dy != 0:
                length = (dx ** 2 + dy ** 2) ** 0.5
                dx /= length
                dy /= length

                self.character.x += dx * speed * dt / 1000
                self.character.y += dy * speed * dt / 1000

                half = 32

                self.character.x = max(half - 12, min(self.character.x, self.map_width - half + 12))
                self.character.y = max(half - 10, min(self.character.y, self.map_height - half))

                moving = True
            else:
                moving = False
            
            if self.character.is_running:
                if not keys[self.character.run_direction]:
                    self.character.is_running = False

            if moving:
                if self.character.is_running:
                    self.character.set_mode("Run")
                else:
                    self.character.set_mode("Walk")
            else:
                self.character.is_running = False
                self.character.set_mode("Idle")

            self.character.update(dt)

            # centraliza no player
            self.camera_x = self.character.x - self.screen.get_width() // 2
            self.camera_y = self.character.y - self.screen.get_height() // 2

            # trava nas bordas do mapa
            self.camera_x = max(0, min(self.camera_x, self.map_width - self.screen.get_width()))
            self.camera_y = max(0, min(self.camera_y, self.map_height - self.screen.get_height()))

            # desenhar
            self.screen.fill((0, 0, 0))
            self.draw_maps()

            # mecanica da camera
            screen_x = self.character.x - self.camera_x - 32
            screen_y = self.character.y - self.camera_y - 32

            self.character.draw(self.screen, (screen_x, screen_y))

            pygame.display.flip()


game = Game()
game.run()