import pygame
from tile import Tile
from abc import (
    ABC,
    abstractmethod,
)


class Entity(Tile, ABC):

    """Entity abstract class

    Base class for all entities including player, enemies, and damsels.
    ...

    Attributes
    ----------
    frameIndex : int
        the currently shown frame represented by an index
    animationSpeed : int
        the speed at which animations run
    direction : pygame.math.Vector2
        the x and y direction of movement. This will be in a range
        of -1 to 1 where 0 means no movement.
    speed : int
        the speed at which the sprite moves
    movementTracker
        Contains how far the entity has traveled without moving

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
    collision_check(self, direction)
        Handles the collision check for entities

    """

    def __init__(self, groups):
        """Initialize base class"""
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.direction = pygame.math.Vector2()
        self.speed = 0
        self.movementTracker = {"vertical": 0.0, "horizontal": 0.0}

    def move(self, speed):
        """Handles movement of the entity

        Updates position of the entity using current heading and speed.
        Will be overwritten inherited classes that use different movement described
        in the docs.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        # define the coordinate system
        left = -1
        right = 1
        up = -1
        down = 1

        # move each time a tracker is 1 or -1 and then reset the tracker
        self.update_movement_tracker()

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

    def move_left(self, speed):
        """Move to the left

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = -1 * speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def move_right(self, speed):
        """Move to the right

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = 1 * speed
        move_pixels_y = 0
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def move_up(self, speed):
        """Move up

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = -1 * speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def move_down(self, speed):
        """Move down

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position
        """
        move_pixels_x = 0
        move_pixels_y = 1 * speed
        self.rect.move_ip(move_pixels_x, move_pixels_y)

    def update_movement_tracker(self):
        """Update movement tracker

        Keeps tracker of how far the entity has moved without yet accounting for that
        movement. Each time a movement of 1 pixel is detected, the move will be made,
        and the tracker will be modified by that move distance in pixels towards 0.
        Speed can multiply the number of pixels moved at a time.
        """
        self.movementTracker["horizontal"] += self.direction.x
        self.movementTracker["vertical"] += self.direction.y

    @abstractmethod
    def collision_check(self, direction):
        """Handles the collision check for entities

        This method should be implemented in any child classes that use it.
        The method should handle the following:
        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.

        Parameters
        ----------
        direction : str
            the axis to check for a collision on
        """

        raise Exception("Not Implemented")
