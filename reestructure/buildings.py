buildings = {
    "house": {
        "chance": 0.05,
        "model1": {
            "chance": 0.4,
            "house_top": {
                "grid": [
                    [27, 39, 40, 41, 29],
                    [36, 48, 49, 50, 38],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 1000,
                "type": "house"
            },
            "house_base": {
                "grid": [
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [45, 46, 46, 46, 47],
                    [[0, 63], [1, 21], [1, 65],  1,  2],
                    [[9, 72], 5, [10, 74], [10, 8], 11],
                    [[18, 81], [4, 14], [19, 83], [19, 17], 20],
                    [-1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "house"
            },
            "house_bottom": {
                "grid": [
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, 13, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "house"
            }
        },
        "model2": {
            "chance": 0.35,
            "house_top": {
                "grid": [
                    [27, 39, 40, 40, 40, 41, 29],
                    [36, 48, 49, 49, 49, 50, 38],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 1000,
                "type": "house"
            },
            "house_base": {
                "grid": [
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [45, 46, 46, 46, 46, 46, 47],
                    [ 0,  1, [1, 63],  [1, 21],  [1, 65],  1,  2],
                    [ 9, [10,  8], [10, 72],  5, [10, 74], [10,  8], 11],
                    [ 18, [19, 17], [19, 81], [4, 14], [19, 83], [19, 17], 20],
                    [-1, -1, -1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "house"
            },
            "house_bottom": {
                "grid": [
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, 13, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "house"
            }
        },
        "model3": {
            "chance": 0.25,
            "house_top": {
                "grid": [
                    [27, 39, 40, 40, 40, 40, [41, 6], 29],
                    [36, 48, 49, 49, 49, 58, [59, 15], 38],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 1000,
                "type": "house"
            },
            "house_base": {
                "grid": [
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [45, 46, 46, 46, 54, 48, 50, 38],
                    [ 0,  1,  1,  1, 45, 46, 46, 47],
                    [ 9, [10, 8], [10, 25], [10, 26], [10, 0, 63], [1, 21], [1, 65],  2],
                    [18, [19, 17], [19, 34], [19, 35], [19, 9, 72],  3, [10, 25, 74], [11, 26]],
                    [-1, -1, -1, -1, [18, 81], [12, 4], [19, 34, 83], [20, 35]],
                    [-1, -1, -1, -1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "house"
            },
            "house_bottom": {
                "grid": [
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, 13, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "house"
            },
            "barrel_base": {
                "grid": [
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1,  0, -1, -1, -1, -1],
                    [-1, -1, -1,  4, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                "z": 0,
                "type": "barrel"
            }
        }
    },
    "market": {
        "chance": 0.1,
        "model1": {
            "chance": 1,
            "victorian-market_top": {
                "grid": [
                    [   544,        545,       546,         547,     -1,       -1,            -1,        -1],
                    [   560,        561,       562,         563,     -1,      364,           365,       366],
                    [[904, 576], [905, 577], [803, 578], [804, 579], -1,      380,           381,       382],
                    [    84,         -1,        -1,          87,     -1, [84, 396, 752], [753, 397], [87, 398]],
                    [   285,         -1,        -1,          286,    -1,       -1,            -1,        -1],
                    [    -1,         -1,        -1,          -1,     -1,       -1,            -1,        -1],
                    [    -1,         -1,        -1,          -1,     -1,       -1,            -1,        -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 1000,
                "type": "victorian-market"
            },
            "victorian-market_base": {
                "grid": [
                    [      -1,           -1,      -1,     -1,         -1,       -1,          -1,            -1,],
                    [      -1,           -1,      -1,     -1,         -1,       -1,          -1,            -1,],
                    [      84,           -1,      -1,     87,         -1,       84,          -1,            87,],
                    [     920,          921,     819,    820,         -1,       -1,          -1,            -1,],
                    [[84, 960, 877], [961, 885], 961, [87, 962, 886], -1, [84, 763, 768], [764, 769], [87, 963, 875]],
                    [  [976, 301],      977,     977,  [978, 302],    -1,       -1,          -1,        [995, 1050]],
                    [      -1,           -1,      -1,     -1,         -1,       -1,          -1,          1011]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "victorian-market"
            }
        }
    },
    "tree": {
        "chance": 0.05,
        "model1": {
            "chance": 0.25,
            "tree_top": {
                "grid": [
                    [18, 19, 20],
                    [24, 25, 26],
                    [30, [46, 31], 32],
                    [-1, -1, -1],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 500,
                "type": "tree"
            },
            "tree_base": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, 52, -1],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "tree"
            },
            "tree_bottom": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [51, -1, 53],
                    [57, 58, 59]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "tree"
            },
        },
        "model2": {
            "chance": 0.25,
            "tree_top": {
                "grid": [
                    [21, 22, 23],
                    [27, 28, 29],
                    [33, 34, 35],
                    [39, 40, 41],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 500,
                "type": "tree"
            },
            "tree_base": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, 52, -1],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "tree"
            },
            "tree_bottom": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [51, -1, 53],
                    [57, 58, 59]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "tree"
            },
        },
        "model3": {
            "chance": 0.25,
            "tree_top": {
                "grid": [
                    [ 0,  1,  2],
                    [ 6,  7,  8],
                    [12, 13, 14],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 500,
                "type": "tree"
            },
            "tree_base": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, 49, -1],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "tree"
            },
            "tree_bottom": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [48, -1, 50],
                    [54, 55, 56]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "tree"
            },
        },
        "model4": {
            "chance": 0.25,
            "tree_top": {
                "grid": [
                    [ 3,  4,  5],
                    [ 9, 10, 11],
                    [15, [43, 16], 17],
                    [-1, -1, -1],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": 500,
                "type": "tree"
            },
            "tree_base": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, 49, -1],
                    [-1, -1, -1]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites],
                "z": 0,
                "type": "tree"
            },
            "tree_bottom": {
                "grid": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [48, -1, 50],
                    [54, 55, 56]
                ],
                "groups": lambda self: [self.visible_sprites],
                "z": -1000,
                "type": "tree"
            }
        }
    },
    "barrel": {
        "chance": 0.05,
        "model1": {
            "chance": 1,
            "barrel_top": {
                "grid": [
                    [ 1],
                    [-1]
                ],
                "groups": lambda self: [self.visible_sprites, self.attackable_sprites],
                "z": 250,
                "type": "barrel"
            },
            "barrel_base": {
                "grid": [
                    [-1],
                    [ 5]
                ],
                "groups": lambda self: [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                "z": 0,
                "type": "barrel"
            }
        }
    }
}