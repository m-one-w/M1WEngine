"""This module contains the Skeleton class."""
import pygame
from tiles.entities.characters.NPCs.NPC import NPC
import settings


class Skeleton(NPC):
    """Skeleton class.

    Defines how the skeleton behaves.

    Methods
    -------
    automate_movement(self)
        Define how skeleton will move
    collision_handler(self)
        Define how to handle collisions
    die(self)
        Handle skeleton death actions
    update(self,  bad_sprites: pygame.sprite.Group,
    good_sprites: pygame.sprite.Group)
        Update animation and move with collision handling
    """

    def __init__(
        self,
        pos: tuple,
        group: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ) -> None:
        """Construct the skeleton class.

        Parameters
        ----------
        pos: tuple
            The spawning position in the map as (x,y) coordinates
        group: pygame.sprite.Group
            The sprite groups this skeleton is a part of
        obstacle_sprites: pygame.sprite.Group
            The sprites the skeleton cannot move through
        """
        skeleton_movements_path: str = (
            settings.CHARACTER_IMAGES + "NPCs/skeleton/skeleton.png"
        )
        skeleton_image_rect: pygame.Rect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        super().__init__(
            group, pos, skeleton_movements_path, skeleton_image_rect, obstacle_sprites
        )
        self.hitbox = self.rect.inflate(-4, 0)

    def automate_movement(self) -> None:
        """Movement logic method."""
        # update radar with new pos
        self._radar.center = self.rect.center
        # always patrol when no radar detections
        passive_state = self.set_state_patrol

        # change state to flee if player is nearby
        active_state = self.set_state_flee
        self.radar_set_states(self._player, active_state, passive_state)

        # change state to attack if there is good_entity nearby
        active_state = self.set_state_attack
        self.radar_set_state(self._good_sprites, active_state)

        self.move_based_on_state()

    def collision_handler(self) -> None:
        """Handle collision interactions with environment."""
        super().collision_handler()
        collisions = self.rect.colliderect(self._player.hitbox)

        if collisions:
            try:
                self.collided_with_player()
            except ValueError:
                print("Unable to resolve player collisions from skeleton.")

    def die(self) -> None:
        """Handle actions on skeleton death."""
        self._score_controller.bad_entity_destroyed_update_score(
            self.__class__.__name__
        )
        super().die()

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ) -> None:
        """Update skeleton behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/spec_sheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        bad_sprites: pygame.sprite.Group()
            Group of bad aligned sprites
        good_sprites: pygame.sprite.Group()
            Group of good aligned sprites
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.set_status_by_curr_rotation()
        self.image = self.animate()
        # will move half as fast as player at the same speed
        self.automate_movement()

        if self._current_state != self._states.Thrown:
            # Flee collision handler must be handled within auto movement
            self.collision_handler()
