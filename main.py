import pygame


class Game:
    def __init__(self):
        from character import generate_character
        from tileset import TileSet
        from reestructure.maps import maps

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
            "chunk6": maps["chunk_6"]["model_1"],
            "chunk7": maps["chunk_7"]["model_1"],
            "chunk8": maps["chunk_8"]["model_1"],
            "chunk9": maps["chunk_9"]["model_1"],
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
        self.generate_buildings()
        self.generate_collision_layer()

        self.tilesets = {
            "dirt": TileSet("map_assets/tiles/dirt.png", self.TILE_SIZE),
            "grass": TileSet("map_assets/tiles/grass.png", self.TILE_SIZE),
            "house_outside": TileSet("map_assets/tiles/house.png", self.TILE_SIZE),
            "house_ornaments": TileSet("map_assets/tiles/house.png", self.TILE_SIZE)
        }

        self.map_width = 75 * self.TILE_SIZE
        self.map_height = 75 * self.TILE_SIZE

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


    
    def generate_buildings(self, chance=0.20):
        import random
        from reestructure.buildings import buildings

        model = buildings["house"]["model1"]

        base_tiles = model["house_outside"]
        ornament_tiles = model["house_ornaments"]

        h = len(base_tiles)
        w = len(base_tiles[0])

        dirt = self.map_layers["dirt"]
        map_h = len(dirt)
        map_w = len(dirt[0])

        # cria layers se não existirem
        if "house_outside" not in self.map_layers:
            self.map_layers["house_outside"] = [[-1 for _ in range(map_w)] for _ in range(map_h)]
        if "house_ornaments" not in self.map_layers:
            self.map_layers["house_ornaments"] = [[-1 for _ in range(map_w)] for _ in range(map_h)]

        house_layer = self.map_layers["house_outside"]
        ornament_layer = self.map_layers["house_ornaments"]

        for y in range(map_h - h):
            for x in range(map_w - w):

                if random.random() > chance:
                    continue

                if not self.can_place_building(x, y, w, h, margin=1):
                    continue

                # aplica estrutura
                for yy in range(h):
                    for xx in range(w):
                        tile = base_tiles[yy][xx]
                        if tile != -1:
                            house_layer[y + yy][x + xx] = tile

                # aplica ornamentos
                for yy in range(h):
                    for xx in range(w):
                        tile = ornament_tiles[yy][xx]
                        if tile != -1:
                            ornament_layer[y + yy][x + xx] = tile

    

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
    

    def generate_collision_layer(self):
        height = len(self.map_layers["dirt"])
        width = len(self.map_layers["dirt"][0])

        collision = [[False for _ in range(width)] for _ in range(height)]

        # casas bloqueiam
        if "house_outside" in self.map_layers:
            for y, row in enumerate(self.map_layers["house_outside"]):
                for x, tile in enumerate(row):
                    if tile != -1:
                        collision[y][x] = True

        self.map_layers["collision"] = collision


    def is_colliding(self, px, py):
        FOOT_Y_OFFSET = 28        # onde fica o pé no sprite
        FOOT_HALF_WIDTH = 10     # metade da largura REAL do pé

        foot_y = py + FOOT_Y_OFFSET

        # três pontos: esquerda, centro, direita
        points = [
            (px - FOOT_HALF_WIDTH, foot_y),
            (px, foot_y),
            (px + FOOT_HALF_WIDTH, foot_y),
        ]

        for point_x, point_y in points:
            tx = int(point_x // self.TILE_SIZE)
            ty = int(point_y // self.TILE_SIZE)

            if (
                ty < 0 or ty >= len(self.map_layers["collision"]) or
                tx < 0 or tx >= len(self.map_layers["collision"][0])
            ):
                return True

            if self.map_layers["collision"][ty][tx]:
                return True

        return False


    def draw_house_ornaments_with_depth(self):
        FOOT_Y_OFFSET = 28
        player_foot_y = self.character.y + FOOT_Y_OFFSET

        tileset = self.tilesets["house_ornaments"]

        for row, row_tiles in enumerate(self.map_layers["house_ornaments"]):
            tile_world_y = row * self.TILE_SIZE

            for col, tile_index in enumerate(row_tiles):
                if tile_index == -1:
                    continue

                x = col * self.TILE_SIZE - self.camera_x
                y = tile_world_y - self.camera_y

                # se o pé do personagem está ACIMA do ornamento → ornamento na frente
                if player_foot_y < tile_world_y:
                    self.screen.blit(tileset.tiles[tile_index], (x, y))



    def draw_map(self, tile_type):
        tileset = self.tilesets[tile_type]

        for row_index, row in enumerate(self.map_layers[tile_type]):
            for col_index, tile_index in enumerate(row):

                if tile_index < 0:
                    continue

                tile = tileset.tiles[tile_index]

                x = col_index * self.TILE_SIZE - self.camera_x
                y = row_index * self.TILE_SIZE - self.camera_y

                # desenha só o que está na tela
                if -32 < x < self.screen.get_width() and -32 < y < self.screen.get_height():
                    self.screen.blit(tile, (x, y))


    def draw_maps(self):
        for layer in ["dirt", "grass", "house_outside"]:
            if layer in self.map_layers:
                self.draw_map(layer)

    
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

                new_x = self.character.x + dx * speed * dt / 1000
                new_y = self.character.y + dy * speed * dt / 1000

                # testa X
                if not self.is_colliding(new_x, self.character.y):
                    self.character.x = new_x

                # testa Y
                if not self.is_colliding(self.character.x, new_y):
                    self.character.y = new_y


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

            # mecanica da camera
            screen_x = self.character.x - self.camera_x - 32
            screen_y = self.character.y - self.camera_y - 32

            self.draw_maps()
            self.character.draw(self.screen, (screen_x, screen_y))
            self.draw_house_ornaments_with_depth()

            pygame.display.flip()


game = Game()
game.run()
