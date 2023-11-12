"""This module contains the Skeleton class."""
import pygame
from filemanagement.spriteSheet import SpriteSheet
from entities.entity import Entity

IMAGE_WIDTH = 48
IMAGE_HEIGHT = 64

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20

# modify model rect to have slightly less tall hitbox. Used for movement
SPRITE_HITBOX_OFFSET = -4


class Skeleton(Entity):
    """First enemy class. Called Skeleton.

    Inherits from Entity. Move method is overwritten using logic described
    in the docs. Still uses Entity's collision_check method.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        """Construct the skeleton class."""
        super().__init__(groups)

        # grab self image
        skeletonMovementsPath = "graphics/skeleton/skeleton.png"
        self.skeletonAnimations = SpriteSheet(skeletonMovementsPath)
        skeletonSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.image = self.skeletonAnimations.image_at(
            skeletonSelfImageRect
        ).convert_alpha()
        self.setColorKeyBlack()
        self.rect = self.image.get_rect(topleft=pos)

        # modify model rect to be a slightly less tall hitbox.
        # this will be used for movement.
        self.hitbox = self.rect.inflate(0, SPRITE_HITBOX_OFFSET)

        self.obstacleSprites = obstacle_sprites
        self.import_skeleton_assets()

    def import_skeleton_assets(self):
        """Import and divide the animation image into it's smaller parts.

        Called at end of :func:'init()', takes the image with all character animations
        and divides it into its sub-images. Can be expanded with more images to fulfill
        idle and attack animations.
        """
        walkingUpRect = (0, SPRITE_HEIGHT * 3, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingDownRect = (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingLeftRect = (0, SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingRightRect = (0, SPRITE_HEIGHT * 2, SPRITE_WIDTH, SPRITE_HEIGHT)

        # number of images for each directional animation
        IMAGE_COUNT = 3

        # animation states in dictionary
        self.animations = {
            "up": self.skeletonAnimations.load_strip(walkingUpRect, IMAGE_COUNT),
            "down": self.skeletonAnimations.load_strip(walkingDownRect, IMAGE_COUNT),
            "left": self.skeletonAnimations.load_strip(walkingLeftRect, IMAGE_COUNT),
            "right": self.skeletonAnimations.load_strip(walkingRightRect, IMAGE_COUNT),
        }

    def collision_handler(self, direction):
        """Collision check for entity.

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.

        Parameters
        ----------
        direction: str
            the axis to check for collisions on. It can be 'horizontal' or 'vertical'.
        """
        return

    def update(self, enemy_sprites, friendly_sprites):
        """Update skeleton behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        friendly_sprites : pygame.sprite.Group()
            group of entities friendly to the player used for behavior
        """
        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.animate()
        # will move half as fast as player at the same speed
        self.move(self.speed)
