"""This module contains the Minotaur class."""
import pygame
from m1wengine.tiles.entities.characters.NPCs.NPC import NPC
import m1wengine.settings as settings


class Minotaur(NPC):
    """Minotaur class.

    Defines how a minotaur will behave.

    Attributes
    ----------
    _hitbox: pygame.rect
        The rect where a minotaur can be hit
    image: pygame.Surface
        The image to display when rendering

    Methods
    -------
     __init__(self)
        Initialize the minotaur object's instance
    automate_movement(self)
        Define how minotaur will move
    collision_handler(self)
        Define how to handle collisions
    die(self)
        Handle minotaur death actions
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
        """Construct the minotaur class.

        Parameters
        ----------
        pos: tuple
            The spawning position in the map as (x,y) coordinates
        group: pygame.sprite.Group
            The sprite groups this minotaur is a part of
        obstacle_sprites: pygame.sprite.Group
            The sprites the minotaur cannot move through
        """
        minotaur_width: int = 48
        minotaur_height: int = 48
        minotaur_movements_path: str = (
            settings.CHARACTER_IMAGES + "NPCs/minotaur/minotaur.png"
        )
        minotaur_image_rect: pygame.Rect = pygame.Rect(
            0, 0, minotaur_width, minotaur_height
        )
        # self.setup_import_assets()
        super().__init__(
            group, pos, minotaur_movements_path, minotaur_image_rect, obstacle_sprites
        )
        self._hitbox: pygame.Rect = self.rect
        self.speed: int = self.DEFAULT_SPEED

    def automate_movement(self) -> None:
        """Movement logic method."""
        # update radar with new pos
        self.radar.center = self.rect.center
        # always patrol when no radar detections
        passive_state: callable = self.set_state_patrol

        # change state to flee if player is nearby
        active_state: callable = self.set_state_flee
        self.radar_set_states(self._player, active_state, passive_state)

        active_state = self.set_state_track
        self.radar_set_state(self._good_sprites, active_state)

        self.move_based_on_state()

    def collision_handler(self) -> None:
        """Handle collision interactions with environment.

        Raises
        -------
            ValueError: when unable to resolve player collisions
        """
        super().collision_handler()
        collisions = self.rect.colliderect(self._player._hitbox)

        if collisions:
            try:
                self.collided_with_player()
            except ValueError:
                print("Unable to resolve player collisions from minotaur.")

    def die(self) -> None:
        """Handle actions on minotaur death."""
        self._score_controller.bad_entity_destroyed_update_score(
            self.__class__.__name__
        )
        super().die()

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ) -> None:
        """Update minotaur behavior based on entities on the map.

        Parameters
        ----------
        bad_sprites: pygame.sprite.Group()
            Group of bad aligned sprites
        good_sprites: pygame.sprite.Group()
            Group of good aligned sprites
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        image: pygame.Surface = self.animate()
        self.image: pygame.Surface = self.set_image_rotation(image)
        # will move half as fast as player at the same speed
        self.automate_movement()
        self.set_status_by_curr_rotation()

        if self._current_state != self._states.Thrown:
            # thrown collision handler must be handled within auto movement
            self.collision_handler()
