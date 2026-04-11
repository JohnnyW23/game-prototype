import os
from random import choice
import pygame


class Character:
    def __init__(self, head, body, hair, eyes, eyebrowns, facial_hair, torso, legs, feet):
        self.parts = [body, head, hair, eyes, eyebrowns, facial_hair, torso, legs, feet]

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150
        self.mode = "Idle"
        self.direction_row = 3  # 0=cima, 1=esquerda, 2=baixo, 3=direita
        self.walking = True


        self.x, self.y = 400, 368
        self.speed = 100  # pixels por segundo

    def get_num_columns(self, sprite):
        return sprite.get_width() // (sprite.get_height() // 4)

    def get_frame(self, frame_index):
        frame_height = 64
        frame_width = 64

        rect = pygame.Rect(
            frame_index * frame_width,
            self.direction_row * frame_height,
            frame_width,
            frame_height
        )

        composed = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        for part in self.parts:
            if part is None:
                continue
            img = part[self.mode]
            frame = img.subsurface(rect)
            composed.blit(frame, (0, 0))

        return composed

    def update(self, dt):

        # animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % self.get_num_columns(self.parts[0][self.mode])

    def draw(self, surface, pos):
        frame = self.get_frame(self.current_frame)
        surface.blit(frame, pos)
    
    def set_mode(self, mode):
        if mode == "Idle":
            self.animation_speed = 300
        elif mode == "Run":
            self.animation_speed = 70
        elif mode == "Walk":
            self.animation_speed = 100
        
        if mode != self.mode:
            self.current_frame = 0

        self.mode = mode        


def generate_head(skin_color):
    return {
        "Name": "Head",
        "Idle": pygame.image.load(f'assets/characters/heads/{skin_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/heads/{skin_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/heads/{skin_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/heads/{skin_color}/Walk.png').convert_alpha()
    }


def generate_body(skin_color):
    return {
        "Name": "Body",
        "Idle": pygame.image.load(f'assets/characters/body/{skin_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/body/{skin_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/body/{skin_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/body/{skin_color}/Walk.png').convert_alpha(),
    }


def generate_hair(hair_color):
    hair_styles = [f for f in os.listdir('assets/characters/hairs') if os.path.isdir(os.path.join('assets/characters/hairs', f))]
    hair_style = choice(hair_styles)
    return {
        "Name": "Hair",
        "Idle": pygame.image.load(f'assets/characters/hairs/{hair_style}/{hair_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/hairs/{hair_style}/{hair_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/hairs/{hair_style}/{hair_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/hairs/{hair_style}/{hair_color}/Walk.png').convert_alpha()
    }

def generate_eyes():
    eye_colors = [f for f in os.listdir('assets/characters/eyes') if os.path.isdir(os.path.join('assets/characters/eyes', f))]
    eye_color = choice(eye_colors)
    return {
        "Name": "Eyes",
        "Idle": pygame.image.load(f'assets/characters/eyes/{eye_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/eyes/{eye_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/eyes/{eye_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/eyes/{eye_color}/Walk.png').convert_alpha()
    }


def generate_eyebrowns(hair_color):
    eyebrown_types = [f for f in os.listdir('assets/characters/eyebrowns') if os.path.isdir(os.path.join('assets/characters/eyebrowns', f))]
    eyebrown_type = choice(eyebrown_types)
    return {
        "Name": "Eyebrowns",
        "Idle": pygame.image.load(f'assets/characters/eyebrowns/{eyebrown_type}/{hair_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/eyebrowns/{eyebrown_type}/{hair_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/eyebrowns/{eyebrown_type}/{hair_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/eyebrowns/{eyebrown_type}/{hair_color}/Walk.png').convert_alpha()
    }


def generate_facial_hair(hair_color):
    from random import randint
    if randint(1, 5) < 4:
        return None
    facial_hair_types = [f for f in os.listdir('assets/characters/facial_hair') if os.path.isdir(os.path.join('assets/characters/facial_hair', f))]
    facial_hair_type = choice(facial_hair_types)
    return {
        "Name": "Facial Hair",
        "Idle": pygame.image.load(f'assets/characters/facial_hair/{facial_hair_type}/{hair_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/facial_hair/{facial_hair_type}/{hair_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/facial_hair/{facial_hair_type}/{hair_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/facial_hair/{facial_hair_type}/{hair_color}/Walk.png').convert_alpha()
    }


def generate_torso():
    torso_types = [f for f in os.listdir('assets/characters/torsos') if os.path.isdir(os.path.join('assets/characters/torsos', f))]
    torso_type = choice(torso_types)
    torso_colors = [f for f in os.listdir(f'assets/characters/torsos/{torso_type}') if os.path.isdir(os.path.join('assets/characters/torsos', torso_type, f))]
    torso_color = choice(torso_colors)
    return {
        "Name": "Torso",
        "Idle": pygame.image.load(f'assets/characters/torsos/{torso_type}/{torso_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/torsos/{torso_type}/{torso_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/torsos/{torso_type}/{torso_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/torsos/{torso_type}/{torso_color}/Walk.png').convert_alpha()
    }


def generate_legs():
    leg_types = [f for f in os.listdir('assets/characters/legs') if os.path.isdir(os.path.join('assets/characters/legs', f))]
    leg_type = choice(leg_types)
    leg_colors = [f for f in os.listdir(f'assets/characters/legs/{leg_type}') if os.path.isdir(os.path.join('assets/characters/legs', leg_type, f))]
    leg_color = choice(leg_colors)
    return {
        "Name": "Legs",
        "Idle": pygame.image.load(f'assets/characters/legs/{leg_type}/{leg_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/legs/{leg_type}/{leg_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/legs/{leg_type}/{leg_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/legs/{leg_type}/{leg_color}/Walk.png').convert_alpha()
    }


def generate_feet():
    foot_types = [f for f in os.listdir('assets/characters/feet') if os.path.isdir(os.path.join('assets/characters/feet', f))]
    foot_type = choice(foot_types)
    foot_colors = [f for f in os.listdir(f'assets/characters/feet/{foot_type}') if os.path.isdir(os.path.join('assets/characters/feet', foot_type, f))]
    foot_color = choice(foot_colors)
    return {
        "Name": "Feet",
        "Idle": pygame.image.load(f'assets/characters/feet/{foot_type}/{foot_color}/Idle.png').convert_alpha(),
        "Run": pygame.image.load(f'assets/characters/feet/{foot_type}/{foot_color}/Run.png').convert_alpha(),
        "Emotes": pygame.image.load(f'assets/characters/feet/{foot_type}/{foot_color}/Emotes.png').convert_alpha(),
        "Walk": pygame.image.load(f'assets/characters/feet/{foot_type}/{foot_color}/Walk.png').convert_alpha()
    }


def generate_character():
    skin_color = choice(os.listdir('assets/characters/heads'))
    hair_color = choice([f for f in os.listdir('assets/characters/hairs/Short 01 - Buzzcut') if os.path.isdir(os.path.join('assets/characters/hairs/Short 01 - Buzzcut', f))])
    head = generate_head(skin_color)
    body = generate_body(skin_color)
    hair = generate_hair(hair_color)
    eyes = generate_eyes()
    eyebrowns = generate_eyebrowns(hair_color)
    facial_hair = generate_facial_hair(hair_color)
    torso = generate_torso()
    legs = generate_legs()
    feet = generate_feet()

    return Character(head, body, hair, eyes, eyebrowns, facial_hair, torso, legs, feet)