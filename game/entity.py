import pygame
from settings import TILESIZE
from abc import (
    ABC,
    abstractmethod,
)


class Entity(pygame.sprite.Sprite, ABC):
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

    Methods
    -------
    move(self, speed)
        Handles movement of the entity
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

    def move(self, speed):
        """Handles movement of the entity

        Updates position of the entity using current heading and speed.
        Will be overwritten inherited classes that use different movement described
        in the docs.

        Parameters
        ----------
        speed : int
            the multiplier for changing the sprite position.
        """

        # prevent diagonal moving from increasing speed
        # check if vector has magnitude
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # update position
        self.hitbox.x += self.direction.x * speed
        self.collision_check("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision_check("vertical")
        self.rect.center = self.hitbox.center

        # if we go beyond the map size, wrap around to the other side.
        # Need to test hitbox collisions if wrap around into a wall or enemy..
        if self.hitbox.x >= self.mapSize.x * TILESIZE:
            self.hitbox.x = TILESIZE
        if self.hitbox.y >= self.mapSize.y * TILESIZE:
            self.hitbox.y = TILESIZE

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
