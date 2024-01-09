"""This module contains the Entity class."""

from enum import Enum
import math
import sys
import time
from typing import Callable
import pygame
from enums.actions import Actions
from enums.eaten_powers import EatenPowers
from enums.direction import Direction
from HUD import HeadsUpDisplay
from tiles.entities.characters.character import Character
import settings
import prompt_strings


class NPC(Character):
    """NPC class.

    Base class for all NPC entities including skeletons, damsels, and more.

    Attributes
    ----------
    rect: pygame.Rect
        The size of the NPC
    _player: Character
        The player's character, tracked by each NPC
    _states: Enum
        The state machine for automated movement
    _current_state: states
        The current NPC state
    _target_sprite: Entity
        The currently tracked sprite detected in radar
    _last_time_stored: int
        The last time an automated state used a timer
    _hitbox: pygame.Rect
        A modified NPC rectangle used for collisions
    _radar: pygame.Rect
        The inflated rectangle used to detect other nearby Characters

    Methods
    -------
    radar_set_states(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    )
        Set the active and passive states based on stuff detected on radar
    radar_set_state(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
    ) -> bool
        Set the state on a radar detection of entities
    set_target_sprite_from_list(self, sprite_group_list: list, collisions: list)
        Choose a target sprite from a list of sprites
    move_based_on_state(self)
        Automatically move depending on the current state
    patrol_movement(self)
        Define the patrol movement
    flee_movement(self)
        Define the flee movement
    attack_movement(self)
        Define the attack movement
    follow_movement(self)
        Define the follow movement
    thrown_movement(self)
        Throw self from current position
    charge_movement(self)
        Charge self from current position
    rotate_compass_to_target_sprite(self)
        Rotate the compass to point at the target sprite
    move_towards_target_sprite(self)
        Move to the target sprite
    set_state_patrol(self)
        Set state to patrol
    set_state_attack(self)
        Set state to attack
    set_state_flee(self)
        Set state to flee
    set_state_follow(self)
        Set state to follow
    set_state_thrown(self)
        Set the state to thrown
    set_state_charge(self)
        Set the state to charge
    set_player(self, player: pygame.sprite)
        Set player for NPC to track
    collided_with_player(self)
        NPC actions on collision with player
    neutral_collided_with_player(self)
        Neutral sprite collision logic
    facing_towards_entity(self, other_sprite: pygame.sprite) -> bool
        Determine if another sprite is facing towards this sprite
    collision_set_compass(self, collided_coords: tuple)
        Set the compass away from the direction of the collision
    teleport_out_of_sprite(self, collision_rect: pygame.Rect)
        Teleport out of a collided wall - NPC specific
    """

    def __init__(
        self,
        group: pygame.sprite.Group,
        pos: tuple,
        sprite_sheet_path: str,
        image_rect: pygame.Rect,
    ):
        """Initialize NPC class.

        Parameters
        ----------
        group: pygame.sprite.Group
            The sprite group this NPC is part of
        """
        super().__init__(group, pos, sprite_sheet_path, image_rect)

        # init empty player
        self._player: Character = pygame.sprite.Sprite()

        # setting up state machine
        self._states: Enum = Enum(
            "states", ["Patrol", "Attack", "Flee", "Follow", "Thrown", "Charge"]
        )
        self._current_state: Enum = self._states.Patrol
        self._initial_charge_compass: pygame.Vector2 = pygame.Vector2(0, 0)
        self._hud = HeadsUpDisplay()

        # the closest sprite on our radar
        self._target_sprite: Character = pygame.sprite.Sprite()

        # for automated movements, store a previous timestamp
        self._last_time_stored: int = 0

        # TODO: find sweet spot inflation size for radar detection
        inflation_size: int = 8
        self._radar: pygame.Rect = self.rect.inflate(
            settings.TILESIZE * inflation_size, settings.TILESIZE * inflation_size
        )
        self._player_collision_resolved = True

    def radar_set_states(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    ) -> None:
        """Set state and selects which sprite to apply an active state to.

        Depending on what we detect on the radar, set the state of the NPC.

        Parameters
        ----------
        entities: pygame.sprite.Group
            Either the player, or any sprite group
        set_active_state: type(Callable[[], None])
            The new active state to set
        set_passive_state: type(Callable[[], None])
            The new passive state to set
        """
        collided: bool = self.radar_set_state(entities, set_active_state)
        if not collided:
            # no radar hit and not in passive state
            if self._current_state != set_passive_state:
                set_passive_state()

    def radar_set_state(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
    ) -> bool:
        """Set state and selects which sprite to apply an active state to.

        Depending on what we detect on the radar, set the state of the NPC.

        Parameters
        ----------
        entities: pygame.sprite.Group
            Either the player, or any sprite group
        set_active_state: type(Callable[[], None])
            The new active state to set

        Returns
        -------
        collisions: bool
            The flag for whether a collision was detected

        Raises
        ------
        Exception:
            Invalid active state
        """
        is_player: bool = entities.__class__.__name__ == "Player"

        if is_player:
            # if is_player, then entities is a single sprite
            entity_rect_list: list[pygame.sprite.Sprite] = entities
            collisions = self._radar.colliderect(entity_rect_list)
        else:
            # sprites as a list of sprites, not a Group of sprites
            sprite_group_list: list[pygame.sprite.Sprite] = pygame.sprite.Group.sprites(
                entities
            )
            hitbox_list: list[int] = [sprite._hitbox for sprite in sprite_group_list]
            # list of all NPC collisions
            collisions = self._radar.collidelistall(hitbox_list)

        # if there is an entity inside our radar
        if collisions and self._current_state != self._states.Thrown:
            if not is_player:
                self.set_target_sprite_from_list(sprite_group_list, collisions)
            else:
                self._target_sprite = self._player

            # try to attack
            if set_active_state == self.set_state_attack:
                if self._current_state != self._states.Attack:
                    set_active_state()
            # try to flee
            elif set_active_state == self.set_state_flee:
                if self._current_state != self._states.Flee:
                    set_active_state()
            # try to follow
            elif set_active_state == self.set_state_follow:
                if self._current_state != self._states.Follow:
                    set_active_state()
            # try to charge
            elif set_active_state == self.set_state_charge:
                if self._current_state != self._states.Flee:
                    set_active_state()
            # cannot try to patrol as an active state
            elif set_active_state == self.set_state_patrol:
                raise Exception("Invalid active state of patrol has been found!")

        return collisions

    def set_target_sprite_from_list(
        self, sprite_group_list: list, collisions: list[int]
    ) -> None:
        """Set the target sprite from a radar collision.

        Parameters
        ----------
        sprite_group_list: list
            List of all sprites that might have collided
        collisions: list[int]
            List of indices for which sprites have collided
        """
        current_min_distance: float = float(sys.maxsize)
        index_of_closest: int = -1

        for collision_index in collisions:
            # get the coordinates of detected sprite
            coord: tuple = sprite_group_list[collision_index].rect.center
            # distance between self and the entity on radar
            distance: float = self.get_distance(coord)
            # track if entity is closest to self
            old_min: float = current_min_distance
            current_min_distance = min(distance, current_min_distance)
            # if current entity on radar is new closest entity
            if current_min_distance < old_min:
                index_of_closest = collision_index

        # set target sprite to closest sprite IF something detected
        if index_of_closest != -1:
            # some states will use a target sprite
            self._target_sprite = sprite_group_list[index_of_closest]

    def move_based_on_state(self) -> None:
        """Logic to determine which _movement() method to call."""
        if self._current_state == self._states.Attack:
            self.attack_movement()

        elif self._current_state == self._states.Flee:
            self.flee_movement()

        elif self._current_state == self._states.Patrol:
            self.patrol_movement()

        elif self._current_state == self._states.Follow:
            self.follow_movement()

        elif self._current_state == self._states.Thrown:
            self.thrown_movement()

        elif self._current_state == self._states.Charge:
            self.charge_movement()

    def patrol_movement(self) -> None:
        """Move back and forth."""
        if self._current_state == self._states.Patrol:
            current_time_in_seconds = time.perf_counter()

            seconds_per_direction: int = 3
            if current_time_in_seconds - self._last_time_stored > seconds_per_direction:
                # 10 seconds passed
                if self._compass.x != 1 or self._compass.x != 1:
                    self._compass.x = 1
                else:
                    self._compass.x *= -1
                self._compass.y = 0
                self._last_time_stored = current_time_in_seconds

            self.collision_handler()
            self.move(self._speed)

    def flee_movement(self) -> None:
        """Change direction based on where target is."""
        if self._current_state == self._states.Flee:
            if self.facing_towards_entity(self._target_sprite):
                # must set to copy or it gives the entity a shared compass
                self._compass = self._target_sprite._compass.copy()
                self.collision_handler()

            # move according to the compass direction
            self.move(self._speed)

    def attack_movement(self) -> None:
        """Change compass based on where target sprite is."""
        if self._current_state == self._states.Attack:
            self.move_towards_target_sprite()

    def follow_movement(self) -> None:
        """Follow behind another entity."""
        # TODO: only follow at a set distance
        if self._current_state == self._states.Follow:
            self.move_towards_target_sprite()

    def thrown_movement(self) -> None:
        """Get thrown from current position."""
        # TODO: move to game counter
        current_time_in_seconds: float = time.perf_counter()

        seconds_per_throw: int = 1
        if current_time_in_seconds - self._last_time_stored > seconds_per_throw:
            self._current_state = self._states.Patrol
        else:
            collision_dictionary: dict = self.collision_detection(
                self._obstacle_sprites
            )
            if collision_dictionary["collision_detected"]:
                self.die()
            else:
                speed: int = 5
                self.move(speed)

    def charge_movement(self) -> None:
        """Charge from current position until charge is disrupted."""
        if self._current_state == self._states.Charge:
            if self._initial_charge_compass == pygame.Vector2(0, 0):
                self._initial_charge_compass = self.rotate_compass_to_target_sprite()

            collision_dictionary: dict = self.collision_detection(
                self._obstacle_sprites
            )
            if collision_dictionary["collision_detected"]:
                self._initial_charge_compass = pygame.Vector2(0, 0)
                self.set_state_patrol()
            else:
                speed: int = 2
                self.move(speed)

    def rotate_compass_to_target_sprite(self) -> None:
        """Rotate compass to point towards the target sprite."""
        opposite = self._target_sprite.rect.centerx - self.rect.centerx
        adjecent = self.rect.centery - self._target_sprite.rect.centery
        radians = math.atan2(opposite, adjecent)
        self._compass.x = Direction.stop
        self._compass.y = Direction.down
        self._compass.rotate_ip_rad(radians)

    def move_towards_target_sprite(self) -> None:
        """Move towards the target sprite."""
        if self.rect.x < self._target_sprite.rect.x:
            self.move_right(self._speed)
        elif self.rect.x > self._target_sprite.rect.x:
            self.move_left(self._speed)

        if self.rect.y < self._target_sprite.rect.y:
            self.move_down(self._speed)
        elif self.rect.y > self._target_sprite.rect.y:
            self.move_up(self._speed)

        self._compass = self._target_sprite._compass.copy()

    def set_state_patrol(self) -> None:
        """Set state machine to 'Patrol'."""
        if self._current_state != self._states.Thrown:
            self._current_state = self._states.Patrol

    def set_state_attack(self) -> None:
        """Set state machine to 'Attack'."""
        if self._current_state != self._states.Thrown:
            self._current_state = self._states.Attack

    def set_state_flee(self) -> None:
        """Set state machine to 'Flee'."""
        self._current_state = self._states.Flee

    def set_state_follow(self) -> None:
        """Set state machine to 'Follow'."""
        if self._current_state != self._states.Thrown:
            self._current_state = self._states.Follow

    def set_state_thrown(self) -> None:
        """Set state machine to 'Thrown'."""
        self._current_state = self._states.Thrown
        # TODO: switch to game clock
        self._last_time_stored = time.perf_counter()
        self._compass = self._player._compass.copy()

    def set_state_charge(self) -> None:
        """Set state machine the 'Charge'."""
        if self._current_state != self._states.Thrown:
            self._current_state = self._states.Charge

    def set_player(self, player: pygame.sprite) -> None:
        """Set the player for the entity to track.

        Parameters
        ----------
        player: pygame.sprite
            Player sprite to track
        """
        self._player = player

    def collided_with_player(self) -> None:
        """Go through player action when colliding with a player.

        Raises
        ------
        ValueError: Cannot set player consume attribute
        """
        if self._current_state != self._states.Thrown:
            current_player_action: Actions = self._player.pop_next_player_action()
            if current_player_action == Actions.destroy:
                self.die()
            elif current_player_action == Actions.consume:
                self.die()
                # TODO: make consume logic
                # set player consumption attribute with setter
                child_class: str = self.__class__.__name__
                if child_class == "Skeleton":
                    self._player.eaten_power = EatenPowers.basic_skeleton
                elif child_class == "Damsel":
                    self._player.eaten_power = EatenPowers.damsel
                else:
                    raise ValueError(
                        "Unknown caller, cannot set player consume attribute."
                    )
            elif current_player_action == Actions.throw:
                self.set_state_thrown()

    def neutral_collided_with_player(self):
        """Player has collided with a neutral sprite."""
        self._hud.start_prompt_timer()
        child_class: str = self.__class__.__name__

        prompt_text: str = prompt_strings.npc_prompts[child_class]["hint_text"]
        self._hud.level_hint = prompt_text

    def facing_towards_entity(self, other_sprite: pygame.sprite) -> bool:
        """Check if another sprite is looking at this sprite.

        Parameters
        ----------
        other_sprite: pygame.sprite
            The sprite to check against

        Returns
        -------
        is_same_direction: bool
            The boolean value of entity is facing towards this entity
        """
        is_same_direction: bool = False

        # find greater distance, x or y
        delta_x: float = abs(self.rect.x - other_sprite.rect.x)
        delta_y: float = abs(self.rect.y - other_sprite.rect.y)

        # further left or right
        if delta_x >= delta_y:
            # current sprite is to the left
            if self.rect.x < other_sprite.rect.x:
                if other_sprite._status == "left":
                    is_same_direction = True
            else:
                if other_sprite._status == "right":
                    is_same_direction = True

        # further up or down
        if delta_y > delta_x:
            # current sprite is above
            if self.rect.y < other_sprite.rect.y:
                if other_sprite._status == "up":
                    is_same_direction = True
            else:
                if other_sprite._status == "down":
                    is_same_direction = True

        return is_same_direction

    def collision_set_compass(self, collided_coords: tuple) -> None:
        """Set the compass away from the position of the collision.

        Parameters
        ----------
        collided_coords: tuple
            A tuple containing the x and y of the average collision point
        """
        super().collision_set_compass(collided_coords)
        # TODO: time should be retrieved from level_manager
        self._last_time_stored = time.perf_counter()

    def teleport_out_of_sprite(self, collision_rect: pygame.Rect):
        """Remove self from the collided sprite's collision bounds.

        The NPC version of this method must adjust the compass when moving out
        of walls in order for the automated movement to work as expected.

        Parameters
        ----------
        collision_rect: pygame.Rect
            The hitbox of the sprite that was collided with
        """
        # check if still within bounds,
        # might not be from prev calls

        axis: str = self.further_axis((collision_rect.centerx, collision_rect.centery))

        if axis == "horizontal":
            # collided sprite is on the right
            if self._hitbox.centerx < collision_rect.centerx:
                # teleport to the left
                if collision_rect.left - (self._hitbox.right + 1) < 0:
                    self.move_left()
            # collided sprite is on the left
            else:
                # teleport to the right of the sprite
                if collision_rect.right - (self._hitbox.left - 1) > 0:
                    self.move_right()

        else:
            # collided sprite is below
            if self._hitbox.centery < collision_rect.centery:
                # teleport above the bottom of the sprite
                if collision_rect.top - (self._hitbox.bottom + 1) < 0:
                    self.move_up()
            # collided sprite is above
            else:
                # teleport below the top of the sprite
                if collision_rect.bottom - (self._hitbox.top - 1) > 0:
                    self.move_down()
