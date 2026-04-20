WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TILESIZE = 32

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
ITEM_BOX_SIZE = 64
UI_FONT = 'assets/fonts/DejaVuSans.ttf'
UI_FONT_SIZE = 18

# UI colors
HEALTH_COLOR = "#c50000"
ENERGY_COLOR = "#00aac0"
UI_BORDER_COLOR_ACTIVE = 'gold'

# general colors
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = "#eeeeee"

# frames for each of player modes
HUMAN_FRAMES = {
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
    "spellcast": 7,
    "walk": 9,
    "shoot": 13,
    "thump": 6
}

# weapons
WEAPON_DATA = {
    "brass_sword": {
        "damage": 8,
        "cooldown": 100,
        "graphic": 'assets/characters/weapons/brass_sword.png'
    },
    "silver_sword": {
        "damage": 10,
        "cooldown": 300,
        "graphic": 'assets/characters/weapons/silver_sword.png'
    },
    "normal_bow": {
        "damage": 5,
        "cooldown": 300,
        "graphic": 'assets/characters/weapons/normal_bow.png'
    }
}

# magic
MAGIC_DATA = {
    "flame": {
        "strenght": 8,
        "cost": 20,
        "cooldown": 1500,
        "graphic": 'assets/characters/magics/flame.png',
        "image_frame": 6,
        "image_layer": 0
    },
    "heal": {
        "strenght": 8,
        "cost": 20,
        "cooldown": 500,
        "graphic": 'assets/characters/magics/heal.png',
        "image_frame": 3,
        "image_layer": 3
    }
}

# hitboxes for attacks
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
    },
    "shoot": {
        "start": 0,
        "size": None,
        "vector_coordinates": None
    },
    "magic": {
        "start": 0,
        "size": None,
        "vector_coordinates": None
    }
}

# enemy
ENEMY_DATA = {
    'zombie1': {
        'health': 100,
        'exp': 10,
        'damage': 10,
        'attack_type': 'thump',
        'attack_sound': 'assets/audio/attack/thump.mp3',
        'graphic': 'assets/enemies/zombie1',
        'speed': 2,
        'resistance': 3,
        'attack_cooldown': 400,
        'attack_radius': 40,
        'notice_radius': 360
    },
    'zombie2': {
        'health': 100,
        'exp': 10,
        'damage': 10,
        'attack_type': 'thump',
        'attack_sound': 'assets/audio/attack/thump.mp3',
        'graphic': 'assets/enemies/zombie2',
        'speed': 2,
        'resistance': 3,
        'attack_cooldown': 400,
        'attack_radius': 40,
        'notice_radius': 360
    }
}

# map tiles settings
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
        "z": -1000,
        "type": "house",
    },
    "tree_top": {
        "tileset": "tree",
        "groups": lambda self: [self.visible_sprites],
        "z": 1000,
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
        "z": -1000,
        "type": "tree",
    },
    "barrel_top": {
        "tileset": "barrel",
        "groups": lambda self: [self.visible_sprites, self.attackable_sprites],
        "z": 500,
        "type": "barrel",
    },
    "barrel_base": {
        "tileset": "barrel",
        "groups": lambda self: [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
        "z": 0,
        "type": "barrel",
    },
    "barrel_bottom": {
        "tileset": "barrel",
        "groups": lambda self: [self.visible_sprites, self.attackable_sprites],
        "z": -1000,
        "type": "barrel",
    }
}
