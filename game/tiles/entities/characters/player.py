"""This module contains the Player class."""
import random
import pygame
from file_managers.spriteSheet import SpriteSheet
from enums.actions import Actions
from enums.eatenPowers import EatenPowers
from tiles.entities.characters.character import Character
import settings

# Defines how fast the player object can rotate while running
PLAYER_ROTATION_SPEED = 5
# Defines how many queue actions there can be at one time
MAX_ACTION_QUEUE_LENGTH = 3


class Player(Character):
    """Player class contains the object players will directly control.

    The player class will handle user input, movement logic, and logic for powers.
    The player class will also handle the action queue for said powers.

    Attributes
    ----------
    _sprite_sheet: SpriteSheet
        Hold all the player animations
    image: pygame.Surface
        Hold the current player animation image
    rect: pygame.Rect
        Hold the player position and size
    _hitbox: pygame.Rect
        Hold the player hitbox
    _obstacle_sprites: pygame.sprite.Group
        Hold the sprites that are considered obstacles
    _action_queue: list
        Contain the internal player action queue

    Methods
    -------
    eaten_power(self)
        Get the current eaten power
    eaten_power(self, new_value) -> EatenPowers
        Set the current eaten power
    input(self)
        Handle keyboard input for the player
    ensure_full_action_queue(self)
        Ensure the action queue is growing if less than max length
    current_action(self) -> Actions
        Get the current player action
    pop_next_player_action(self) -> Actions
        Get and remove the next player action
    move(self, speed)
        Player specific movement logic
    update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    )
        Update data, get user input, animate, rotate, handle collisions, and movement
    """

    def __init__(
        self,
        pos: tuple,
        groups: pygame.sprite.Group,
        obstacle_sprites: pygame.sprite.Group,
    ) -> None:
        """Construct the player object.

        Sets all required values to construct the player object.

        Parameters
        ----------
        pos: tuple
            The (x, y) position the player spawns at
        groups: pygame.sprite.Group
            The sprite groups the player is part of
        obstacle_sprites: pygame.sprite.Group
            The sprite group containing all sprites the player can't move through
        """
        super().__init__(groups)

        # grab self image
        playerMovementsPath = (
            "game_assets/graphics/tiles/entities/characters/player/player.png"
        )
        self._sprite_sheet = SpriteSheet(playerMovementsPath, pygame.Color("black"))
        player_image_rect = pygame.Rect(
            0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT
        )
        self.image: pygame.surface = self._sprite_sheet.image_at(player_image_rect)
        self.rect = self.image.get_rect(topleft=pos)
        # ensure hitbox is large enough to cover player rotations
        self._hitbox = self.rect.inflate(2, 0)

        self._obstacle_sprites = obstacle_sprites
        self.import_assets()

        # load player powers
        self._action_queue: list = []
        self._eaten_power = EatenPowers.empty_stomach

    @property
    def eaten_power(self) -> EatenPowers:
        """Get the current eaten power of the player.

        Returns
        -------
        eaten_power: EatenPowers
            The current EatenPowers enum value
        """
        return self._eaten_power

    @eaten_power.setter
    def eaten_power(self, new_value) -> None:
        """Set the new eaten power.

        Parameters
        ----------
        new_value: int
            Incoming value to set which must be an EatenPowers type

        Raises
        ------
        ValueError: new_value was not in EatenPowers enum
        """
        if isinstance(new_value, EatenPowers):
            self._eaten_power = new_value
        else:
            raise ValueError("Player can only consume eaten_power values.")

    def input(self) -> None:
        """Handle keyboard input to the player class.

        This method will handle turning the player object as input is received.
        """
        keys = pygame.key.get_pressed()

        # left/right input
        if keys[pygame.K_LEFT]:
            self._compass.rotate_ip(-PLAYER_ROTATION_SPEED)
        elif keys[pygame.K_RIGHT]:
            self._compass.rotate_ip(PLAYER_ROTATION_SPEED)

    def ensure_full_action_queue(self) -> None:
        """Fill up the current action queue up to a limit."""
        if len(self._action_queue) < MAX_ACTION_QUEUE_LENGTH:
            actions = [Actions.consume, Actions.destroy, Actions.throw]
            self._action_queue.append(random.choice(actions))

    def current_action(self) -> Actions:
        """Get the current action.

        Returns
        -------
        current_action: Actions
            The Actions enum value of the current action
        """
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

    def move(self, speed) -> None:
        """Player specific move function."""
        super().move(speed)
        # adjust the hitbox for optimal sprite coverage
        self._hitbox.centerx = self.rect.centerx + 1

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ) -> None:
        """Update player behavior based on player input.

        Controls and movement logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501
        Updates local good and bad sprites, handles user input,
        ensures full action queue, sets status by current rotation,
        gets next animation image, handles collisions, and moves the player

        Parameters
        ----------
        bad_sprites: pygame.sprite.Group
            The sprite group containing all bad aligned characters
        good_sprites: pygame.sprite.Group
            The sprite group containing all good aligned characters
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
        self.move(self._speed)
