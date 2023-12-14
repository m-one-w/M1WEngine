"""This module contains the Damsel class."""
import pygame
from filemanagement.spriteSheet import SpriteSheet
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
    _image: pygame.Surface
        The current damsel image to render
    _rect: pygame.Rect
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
        groups: pygame.sprite.Group,
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
        groups: list of sprite groups
            Which groups in level it is a part of
        obstacle_sprites: list of sprite groups
            Which sprites in the level damsel cannot walk through
        """
        super().__init__(groups)

        damsel_image_path: str = "graphics/damsel/damselWalking.png"
        self._sprite_sheet: SpriteSheet = SpriteSheet(
            damsel_image_path, pygame.Color("black")
        )
        damsel_image_rect: pygame.Rect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        self._image: pygame.Surface = self._sprite_sheet.image_at(damsel_image_rect)
        self.rect: pygame.Rect = self._image.get_rect(topleft=pos)
        self._obstacle_sprites: pygame.sprite.Group = obstacle_sprites
        self.import_assets()

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
            self.damsel_die()

    def die(self) -> None:
        """Handle effects of damsel death."""
        self.scoreController.good_entity_destroyed_update_score(self.__class__.__name__)
        self.die()

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ) -> None:
        """Update damsel behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

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
        self._image = self.animate()
        # will move half as fast as player at the same speed
        self.automate_movement()
        self.collision_handler()
