WIDTH    = 800
HEIGHT   = 600
FPS      = 60
TILESIZE = 32

PLAYER_FRAMES = {
    "backslash": 13,
    "climb": 6,
    "combat": 2,
    "emote": 3,
    "halfslash": 6,
    "hurt": 6,
    "idle": 2,
    "jump": 5,
    "run": 8,
    "sit": 1,
    "slash": 5,
    "speelcast": 7,
    "walk": 9
}

WEAPON_DATA = {
    "brass_sword": {
        "base_damage": 8
    },
    "silver_sword": {
        "base_damage": 10
    }
}

ATTACK_TYPES_DATA = {
    "slash": {
        "start": 120,
        "size": (33, 36),
        "vector_coordinates": [(0, -52), (44, 12), (0, -44), (44, -12)]
    },
    "halfslash": {
        "start": 140,
        "size": (33, 36),
        "vector_coordinates": [(0, -52), (34, 12), (0, -44), (34, -12)]
    },
    "backslash": {
        "start": 140,
        "size": (33, 36),
        "vector_coordinates": [(0, -52), (44, 12), (0, -44), (44, -12)]
    }
}

STYLE_CONFIG = {
    "dirt": {
        "tileset": "dirt",
        "groups": lambda self: [self.visible_sprites],
        "z": -1000,
        "type": "floor",
    },
    "grass": {
        "tileset": "grass",
        "groups": lambda self: [self.visible_sprites],
        "z": -1000,
        "type": "floor",
    },
    "house_top": {
        "tileset": "house",
        "groups": lambda self: [self.visible_sprites],
        "z": 1000,
        "type": "house",
    },
    "house_base": {
        "tileset": "house",
        "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
        "z": 0,
        "type": "house",
    },
    "house_bottom": {
        "tileset": "house",
        "groups": lambda self: [self.visible_sprites],
        "z": -500,
        "type": "house",
    },
    "tree_top": {
        "tileset": "tree",
        "groups": lambda self: [self.visible_sprites],
        "z": 500,
        "type": "tree",
    },
    "tree_base": {
        "tileset": "tree",
        "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
        "z": 0,
        "type": "tree",
    },
    "tree_bottom": {
        "tileset": "tree",
        "groups": lambda self: [self.visible_sprites],
        "z": -500,
        "type": "tree",
    }
}
