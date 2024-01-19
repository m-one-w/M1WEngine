"""This module Crystal Item class."""
import pygame
from tiles.entities.items.item import Item
import settings


class Crystal(Item):
    """Crystal class.

    Class for all Crystal Items in the game.

    Methods
    -------
    collisions_handler(self)
        Handle collisions with the item and entities
    """

    def __init__(self, group: pygame.sprite.Group, pos: tuple):
        """Initialize a tile.

        Parameters
        ----------
        group: pygame.sprite.Group
            The group this sprite is a part of
        pos: tuple
            The current item position
        """
        crystal_image_path: str = settings.ITEM_IMAGES + "crystal.png"
        image_rect: pygame.Rect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT * 2
        )
        super().__init__(group, pos, crystal_image_path, image_rect)

    def collision_handler(self):
        """Handle collisions on the item instance."""
        # TODO: implement item collision handler
        pass
