"""This module contains the Postman class."""
import pygame
from tiles.entities.characters.NPCs.NPC import NPC
import settings


class Postman(NPC):
    """Postman class to represent a good NPC within the game.

    Attributes
    ----------
    _obstacle_sprites: pygame.sprite.Group
        The sprite group containing all obstacles

    Methods
    -------
    automate_movement(self)
        Handle postman specific movement
    collision_handler(self)
        Handles interaction with enemy sprites.
    die(self)
        Handle postman death actions
    update(self)
        Update current game info, handle next image, move, and handle collisions
    """

    def __init__(
        self,
        pos: tuple,
        group: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ) -> None:
        """Initialize a Postman with level info.

        Parameters
        ----------
        pos: tuple
            Starting (x, y) coordinates
        group: list of sprite groups
            Which groups in level it is a part of
        obstacle_sprites: list of sprite groups
            Which sprites in the level postman cannot walk through
        """
        postman_image_path: str = settings.CHARACTER_IMAGES + "NPCs/postman/postman.png"
        postman_image_rect: pygame.Rect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        super().__init__(group, pos, postman_image_path, postman_image_rect)

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

        self.move_based_on_state()

    def collision_handler(self) -> None:
        """Handle collision interactions with the environment and other entities."""
        super().collision_handler()

        player_collisions = self.rect.colliderect(self._player._hitbox)

        if player_collisions:
            self.neutral_collided_with_player()
        else:
            self._hud.try_close_level_prompt()

    def die(self) -> None:
        """Handle effects of postman death."""
        self._score_controller.good_entity_destroyed_update_score(
            self.__class__.__name__
        )
        super().die()

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ) -> None:
        """Update postman behavior based on entities on the map.

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
