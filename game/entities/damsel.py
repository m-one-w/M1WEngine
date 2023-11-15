"""This module contains the Damsel class."""
import pygame
import random
import time
from entities.entity import Entity
import settings


class Damsel(Entity):
    """Damsel class to represent a good entity within the game.

    Each damsel object that is spawned in will be hunted by enemy
    sprites while the player character will try to save them.

    Methods
    -------
    collision_handler(self)
        Handles interaction with environment.
    update(self)
        Update damsel with current game state information.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        """Initialize a Damsel with level info.

        Each damsel is initialized with their starting position,
        which sprite groups it is part of, boundary sprites,
        and enemy/interactable sprites.

        Parameters
        ----------
        pos : Tuple
            starting x, y coordinates
        groups : list of sprite groups
            which groups in level it is a part of
        obstacle_sprites : list of sprite groups
            which sprites in the level damsel cannot walk through
        """
        super().__init__(groups)

        damselMovementImagePath = "graphics/damsel/damselWalking.png"
        self.sprite_sheet = self.get_sprite_sheet(damselMovementImagePath)
        damselSelfImageRect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        self.image = self.sprite_sheet.image_at(damselSelfImageRect)
        self.setColorKeyWhite()
        self.rect = self.image.get_rect(topleft=pos)
        # modify model rect to be a slightly less tall hitbox.
        self.hitbox = self.rect.inflate(0, -10)
        random.seed(time.time())
        self.timer = 100
        self.obstacle_sprites = obstacle_sprites
        self.enemy_sprites = pygame.sprite.Group()
        self.import_assets()

    def collision_handler(self):
        """Handle collision interactions with the environment.

        Parameters
        ----------
        direction : string
            used to determine horizontal/vertical check.
        """
        enemy_sprites = self.enemy_sprites.sprites()
        collisions = self.rect.collidelistall(enemy_sprites)

        if collisions:
            self.die()

    def update(self, enemy_sprites, friendly_sprites):
        """Update damsel behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        enemy_sprites : pygame.sprite.Group()
            group of enemy entities used to for behavior
        """
        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.set_status_by_curr_rotation()
        self.image = self.animate()
        self.collision_handler()
        # will move half as fast as player at the same speed
        self.move(self.speed)
