WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TILESIZE = 32

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
PROFICIENCY_BAR_WIDTH = 300
PROFICIENCY_BAR_HEIGHT = 15
ITEM_BOX_SIZE = 64
UI_FONT = 'assets/fonts/DejaVuSans.ttf'
UI_FONT_SIZE = 18

# UI colors
HEALTH_COLOR = "#c50000"
ENERGY_COLOR = "#00aac0"
PROFICIENCY_COLOR = "#360021"
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
    "spellcast": {"frames": 7, "animation_speed": {"flame": 300, "heal": 65, "fireball": 150}},
    "walk": {"frames": 9, "animation_speed": 120},
    "shoot": {"frames": 13, "animation_speed": 55},
    "thump": {"frames": 6, "animation_speed": 70}
}

# weapons
WEAPON_DATA = {
    "brass_sword": {
        "damage": 8,
        "cooldown": 300,
        "graphic": 'assets/characters/weapons/brass_sword.png'
    },
    "silver_sword": {
        "damage": 12,
        "cooldown": 700,
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
    "flame": {
        "strenght":10,
        "cost": 20,
        "cooldown": 12000,
        "start_cooldown": 1800,
        "graphic": 'assets/characters/magics/flame.png',
        "image_frame": 6,
        "image_layer": 0
    },
    "heal": {
        "strenght": 20,
        "cost": 15,
        "cooldown": 500,
        "start_cooldown": 0,
        "graphic": 'assets/characters/magics/heal.png',
        "image_frame": 3,
        "image_layer": 3
    },
    "fireball": {
        "strenght": 20,
        "cost": 10,
        "cooldown": 5000,
        "start_cooldown": 1000,
        "graphic": 'assets/characters/magics/fireball.png',
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
        'echoes': [5, 8],
        'proficiency': [5, 8],
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
        'echoes': [5, 8],
        'proficiency': [5, 8],
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
        'echoes': [12, 15],
        'proficiency': [10, 13],
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
MAP_FLOOR_CONFIG = {
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
    }
}
