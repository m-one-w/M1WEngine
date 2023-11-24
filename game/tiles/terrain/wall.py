"""This module contains the Wall class."""
import pygame


class Wall(pygame.sprite.Sprite):
    """Wall class to hold all information for wall objects."""

    # other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, pos: tuple, groups: pygame.sprite.Group):
        """Construct the wall class.

        This method will instantiate all information for a wall object.
        """
        super().__init__(groups)
        # self.sprite_type = sprite_type
        self.image = pygame.image.load("graphics/wall/wall.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
