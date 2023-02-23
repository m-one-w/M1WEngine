import pygame
from settings import TILESIZE


class Entity(pygame.sprite.Sprite):
    """Entity base class

    Base class for all entities including player, enemies, and damsels.
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

    def collision_check(self, direction):
        """Collision check for entity

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.
        """

        raise Exception("Not Implemented")
