"""This module contains the Damsel class."""
import pygame
from tiles.entities.characters.NPCs.NPC import NPC
import settings


class Damsel(NPC):
    """Damsel class to represent a good NPC within the game.

    Each damsel spawned in runs away from bad NPCs and move
    towards a nearby player.

    Attributes
    ----------
    _sprite_sheet: SpriteSheet
        The sprite sheet containing damsel images
    image: pygame.Surface
        The current damsel image to render
    rect: pygame.Rect
        The rectangle of the damsel image
    _obstacle_sprites: pygame.sprite.Group
        The sprite group containing all obstacles

    Methods
    -------
    automate_movement(self)
        Handle damsel specific movement
    collision_handler(self)
        Handles interaction with enemy sprites.
    die(self)
        Handle damsel death actions
    update(self)
        Update current game info, handle next image, move, and handle collisions
    """

    def __init__(
        self,
        pos: tuple,
        group: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ) -> None:
        """Initialize a Damsel with level info.

        Each damsel is initialized with their starting position,
        which sprite groups it is part of, boundary sprites,
        and enemy/interactable sprites.

        Parameters
        ----------
        pos: tuple
            Starting (x, y) coordinates
        group: list of sprite groups
            Which groups in level it is a part of
        obstacle_sprites: list of sprite groups
            Which sprites in the level damsel cannot walk through
        """
        damsel_image_path: str = settings.CHARACTER_IMAGES + "NPCs/damsel/damsel.png"
        damsel_image_rect: pygame.Rect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        super().__init__(group, pos, damsel_image_path, damsel_image_rect)

        self._obstacle_sprites: pygame.sprite.Group = obstacle_sprites

    def automate_movement(self) -> None:
        """Movement logic method."""
        # update radar with new pos
        self._radar.center: tuple[int, int] = self.rect.center
        # always patrol when no radar detections
        passive_state = self.set_state_patrol

        # change state to flee if evil_entity nearby
        active_state = self.set_state_flee
        self.radar_set_states(self._bad_sprites, active_state, passive_state)

        # change state to follow if player is nearby
        active_state = self.set_state_follow
        self.radar_set_state(self._player, active_state)

        self.move_based_on_state()

    def collision_handler(self) -> None:
        """Handle collision interactions with the environment and other entities."""
        super().collision_handler()
        enemy_sprites: list = self._bad_sprites.sprites()
        collisions: list[int] = self.rect.collidelistall(enemy_sprites)

        if collisions:
            self.die()

    def die(self) -> None:
        """Handle effects of damsel death."""
        self._score_controller.good_entity_destroyed_update_score(
            self.__class__.__name__
        )
        super().die()

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ) -> None:
        """Update damsel behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/spec_sheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        bad_sprites: pygame.sprite.Group
            The sprite group containing all bad entities
        good_sprites: pygame.sprite.Group
            The sprite group containing all good entities
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.set_status_by_curr_rotation()
        self.image = self.animate()
        # will move half as fast as player at the same speed
        self.automate_movement()
        self.collision_handler()
