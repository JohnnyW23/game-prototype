import pygame
from settings import *
from maps import MAPS
from tile import Tile
from player import Player
from enemy import Enemy
from hitbox import Hitbox
from ui import UI
from particles import AnimationPlayer
from magic import MagicPlayer


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack hitbox surface
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
    

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


    def escolher_modelo(self, models_dict):
        import random

        total = sum(m["chance"] for m in models_dict.values())
        r = random.uniform(0, total)

        acumulado = 0
        for nome, model in models_dict.items():
            acumulado += model["chance"]
            if r <= acumulado:
                return nome, model


    def generate_buildings(self):
        import random
        from buildings import buildings
        import uuid

        dirt = self.map_layers["dirt"]
        map_h = len(dirt)
        map_w = len(dirt[0])

        # cria layers para todos os tipos de building
        for building_data in buildings.values():
            for model_name, model in building_data.items():
                if model_name == "chance":
                    continue

                for part_name in model.keys():
                    if part_name == "chance":
                        continue

                    if part_name not in self.map_layers:
                        self.map_layers[part_name] = [
                            [-1 for _ in range(map_w)] for _ in range(map_h)
                        ]

        # percorre o mapa verticalmente
        # percorre por tipo de building (PRIORIDADE)
        for building, building_data in buildings.items():

            for y in range(map_h):
                for x in range(map_w):
                    # sorteia modelo
                    # 1. chance do building
                    if random.random() > building_data["chance"]:
                        continue

                    # 2. pega apenas modelos
                    models = {
                        name: data
                        for name, data in building_data.items()
                        if name != "chance"
                    }

                    # 3. escolhe modelo ponderado
                    model_name, model = self.escolher_modelo(models)

                    parts = {
                        name: data for name, data in model.items()
                        if name != "chance"
                    }

                    base_parts = {
                        name: data for name, data in parts.items()
                        if name.endswith("_base")
                    }

                    reference = next((p["grid"] for p in base_parts.values() if "grid" in p), None)

                    if not reference:
                        continue  # building inválido sem base

                    h = len(reference)
                    w = len(reference[0])

                    if y + h > map_h or x + w > map_w:
                        continue

                    # valida posição
                    valid = True

                    for part_name, part in base_parts.items():
                        grid = part.get("grid")
                        if not grid:
                            continue

                        for yy in range(len(grid)):
                            for xx in range(len(grid[0])):
                                if grid[yy][xx] != -1:
                                    if not self.can_place_building(x + xx, y + yy, 1, 1):
                                        valid = False
                                        break
                            if not valid:
                                break
                        if not valid:
                            break

                    if not valid:
                        continue

                    building_id = uuid.uuid4()

                    for part_name, part_data in parts.items():
                        grid = part_data.get("grid")
                        if not grid:
                            continue

                        layer = self.map_layers[part_name]

                        tileset_key = part_name.split("_")[0]  # prefixo

                        for yy in range(len(grid)):
                            for xx in range(len(grid[0])):
                                tile = grid[yy][xx]

                                if tile == -1:
                                    continue

                                # marca colisão se necessário
                                if part_name.endswith("_base"):
                                    self.building_grid[y + yy][x + xx] = True

                                if layer[y + yy][x + xx] == -1:
                                    layer[y + yy][x + xx] = []

                                layer[y + yy][x + xx].append(
                                    (tileset_key, tile, building_id, part_data)
                                )

    
    def create_map(self):
        import random
        import uuid

        self.tilesets = {
            "dirt": self.slice_tiles("map_assets/tiles/dirt.png"),
            "grass": self.slice_tiles("map_assets/tiles/grass.png"),
            "house": self.slice_tiles("map_assets/tiles/house.png"),
            "tree": self.slice_tiles("map_assets/tiles/tree.png"),
            "barrel": self.slice_tiles("map_assets/tiles/barrel.png"),
            "victorian-market": self.slice_tiles("map_assets/victorian/victorian-market.png")
        }

        self.create_floor_map()
        self.building_grid = [
            [False for _ in range(len(self.map_layers["dirt"][0]))]
            for _ in range(len(self.map_layers["dirt"]))
        ]
        self.generate_buildings()

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


        for layer_name, layer in self.map_layers.items():
            if layer_name not in layouts:
                layouts[layer_name] = layer

        
        for style, layout in layouts.items():
            if style == "boundary":
                for row_index, row in enumerate(layout):
                    for col_index, col in enumerate(row):
                        if col != -1:
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            Tile((x - 32, y - 32), [self.obstacles_sprites], "invisible")
                continue

            config = MAP_FLOOR_CONFIG.get(style)

            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell == -1:
                        continue

                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    # FLOOR
                    if config:
                        for tileset_key, tile_index, tile_id, _ in self.normalize_cell(
                            cell,
                            config["tileset"],
                            config
                        ):
                            Tile(
                                (x, y),
                                config["groups"](self),
                                config["type"],
                                tile_id,
                                self.tilesets[tileset_key][tile_index],
                                z_offset=config["z"]
                            )

                    # BUILDINGS
                    else:
                        for tileset_key, tile_index, tile_id, part_config in self.normalize_cell(cell):
                            Tile(
                                (x, y),
                                part_config["groups"](self),
                                part_config["type"],
                                tile_id,
                                self.tilesets[tileset_key][tile_index],
                                z_offset=part_config["z"]
                            )
                        
        self.player = Player(
            (
                75 * (TILESIZE / 2) - 16,
                75 * (TILESIZE / 2) - 12
            ),
            [
                self.visible_sprites
            ],
            "assets/characters/sprites",
            self.obstacles_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_magic
        )

        names = list(ENEMY_DATA.keys())
        chances_dict = {name: ENEMY_DATA[name]['spawn_chance'] for name in names}

        def escolher_chave(dicionario):
            total = sum(dicionario.values())
            r = random.uniform(0, total)
            acumulado = 0
            for chave, chance in dicionario.items():
                acumulado += chance
                if r <= acumulado:
                    return chave

        for y in range(len(self.building_grid)):
            for x in range(len(self.building_grid[0])):
                if 25 < y < 51 or 25 < x < 51:
                    continue
                if random.random() <= 0.01 and not self.building_grid[y][x]:
                    enemy_x = x * TILESIZE
                    enemy_y = y * TILESIZE
                    id = uuid.uuid4()

                    name = escolher_chave(chances_dict)

                    self.enemy = Enemy(
                        name,
                        id,
                        (enemy_x, enemy_y),
                        [self.visible_sprites, self.attackable_sprites],
                        ENEMY_DATA[name]['graphic'],
                        self.obstacles_sprites,
                        self.damage_player
                    )
    

    def normalize_cell(self, cell, default_tileset=None, default_config=None):
        if cell == -1:
            return []

        result = []

        def process(item, tile_id=None, tileset_key=None, config=None):
            if isinstance(item, tuple):
                if len(item) == 4:
                    ts, tile, tid, cfg = item
                    process(tile, tid, ts, cfg)
                elif len(item) == 3:
                    ts, tile, tid = item
                    process(tile, tid, ts, config)
                elif len(item) == 2:
                    tile, tid = item
                    process(tile, tid, tileset_key, config)
                return

            if isinstance(item, list):
                for sub in item:
                    process(sub, tile_id, tileset_key, config)
                return

            result.append((
                tileset_key or default_tileset,
                item,
                tile_id,
                config or default_config
            ))

        process(cell)
        return result


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
        self.current_attack = Hitbox(self.player, [self.visible_sprites, self.attack_sprites], size, vector_coordinates)


    def create_magic(self, style, strenght, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strenght, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


    def attack_collision(self, attack_sprite, target_sprite):
        if target_sprite.sprite_type == "enemy":
            return attack_sprite.rect.colliderect(target_sprite.dmg_hitbox)

        return attack_sprite.rect.colliderect(target_sprite.rect)


    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:

                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite,
                    self.attackable_sprites,
                    False,
                    collided=self.attack_collision
                )

                for target_sprite in collision_sprites:
                    if target_sprite.sprite_type == 'barrel':
                        target_id = getattr(target_sprite, "id", None)

                        for sprite in self.attackable_sprites.copy():
                            if getattr(sprite, "id", None) == target_id:
                                pos = target_sprite.rect.center
                                self.animation_player.create_particles(pos, 50, 0, 'dust', [self.visible_sprites])
                                sprite.kill()
                    
                    else:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)


    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles



    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
    

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
            if isinstance(sprite, Enemy):
                sprite.hitbox_debug(offset=self.offset)
            '''


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)