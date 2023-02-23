import pygame
import random
import time
from entity import Entity


class Enemy1(Entity):
    """First enemy class

    Inherits from Entity. Move method is overwritten using logic described
    in the docs. Still uses Entity's collision_check method.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            "graphics/enemy1/enemy1animation1.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # modify model rect to be a slightly less tall hitbox.
        # this will be used for movement.
        self.hitbox = self.rect.inflate(0, -26)
        self.speed = 0.5
        random.seed(time.time())

        self.obstacleSprites = obstacle_sprites
        self.timer = 100

    def move(self, speed):
        self.timer += 1
        # update direction every 100 ticks. Still moves every tick
        if self.timer >= 10:
            # update/randomize direction
            # get random number
            seed = random.randint(1, 1000)
            # if odd turn left else right
            if seed % 2:
                self.direction.x = -1
            else:
                self.direction.x = 1
            # if %3 false turn up else down
            if seed % 3:
                self.direction.y = -1
            else:
                self.direction.y = 1
            self.timer = 0

        # prevent diagonal moving from increasing speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # update
        self.hitbox.x += self.direction.x * speed
        self.collision_check("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision_check("vertical")
        self.rect.center = self.hitbox.center

    def collision_check(self, direction):
        """Collision check for entity

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.

        Parameters
        ----------
        direction: str
            the axis to check for collisions on. It can be 'horizontal' or 'vertical'.
        """

        # horizontal collision detection
        if direction == "horizontal":
            # look at all sprites
            for sprite in self.obstacleSprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        # vertical collision detection
        if direction == "vertical":
            # look at all sprites
            for sprite in self.obstacleSprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        self.move(self.speed)
