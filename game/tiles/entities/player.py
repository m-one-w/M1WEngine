"""This module contains the Player class."""
import pygame
from tiles.entities.entity import Entity
import settings

# Defines how fast the player object can rotate while running
PLAYER_ROTATION_SPEED = 5


class Player(Entity):
    """Player class which contains the object players will directly control.

    The player class will handle movement logic and sprite changing logic for the player
    object. The player class will also handle any collision logic that influences the
    player object.

    Attributes
    ----------
    sprite_sheet: SpriteSheet
        Hold all the player animations
    image: pygame.Surface
        Hold the current player image
    rect: pygame.Rect
        Hold the player position and size
    hitbox: pygame.Rect
        Hold the player hitbox
    obstacle_sprites: pygame.sprite.Group
        Contain which sprites are considered opbstacles

    Methods
    -------
    input(self)
        Handle keyboard input for the player
    update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    )
        Update all player data
    """

    def __init__(
        self,
        pos: tuple,
        groups: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ):
        """Construct the player object.

        Sets all required values to construct the player object.
        """
        super().__init__(groups)

        # grab self image
        playerMovementsPath = "graphics/player/playerWalking.png"
        self.sprite_sheet = self.get_sprite_sheet(playerMovementsPath)
        playerSelfImageRect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        self.image = self.sprite_sheet.image_at(playerSelfImageRect)
        self.setColorKeyBlack()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, settings.ENTITY_HITBOX_OFFSET)

        self.obstacle_sprites = obstacle_sprites
        self.import_assets()

    def input(self):
        """Input function to handle keyboard input to the player class.

        This function will handle turning the player object as input is received.
        """
        keys = pygame.key.get_pressed()

        # left/right input
        if keys[pygame.K_LEFT]:
            self.compass.rotate_ip(-PLAYER_ROTATION_SPEED)
        elif keys[pygame.K_RIGHT]:
            self.compass.rotate_ip(PLAYER_ROTATION_SPEED)

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ):
        """Update player behavior based on player input.

        Controls and movement logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.input()
        self.set_status_by_curr_rotation()
        image = self.animate()
        self.image = self.set_image_rotation(image)
        # a new direction may be set by the collision handler
        self.collision_handler()
        # will move twice as fast as any other entity at the same speed due to camera.
        self.move(self.speed)
