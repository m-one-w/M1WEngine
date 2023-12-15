"""This module contains the Entity class."""
import pygame
from tiles.tile import Tile


class Entity(Tile):
    """Entity class.

    Base class for all entities including NPC and the player.
    """

    def __init__(self, groups: pygame.sprite.Group) -> None:
        """Initialize an entity.

        Parameters
        ----------
        groups: pygame.sprite.Group
            The groups this entity is a part of
        """
        super().__init__(groups)
        # TODO: implement the rest of the entity specific logic
