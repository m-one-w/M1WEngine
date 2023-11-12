"""This module contains the Entity class."""
import pygame
from direction import Direction
from tile import Tile
from abc import (
    ABC,
    abstractmethod,
)


class Entity(Tile, ABC):
    """Entity abstract class.

    Base class for all entities including player, enemies, and damsels.
    ...

    Attributes
    ----------
    frameIndex : int
        the currently shown frame represented by an index
    animationSpeed : int
        the speed at which animations run
    speed : int
        the speed at which the sprite moves

    Methods
    -------
    collision_check(self, direction)
        Handles the collision check for entities
    """

    def __init__(self, groups):
        """Initialize base class."""
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.speed = 1
        self.compass.x = Direction.right.value
        self.status = "right"

    def animate(self):
        """Animation loop for the entity.

        Loops through the images to show walking animation.
        Works for each cardinal direction.
        """
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]

    def set_status_by_curr_rotation(self):
        """Set the correct status based on the current direction.

        This function inspects the current direction and determines
        what the status should be.
        """
        # -- xy | xy +-
        # -+ xy | xy ++
        if self.compass.x > 0 and self.compass.y < 0.25 and self.compass.y > -0.25:
            self.status = "right"
        if self.compass.x < 0 and self.compass.y < 0.25 and self.compass.y > -0.25:
            self.status = "left"
        if self.compass.y > 0 and self.compass.x < 0.25 and self.compass.x > -0.25:
            self.status = "down"
        if self.compass.y < 0 and self.compass.x < 0.25 and self.compass.x > -0.25:
            self.status = "up"

    def get_angle_from_direction(self, axis):
        """Get the angle for sprite rotation based on the direction.

        Angle returned will need to be inverted for 'down' and 'left'.
        """
        angle = 0

        if axis == "x":
            angle = self.compass.y * 45
        if axis == "y":
            angle = self.compass.x * 45

        return -angle

    def set_image_rotation(self, image):
        """Set a new image to the correct rotation.

        Return the rotated image correlating to the correct rotation.
        Rotation is based on the status, so image rotations are defined by the
        current status.
        """
        angle = 0

        if self.status == "right":
            angle = self.get_angle_from_direction("x")
        if self.status == "left":
            angle = -self.get_angle_from_direction("x")
        if self.status == "up":
            angle = self.get_angle_from_direction("y")
        if self.status == "down":
            angle = -self.get_angle_from_direction("y")

        return pygame.transform.rotate(image, angle)

    @abstractmethod
    def collision_handler(self):
        """Handle the collision check for entities.

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
