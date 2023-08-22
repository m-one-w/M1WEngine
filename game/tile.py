import pygame


class Tile(pygame.sprite.Sprite):

    """Base class for all game :func:`Sprite<pygame.sprite.Sprite>`"""

    # other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, groups):
        """Initialize a tile

        Parameters
        ----------
        groups: the groups this sprite is a part of
        """
        super().__init__(groups)
        # r,g,b vals for key color
        self.colorKeyWhite = (255, 255, 255)
        self.colorKeyBlack = (0, 0, 0)

    def update(self, shiftx, shifty):
        """Update function for the sprite or sprite group

        Parameters
        ----------
        shiftx: rate at which the x position changes
        shifty: rate at which the y position changes
        """
        self.rect.x += shiftx
        self.rect.y += shifty

    def setColorKeyBlack(self):
        """Set the sprite alpha channel to ignore black backgrounds"""
        self.image.set_colorkey(self.colorKeyBlack, pygame.RLEACCEL)

    def setColorKeyWhite(self):
        """Set the sprite alpha channel to ignore white backgrounds"""
        self.image.set_colorkey(self.colorKeyWhite, pygame.RLEACCEL)


class StaticTile(Tile):
    """Cut a tileset into correct sprites"""

    def __init__(self, group, x, y, surface):
        """Initialize a static tile

        Parameters
        ----------
        size: the filepath to find the tileset
        x: the x location to render
        y: the y location to render
        surface: the :func:`Sprite<pygame.sprite.Sprite>` image to display
        """
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect


class DynamicTile(Tile):
    """Cut a tileset into correct sprites

    Parameters
    ----------
    path: the filepath to find the tileset
    """

    def __init__(self, size, x, y):
        """Initialize a dynamic tile

        Parameters
        ----------
        size: the filepath to find the tileset
        x: the x location to render
        y: the y location to render
        """
        super().__init__(size, x, y)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect
