"""This module contains the Skeleton class."""
import pygame
from filemanagement.spriteSheet import SpriteSheet
from tiles.entities.characters.NPCs.NPC import NPC
import settings


class Skeleton(NPC):
    """First enemy class. Called Skeleton.

    Inherits from Entity. Move method is overwritten using logic described
    in the docs. Still uses Entity's collision_check method.

    Attributes
    ----------
    sprite_sheet: SpriteSheet
        Hold the art assets info
    image: pygame.Surface
        Hold the current sprite image
    rect: pygame.Rect
        Hold the current sprite position
    hitbox: pygame.Rect
        Hold the hitbox rect
    radar: pygame.Rect
        Hold the radar rect
    obstacleSprites: pygame.sprite.Group
        Hold the sprites that block movement

    Methods
    -------
    automate_movement(self)
        Define how sprite will move
    collision_handler(self)
        Define how to handle collisions
    skeleton_die(self)
        Handle skeleton death actions
    update(self,  bad_sprites: pygame.sprite.Group,
    good_sprites: pygame.sprite.Group)
        Define what methods are called on each tick
    """

    def __init__(
        self,
        pos: tuple,
        groups: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ):
        """Construct the skeleton class."""
        super().__init__(groups)

        # grab self image
        skeletonMovementsPath = "graphics/skeleton/skeleton.png"
        self.sprite_sheet = SpriteSheet(skeletonMovementsPath, pygame.Color("black"))
        skeletonSelfImageRect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        self.image = self.sprite_sheet.image_at(skeletonSelfImageRect)
        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites
        self.import_assets()
        self.hitbox = self.rect.inflate(-4, 0)

    def automate_movement(self):
        """Movement logic method."""
        # update radar with new pos
        self.radar.center = self.rect.center
        # always patrol when no radar detections
        passive_state = self.set_state_patrol

        # change state to flee if player is nearby
        active_state = self.set_state_flee
        self.radar_set_states(self.player, active_state, passive_state)

        # change state to attack if there is good_entity nearby
        active_state = self.set_state_attack
        self.radar_set_state(self._good_sprites, active_state)

        self.move_based_on_state()

    def collision_handler(self):
        """Handle collision interactions with environment."""
        super().collision_handler()
        collisions = self.rect.colliderect(self.player.hitbox)

        if collisions:
            try:
                self.collided_with_player()
            except ValueError:
                print("Unable to resolve player collisions from skeleton.")

    def die(self):
        """Handle actions on skeleton death."""
        super().die()
        self.scoreController.bad_entity_destroyed_update_score(self.__class__.__name__)

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ):
        """Update skeleton behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        bad_sprites: pygame.sprite.Group()
            Group of entities hostile to the player
        good_sprites: pygame.sprite.Group()
            Group of entities friendly to the player
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.set_status_by_curr_rotation()
        self.image = self.animate()
        # will move half as fast as player at the same speed
        self.automate_movement()

        if self.current_state != self.states.Thrown:
            # Flee collision handler must be handled within auto movement
            self.collision_handler()
