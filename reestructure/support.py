import pygame
import os

def get_all_sprites(path):

	sprites = os.listdir(path)
	sprite_dict = {}
	for sprite in sprites:
		sprite_dict[sprite[:-4]] = pygame.image.load(f'{path}/{sprite}')

	return sprite_dict
