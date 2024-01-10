"""This module contains the Entity class."""
import pygame
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
    _animation_dict: dict
        The dictionary containing directionally sorted animation images
    _animations: dict
        The dictionary containing all animations for the current direction
    _sprite_sheet: SpriteSheet
        Handler for entire sprite sheet of animation images
    _status: str
        The direction a character is facing stored as a string

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
        self._status: str = "right"
        self.image = self._sprite_sheet.image_at(image_rect)
        self.import_assets()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()

    def animate(self) -> pygame.Surface:
        """Animation loop for the character.

        Loops through the images to show walking animation.
        Works for each cardinal direction.

        Returns
        -------
        animation_strip: pygame.Surface
            The surface containing the image of the specified rect from the animations
        """
        animation_strip = self._animations[self._status]

        self._frame_index += self._animation_speed

        if self._frame_index >= len(animation_strip):
            self._frame_index = 0

        return animation_strip[int(self._frame_index)]

    def import_assets(self) -> None:
        """Import and divide the animation image into it's smaller parts.

        Import all Entity animations according to the animation dictionary passed in.
        """
        for animation in self._animation_dict:
            self._animations[animation["name"]] = self._sprite_sheet.load_strip(
                animation["image_rect"], animation["image_count"]
            )
