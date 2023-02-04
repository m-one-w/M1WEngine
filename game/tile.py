#Sean Nishi
#Lunk Game
#12/22/2022

import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    #other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        #filter+adjust images that are taller than 64 pixels to prevent overlapping
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        #self.image = pygame.image.load('graphics/floor_tile/tile.png').convert_alpha()
        self.hitbox = self.rect.inflate(0,-10)