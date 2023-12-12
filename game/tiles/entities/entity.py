"""This module contains the Entity class."""
import pygame
from dict_structures.animation_dict import AnimationDict
from file_managers.sprite_sheet import SpriteSheet
from tiles.tile import Tile


class Entity(Tile):
    """Entity class.

    Base class for all entities including NPC and the player.

    Attributes
    ----------
    _frame_index: int
        The currently shown frame represented by an index
    _animation_speed: int
        The speed at which animations run

    Methods
    -------
    animate(self)
        Animation loop for character
    import_assets(self, animation_dict: list[AnimationDict])
        Import sprite animations
    """

    def __init__(
        self,
        group: pygame.sprite.Group,
        pos: tuple,
        sprite_sheet_path: str,
        image_rect: pygame.Rect,
    ):
        """Initialize a tile.

        Parameters
        ----------
        group: pygame.sprite.Group
            The group this sprite is a part of
        pos: tuple
            The (x, y) position the entity spawns at
        sprite_sheet_path: str
            The filepath where the sprite sheet is stored
        image_rect: pygame.Rect
            The rectangle representing the entity
        """
        super().__init__(group)
        self._frame_index: int = 0
        self._animation_speed: float = 0.15
        self._animations: dict = {}

        self._sprite_sheet: SpriteSheet = SpriteSheet(
            sprite_sheet_path, pygame.Color("black")
        )
        self.image: pygame.Surface = self._sprite_sheet.image_at(image_rect)
        self.import_assets()

        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self._hitbox: pygame.Rect = self.rect.copy()

    def animate(self) -> pygame.Surface:
        """Animation loop for the character.

        Loops through the images to show walking animation.
        Works for each cardinal direction.

        Returns
        -------
        surface: pygame.Surface
            The surface containing the image of the specified rect from the animations
        """
        animation_strip = self._animations[self._status]

        self._frame_index += self._animation_speed

        if self._frame_index >= len(animation_strip):
            self._frame_index = 0

        return animation_strip[int(self._frame_index)]

    def import_assets(self, animation_dict: list[AnimationDict]) -> None:
        """Import and divide the animation image into it's smaller parts.

        Import all Entity animations according to the animation dictionary passed in.
        """
        for animation in animation_dict:
            self._animations[animation["name"]] = self._sprite_sheet.load_strip(
                animation["image_rect"], animation["image_count"]
            )
