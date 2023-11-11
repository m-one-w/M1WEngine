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
    speed : int
        the speed at which the sprite moves

    Methods
    -------
    collision_check(self, direction)
        Handles the collision check for entities
    """

    def __init__(self, groups):
        """Initialize base class"""
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.speed = 0

    @abstractmethod
    def collision_handler(self):
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
