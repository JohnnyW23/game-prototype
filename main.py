import pygame


class Game:
    def __init__(self):
        from character import generate_character
        from tileset import TileSet

        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.TILE_SIZE = 32

        self.map_layers = {
            "dirt": [
                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 10, 10, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            ],
            "grass": [
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10,  1, 13, 13, 13, 13, 13, 13, 13, 13, 13,  2, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [13, 13, 13, 13, 13, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [ 7,  7,  7,  7,  7,  8, -1, -1,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
                [10, 10, 10, 10, 10, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [10, 10, 10, 10, 10, 11, -1, -1,  6,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 11, -1, -1,  9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
            ]
        }

        self.randomizar_tiles(self.map_layers)

        self.tilesets = {
            "grass": TileSet("map_assets/tiles/grass.png", self.TILE_SIZE),
            "dirt": TileSet("map_assets/tiles/dirt.png", self.TILE_SIZE)
        }

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
    

    
    def randomizar_tiles(self, map_layers, chance=0.1):
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
                x = col_index * self.TILE_SIZE
                y = row_index * self.TILE_SIZE

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

            # desenhar
            self.screen.fill((0, 0, 0))
            self.draw_maps()
            self.character.draw(self.screen, (self.character.x, self.character.y))

            pygame.display.flip()


game = Game()
game.run()