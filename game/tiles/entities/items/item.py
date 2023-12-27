"""This module contains the Item class."""
import pygame
from dict_structures.animation_dict import AnimationDict
from tiles.entities.entity import Entity
import settings


class Item(Entity):
    """Item class.

    Base class for all Items in the game.

    Attributes
    ----------
    _sprite_sheet: SpriteSheet
        Contain sprite image information
    _status: str
        Contain current status
    _animation_speed: float
        Contain current animation speed
    """

    def __init__(
        self,
        group: pygame.sprite.Group,
        pos: tuple,
        image_path: str,
        image_rect: pygame.Rect,
    ):
        """Initialize a tile.

        Parameters
        ----------
        group: pygame.sprite.Group
            The groups this sprite is a part of
        """
        super().__init__(group, pos, image_path, image_rect)
        self._status: str = "idle"
        self._animation_speed: float = 0.05

    def import_assets(self):
        """Import and divide the animation image into it's smaller parts.

        Called at end of :func:'init()', takes the image with all character animations
        and divides it into its sub-images. Can be expanded with more images to fulfill
        idle and attack animations.
        """
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
        self._animation_dict: list[AnimationDict] = [idle_animation]
        super().import_assets()

    def update(self):
        """Update the item instance."""
        self.image = self.animate()
