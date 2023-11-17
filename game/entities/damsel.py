"""This module contains the Damsel class."""
import pygame
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

    def __init__(
        self,
        pos: tuple,
        groups: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ):
        """Initialize a Damsel with level info.

        Each damsel is initialized with their starting position,
        which sprite groups it is part of, boundary sprites,
        and enemy/interactable sprites.

        Parameters
        ----------
        pos: tuple
            Starting x, y coordinates
        groups: list of sprite groups
            Which groups in level it is a part of
        obstacle_sprites: list of sprite groups
            Which sprites in the level damsel cannot walk through
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
        inflation_size = 8
        self.radar = self.rect.inflate(
            settings.TILESIZE * inflation_size, settings.TILESIZE * inflation_size
        )

        self.obstacle_sprites = obstacle_sprites
        self.import_assets()

    def automate_movement(self):
        """Movement logic method."""
        # update radar with new pos
        self.radar.center = self.rect.center
        # always patrol when no radar detections
        passive_state = self.set_state_patrol

        # change state to follow if player is nearby
        active_state = self.set_state_follow
        self.radar_detect_player_entity(active_state, passive_state)

        # change state to flee if evil_entity nearby
        active_state = self.set_state_flee
        self.radar_detect_entities(self._bad_sprites, active_state, passive_state)

        self.move_based_on_state()

    def collision_handler(self):
        """Handle collision interactions with the environment.

        Parameters
        ----------
        direction: string
            Used to determine horizontal/vertical check.
        """
        enemy_sprites = self._bad_sprites.sprites()
        collisions = self.rect.collidelistall(enemy_sprites)

        if collisions:
            self.die()

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ):
        """Update damsel behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        bad_sprites: pygame.sprite.Group
            Group of enemy entities used to for behavior
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.set_status_by_curr_rotation()
        self.image = self.animate()
        self.collision_handler()
        # will move half as fast as player at the same speed
        self.automate_movement()
