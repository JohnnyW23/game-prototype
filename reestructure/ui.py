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
        self.proficiency_bar_rect = pygame.Rect(10, 695, PROFICIENCY_BAR_WIDTH, PROFICIENCY_BAR_HEIGHT)


    def show_bar(self, current_amount, max_amount, bg_rect, color):
        radius = 1
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


    def show_text(self, text, topleft_x, topleft_y, rect_color, border_color, border_radius):
        echoes_font = pygame.font.Font(UI_FONT, 14)
        text_surf = echoes_font.render(text, False, TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (topleft_x, topleft_y))

        pygame.draw.rect(self.display_surface, rect_color, text_rect.inflate(10, 10),
                         border_top_left_radius=border_radius[0],
                         border_top_right_radius=border_radius[1],
                         border_bottom_right_radius=border_radius[2],
                         border_bottom_left_radius=border_radius[3]
                        )
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, border_color, text_rect.inflate(10, 10), 1,
                         border_top_left_radius=border_radius[0],
                         border_top_right_radius=border_radius[1],
                         border_bottom_right_radius=border_radius[2],
                         border_bottom_left_radius=border_radius[3]
                        )
    

    def selection_box(self, left, has_switched):
        y = self.display_surface.get_size()[1]
        bg_rect = pygame.Rect(left, y - ITEM_BOX_SIZE - 35, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
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
        frame = pygame.transform.scale(frame, (56, 56))
        magic_rect = frame.get_rect(center = bg_rect.center)

        self.display_surface.blit(frame, magic_rect)


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_text(f"{str(int(player.echoes))} Echoes", 15, 590, UI_BG_COLOR, UI_BORDER_COLOR, [2, 2, 2, 2])

        self.weapon_overlay(player.weapon_name, not player.can_switch_weapon)
        self.magic_overlay(player.magic_name, not player.can_switch_magic)
        
        self.show_text(f"Level {str(int(player.level))}", 163, 675, UI_BORDER_COLOR, UI_BORDER_COLOR, [2, 2, 2, 2])
        self.show_bar(player.proficiency, player.max_proficiency, self.proficiency_bar_rect, PROFICIENCY_COLOR)
