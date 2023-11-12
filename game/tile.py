"""This module contains the Tile class."""
import pygame
from direction import Direction


class Tile(pygame.sprite.Sprite):
    """Base class for all game :func:`Sprite<pygame.sprite.Sprite>`.

    Attributes
    ----------
    direction : pygame.math.Vector2
        the x and y direction of movement. This will be in a range
        of -1 to 1 where 0 means no movement.
    movementTracker
        Contains how far the entity has traveled without moving
    colorKeyWhite
        the tuple to hold a white RGB value
    colorKeyBlack
        the tuple to hold a black RGB value

    Methods
    -------
    move(self, speed)
        Handles movement of the entity
    move_left(self, speed)
        Moves left
    move_right(self, speed)
        Moves right
    move_up(self, speed)
        Moves up
    move_down(self, speed)
        Moves down
    update_movement_tracker(self)
        Tracks where to move
    set_tile(self, x, y, surface)
        sets all info for a background tile
    """

    # other init options: sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))
    def __init__(self, groups):
        """Initialize a tile.

        Parameters
        ----------
        groups: the groups this sprite is a part of
        """
        super().__init__(groups)
        self.compass = pygame.math.Vector2()
        self.movementTracker = {"vertical": 0.0, "horizontal": 0.0}

        # r,g,b vals for key color
        self.colorKeyWhite = (255, 255, 255)
        self.colorKeyBlack = (0, 0, 0)

    def setColorKeyBlack(self):
        """Set the sprite alpha channel to ignore black backgrounds."""
        self.image.set_colorkey(self.colorKeyBlack, pygame.RLEACCEL)

    def setColorKeyWhite(self):
        """Set the sprite alpha channel to ignore white backgrounds."""
        self.image.set_colorkey(self.colorKeyWhite, pygame.RLEACCEL)

    def move(self, speed):
        """Handle movement of the tile.

        Updates position of the tile using current heading and speed.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        # move each time a tracker is 1 or -1 and then reset the tracker
        self.update_movement_tracker()

        up = Direction.up.value
        down = Direction.down.value
        left = Direction.left.value
        right = Direction.right.value

        if self.movementTracker["vertical"] <= up:
            self.move_up(speed)
            self.movementTracker["vertical"] += down
        elif self.movementTracker["vertical"] >= down:
            self.move_down(speed)
            self.movementTracker["vertical"] += up

        if self.movementTracker["horizontal"] <= left:
            self.move_left(speed)
            self.movementTracker["horizontal"] += right
        elif self.movementTracker["horizontal"] >= right:
            self.move_right(speed)
            self.movementTracker["horizontal"] += left

        # align hitbox with the new position
        self.hitbox.center = self.rect.center

    def move_left(self, speed):
        """Move to the left.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = -1 * speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def move_right(self, speed):
        """Move to the right.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = 1 * speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def move_up(self, speed):
        """Move up.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = -1 * speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def move_down(self, speed):
        """Move down.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = 1 * speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def update_movement_tracker(self):
        """Update movement tracker.

        Keeps tracker of how far the entity has moved without yet accounting for that
        movement. Each time a movement of 1 pixel is detected, the move will be made,
        and the tracker will be modified by that move distance in pixels towards 0.
        Speed can multiply the number of pixels moved at a time.
        """
        self.movementTracker["horizontal"] += self.compass.x
        self.movementTracker["vertical"] += self.compass.y

    def set_tile(self, x, y, surface):
        """Set the position and surface of a tile.

        Parameters
        ----------
        x: int
            the x location to render
        y: int
            the y location to render
        surface: pygame.surface
            the :func:`Sprite<pygame.sprite.Sprite>` image to display
        """
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect
