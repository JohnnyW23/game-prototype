import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 35, ENERGY_BAR_WIDTH, BAR_HEIGHT)


    def show_bar(self, current_amount, max_amount, bg_rect, color):
        radius = 10
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect, border_radius=radius)

        #converting stat to pixel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect, border_radius=radius)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2, border_radius=radius)


    def show_exp(self, exp):
        exp_font = pygame.font.Font(UI_FONT, 14)
        text_surf = exp_font.render(f'{str(int(exp))} XP', False, TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (13, 68))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10), border_radius = 10)
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 1, border_radius = 10)
    

    def selection_box(self, left, has_switched):
        y = self.display_surface.get_size()[1]
        bg_rect = pygame.Rect(left, y - ITEM_BOX_SIZE - 10, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 2)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2)

        return bg_rect
    

    def weapon_overlay(self, weapon_name, has_switched):
        bg_rect = self.selection_box(10, has_switched)
        weapon_surf = pygame.image.load(WEAPON_DATA[weapon_name]['graphic'])
        weapon_surf = pygame.transform.scale(weapon_surf, (48, 48))
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)
    

    def magic_overlay(self, magic_name, has_switched):
        bg_rect = self.selection_box(20 + ITEM_BOX_SIZE, has_switched)
        frame_index = MAGIC_DATA[magic_name]['image_frame']
        magic_level = MAGIC_DATA[magic_name]['image_layer']
        sprite_rect = pygame.Rect(
            frame_index * 64,
            magic_level * 64,
            64,
            64
        )
        magic_surf = pygame.image.load(MAGIC_DATA[magic_name]['graphic'])
        frame = magic_surf.subsurface(sprite_rect)
        magic_rect = frame.get_rect(center = bg_rect.center)

        self.display_surface.blit(frame, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_name, not player.can_switch_weapon)
        self.magic_overlay(player.magic_name, not player.can_switch_magic)
