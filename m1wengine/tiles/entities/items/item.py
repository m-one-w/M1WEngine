"""This module contains the Item class."""
import pygame
from m1wengine.dict_structures.animation_dict import AnimationDict
from m1wengine.tiles.entities.entity import Entity
import m1wengine.settings as settings


class Item(Entity):
    """Item class.

    Base class for all Items in the game.

    Methods
    -------
    import_assets(self) -> None
        Divide the animation image into smaller parts. Calls parent's import_assets
    update(self) -> None
        Update the item's image
    """

    def __init__(
        self,
        group: pygame.sprite.Group,
        pos: tuple[int, int],
        image_path: str,
        image_rect: pygame.Rect,
    ) -> None:
        """Initialize a tile.

        Parameters
        ----------
        group: pygame.sprite.Group
            The groups this sprite is a part of
        pos: tuple[int, int]
            The starting (x, y) coordinates
        image_path: str
            The path to the item's images
        image_rect: pygame.Rect
            The size of the item
        """
        super().__init__(group, pos, image_path, image_rect)
        self._status = "idle"
        self._animation_speed = 0.05

    def import_assets(self) -> None:
        """Import and divide the animation image into it's smaller parts."""
        idle_animation: AnimationDict = {
            "name": "idle",
            "image_rect": (
                0,
                0,
                settings.ENTITY_WIDTH,
                settings.ENTITY_HEIGHT * 2,
            ),
            "image_count": 3,
        }
        self._animation_dict = [idle_animation]
        super().import_assets()

    def update(self) -> None:
        """Update the item instance."""
        self.image = self.animate()
