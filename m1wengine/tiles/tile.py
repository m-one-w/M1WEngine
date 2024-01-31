"""This module contains the Tile class."""
import pygame
from m1wengine.enums.direction import Direction


class Tile(pygame.sprite.Sprite):
    """Base class for all game :func:`Sprite<pygame.sprite.Sprite>`.

    Attributes
    ----------
    _movement_tracker: dict[str, float]
        Contains how far the entity has traveled without moving
    _compass: pygame.math.Vector2
        The x and y direction of movement bounded [-1, 1]
    _image: pygame.Surface
        The current image to display on the screen
    _rect: pygame.Rect
        The size of the current image as a Rect
    _hitbox: pygame.Rect
        The modified image Rect for collision checks

    Methods
    -------
    compass(self) -> pygame.math.Vector2
        Return _compass value
    compass(self, new_value: pygame.math.Vector2) -> None
        Change the compass value
    image(self) -> pygame.Surface
        Return the current image to display onto the screen
    image(self, new_value: pygame.Surface) -> None
        Change the tile image
    move(self, speed: int)
        Handles movement of the entity
    move_left(self, speed: int)
        Moves left
    move_right(self, speed: int)
        Moves right
    move_up(self, speed: int)
        Moves up
    move_down(self, speed: int)
        Moves down
    update_movement_tracker(self)
        Tracks where to move
    set_tile(self, x: int, y: int, surface: pygame.surface)
        sets all info for a background tile
    _move_left(self, speed: int)
        Internal move left
    _move_right(self, speed: int)
        Internal move right
    _move_up(self, speed: int)
        Internal move up
    _move_down(self, speed: int)
        Internal move down
    """

    def __init__(self, groups: pygame.sprite.Group) -> None:
        """Initialize a tile.

        Parameters
        ----------
        groups: pygame.sprite.Group
            The groups this sprite is a part of
        """
        super().__init__(groups)
        self._movement_tracker: dict[str, float] = {"vertical": 0.0, "horizontal": 0.0}
        self._compass: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

        self._image: pygame.Surface = object()
        self._rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self._hitbox: pygame.Rect = self.rect

    @property
    def compass(self) -> pygame.math.Vector2:
        """Return the compass Vector2."""
        return self._compass

    @compass.setter
    def compass(self, new_value: pygame.math.Vector2) -> None:
        """Assign the new Vector2 to the tile's compass.

        Parameters
        ----------
        new_value: pygame.math.Vector2
            The new compass vector to set

        Raises
        ------
        TypeError: parameter must be a Vector2 type
        """
        if type(new_value) is not pygame.math.Vector2 or not pygame.Vector2:
            raise TypeError("ERROR: compass must be a Vector2 type.")
        else:
            self._compass = new_value

    @property
    def image(self) -> pygame.Surface:
        """Return the current tile image."""
        return self._image

    @image.setter
    def image(self, new_value: pygame.Surface) -> None:
        """Assign the new image to the tile.

        Parameters
        ----------
        new_value: pygame.Surface
            The new image Surface to set

        Raises
        ------
        TypeError: parameter must be a pygame.Surface type
        """
        if type(new_value) is not pygame.Surface:
            raise TypeError("ERROR: image must be a pygame.Surface type.")
        else:
            self._image = new_value

    @property
    def rect(self) -> pygame.Rect:
        """Return the tile's rectangle."""
        return self._rect

    @rect.setter
    def rect(self, new_value: pygame.Rect) -> None:
        """Set the tile's new rect.

        Parameters
        ----------
        new_value: pygame.Rect
            The new rectangle size of the tile

        Raises
        ------
        TypeError: parameter must be a pygame.Rect type
        """
        if type(new_value) is not pygame.Rect:
            raise TypeError("ERROR: new value must be a pygame.Rect type")
        else:
            self._rect = new_value

    def move(self, speed: int = 1) -> None:
        """Handle movement of the tile.

        Updates position of the tile using current heading and speed.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        # move each time a tracker is 1 or -1 and then reset the tracker
        self.update_movement_tracker()

        up: Direction = Direction.up
        down: Direction = Direction.down
        left: Direction = Direction.left
        right: Direction = Direction.right

        if self._movement_tracker["vertical"] <= up:
            self._move_up(speed)
            self._movement_tracker["vertical"] += down
        elif self._movement_tracker["vertical"] >= down:
            self._move_down(speed)
            self._movement_tracker["vertical"] += up

        if self._movement_tracker["horizontal"] <= left:
            self._move_left(speed)
            self._movement_tracker["horizontal"] += right
        elif self._movement_tracker["horizontal"] >= right:
            self._move_right(speed)
            self._movement_tracker["horizontal"] += left

    def move_right(self, speed: int = 1) -> None:
        """Move to the right.

        Update the compass and move to the right.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self._compass.x = Direction.right
        self._compass.y = 0
        self._move_right(speed)

    def move_left(self, speed: int = 1) -> None:
        """Move to the left.

        Update the compass and move to the left.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self._compass.x = Direction.right
        self._compass.y = 0
        self._move_left(speed)

    def move_up(self, speed: int = 1) -> None:
        """Move up.

        Update the compass and move up.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self._compass.x = 0
        self._compass.y = Direction.up
        self._move_up(speed)

    def move_down(self, speed: int = 1) -> None:
        """Move down.

        Update the compass and move down.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        self._compass.x = 0
        self._compass.y = Direction.down
        self._move_down(speed)

    def update_movement_tracker(self) -> None:
        """Update movement tracker.

        Keeps tracker of how far the entity has moved without yet accounting for that
        movement. Each time a movement of 1 pixel is detected, the move will be made,
        and the tracker will be modified by that move distance in pixels towards 0.
        Speed can multiply the number of pixels moved at a time.
        """
        self._movement_tracker["horizontal"] += self._compass.x
        self._movement_tracker["vertical"] += self._compass.y

    def set_tile(self, coords: tuple, surface: pygame.Surface) -> None:
        """Set the position and surface of a tile.

        Parameters
        ----------
        coords: tuple
            The x and y coordinate of the tile
        surface: pygame.Surface
            The :func:`Sprite<pygame.sprite.Sprite>` image to display
        """
        self.image = surface
        self.rect = self.image.get_rect(topleft=coords)
        self._hitbox = self.rect

    def die(self) -> None:
        """Remove the sprite from all groups."""
        self.kill()

    def _move_left(self, speed: int) -> None:
        """Move to the left.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = -1 * speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self._hitbox.center = self.rect.center

    def _move_right(self, speed: int) -> None:
        """Move to the right.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self._hitbox.center = self.rect.center

    def _move_up(self, speed: int) -> None:
        """Move up.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = -1 * speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self._hitbox.center = self.rect.center

    def _move_down(self, speed: int) -> None:
        """Move down.

        Parameters
        ----------
        speed: int
            Multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)
        self._hitbox.center = self.rect.center
