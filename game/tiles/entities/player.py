"""This module contains the Player class."""
import random
import pygame
from tiles.entities.actions import Actions
from tiles.entities.entity import Entity
import settings

# Defines how fast the player object can rotate while running
PLAYER_ROTATION_SPEED = 5
# Defines how many queue actions there can be at one time
MAX_ACTION_QUEUE_LENGTH = 3


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
    _action_queue: list
        Contain the internal player action queue

    Methods
    -------
    input(self)
        Handle keyboard input for the player
    ensure_full_action_queue(self)
        Ensure the action queue is growing if less than max length
    current_action(self)
        Get the current player action
    pop_next_player_action(self)
        Get and remove the next player action
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
        self.image: pygame.surface = self.sprite_sheet.image_at(playerSelfImageRect)
        self.setColorKeyBlack()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, settings.ENTITY_HITBOX_OFFSET)

        self.obstacle_sprites = obstacle_sprites
        self.import_assets()
        self._action_queue: list = []

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

    def ensure_full_action_queue(self):
        """Fill up the current action queue up to a limit."""
        if len(self._action_queue) < MAX_ACTION_QUEUE_LENGTH:
            actions = [Actions.consume, Actions.destroy, Actions.throw]
            self._action_queue.append(random.choice(actions))

    def current_action(self) -> Actions:
        """Get the current action."""
        current_action = Actions.none
        if len(self._action_queue) > 0:
            current_action = self._action_queue[-1]
        return current_action

    def pop_next_player_action(self) -> Actions:
        """Pop the next action off the queue."""
        current_action = Actions.none
        if len(self._action_queue) > 0:
            current_action = self._action_queue.pop()
        return current_action

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ):
        """Update player behavior based on player input.

        Controls and movement logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.input()
        self.ensure_full_action_queue()
        self.set_status_by_curr_rotation()
        image = self.animate()
        self.image = self.set_image_rotation(image)
        # a new direction may be set by the collision handler
        self.collision_handler()
        # will move twice as fast as any other entity at the same speed due to camera.
        self.move(self.speed)
