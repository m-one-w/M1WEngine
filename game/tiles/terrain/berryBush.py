"""This module contains the BerryBush class."""
import pygame


class BerryBush(pygame.sprite.Sprite):
    """BerryBush class to hold all information for BerryBush objects."""

    # other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, pos: tuple, groups: pygame.sprite.Group):
        """Construct a BerryBush object."""
        super().__init__(groups)
        # self.sprite_type = sprite_type
        self.image = pygame.image.load("graphics/berry_bush/berryBush.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
