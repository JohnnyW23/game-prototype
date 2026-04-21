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
MODES = {
    "backslash": {"frames": 13, "animation_speed": 60},
    "climb": {"frames": 6, "animation_speed": 70},
    "combat": {"frames": 2, "animation_speed": 300},
    "emote": {"frames": 3, "animation_speed": 40},
    "halfslash": {"frames": 6, "animation_speed": 65},
    "hurt": {"frames": 6, "animation_speed": 150},
    "idle": {"frames": 2, "animation_speed": 500},
    "jump": {"frames": 5, "animation_speed": 60},
    "run": {"frames": 8, "animation_speed": 70},
    "sit": {"frames": 1, "animation_speed": 1},
    "slash": {"frames": 5, "animation_speed": 55},
    "spellcast": {"frames": 7, "animation_speed": {"fireball": 300, "heal": 65}},
    "walk": {"frames": 9, "animation_speed": 120},
    "shoot": {"frames": 13, "animation_speed": 55},
    "thump": {"frames": 6, "animation_speed": 70}
}

# weapons
WEAPON_DATA = {
    "brass_sword": {
        "damage": 8,
        "cooldown": 200,
        "graphic": 'assets/characters/weapons/brass_sword.png'
    },
    "silver_sword": {
        "damage": 12,
        "cooldown": 500,
        "graphic": 'assets/characters/weapons/silver_sword.png'
    },
    "normal_bow": {
        "damage": 5,
        "cooldown": 400,
        "graphic": 'assets/characters/weapons/normal_bow.png'
    }
}

# magic
MAGIC_DATA = {
    "fireball": {
        "strenght": 8,
        "cost": 20,
        "cooldown": 5000,
        "graphic": 'assets/characters/magics/fireball.png',
        "image_frame": 6,
        "image_layer": 3
    },
    "heal": {
        "strenght": 8,
        "cost": 15,
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
    }
}

# enemy
ENEMY_DATA = {
    'zombie1': {
        'spawn_chance': 0.4,
        'health': 100,
        'exp': 10,
        'damage': 10,
        'attack_type': 'thump',
        'attack_sound': 'assets/audio/attack/thump.mp3',
        'graphic': 'assets/enemies/zombie1',
        'speed': 2,
        'resistance': 3,
        'attack_cooldown': 1000,
        'attack_radius': 35,
        'notice_radius': 360
    },
    'zombie2': {
        'spawn_chance': 0.4,
        'health': 100,
        'exp': 10,
        'damage': 10,
        'attack_type': 'thump',
        'attack_sound': 'assets/audio/attack/thump.mp3',
        'graphic': 'assets/enemies/zombie2',
        'speed': 2,
        'resistance': 3,
        'attack_cooldown': 1000,
        'attack_radius': 35,
        'notice_radius': 360
    },
    'zombie_iron_sword': {
        'spawn_chance': 0.2,
        'health': 150,
        'exp': 15,
        'damage': 15,
        'attack_type': 'slash',
        'attack_sound': 'assets/audio/attack/slash.mp3',
        'graphic': 'assets/enemies/zombie_iron_sword',
        'speed': 2.5,
        'resistance': 2.5,
        'attack_cooldown': 1500,
        'attack_radius': 40,
        'notice_radius': 260
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
        "z": -1000,
        "type": "tree",
    },
    "barrel_top": {
        "tileset": "barrel",
        "groups": lambda self: [self.visible_sprites, self.attackable_sprites],
        "z": 250,
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
