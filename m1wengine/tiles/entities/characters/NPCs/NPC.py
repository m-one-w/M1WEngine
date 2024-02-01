"""This module contains the Entity class."""

from enum import Enum
import math
import sys
import time
from typing import Callable
import pygame
from m1wengine.enums.actions import Actions
from m1wengine.enums.eaten_powers import EatenPowers
from m1wengine.enums.direction import Direction
from m1wengine.HUD import HeadsUpDisplay
from m1wengine.tiles.entities.characters.player import Player
from m1wengine.tiles.entities.characters.character import Character
import m1wengine.settings as settings
import m1wengine.prompt_strings as prompt_strings


class NPC(Character):
    """NPC class.

    Base class for all NPC entities including skeletons, damsels, and more.

    Attributes
    ----------
    _player: Character
        The player's character, tracked by each NPC
    _states: Enum
        The state machine for automated movement
    _current_state: states
        The current NPC state
    _initial_charge_compass: pygame.math.Vector2
        The vector of where we start the charge
    _hud: HeadsUpDisplay
        The handler for the HUD singleton
    _target_sprite: Entity
        The currently tracked sprite detected in radar
    DEFAULT_SPEED: int
        Default speed for an NPC
    DEFAULT_SPEED_FAST: int
        Default speed for a fast moving NPC
    DEFAULT_SPEED_ZERO: int
        Default speed for a stationary NPC
    DEFAULT_VECTOR2: pygame.Vector2
        Default vector2 for tracking a sprite
    DEFAULT_TIMER_VALUE: int
        Negative timer value for resetting initial tracking and charging
    TRACKING_TIMER: int
        The amount of time to spend tracking a target sprite
    _initial_tracking_time: int
        The starting time in seconds when tracking a target sprite
    _initial_charge_time: int
        The starting time in seconds when beginning a charge move
    _last_time_stored: int
        The last time an automated state used a timer
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
    default_movement(self)
        Do not move, intermediary state
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
    tracking_movement(self)
        Stop movement and track sprite on radar
    charge_movement(self)
        Charge self from current position at target sprite
    reset_charge_variables(self)
        Reset all variables relating to charge logic back to defaults
    is_timer_finished(self, initial_timer: int, timer_threshold_seconds: int) -> bool
        Check if timer has reached a threshold
    charged_into_obstacle(self) -> bool
        Check if obstacle sprite collision detected
    charged_into_good_sprite(self)
        Check for good sprite collision
    rotate_compass_to_target_sprite(self)
        Rotate the compass to point at the target sprite
    move_towards_target_sprite(self)
        Move to the target sprite
    set_state_default(self)
        Set state to default
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
    flip_current_image(self)
        Flip the current image
    """

    def __init__(
        self,
        group: pygame.sprite.Group,
        pos: tuple,
        sprite_sheet_path: str,
        image_rect: pygame.Rect,
        obstacle_sprites: pygame.sprite.Group,
    ) -> None:
        """Initialize NPC class.

        Parameters
        ----------
        group: pygame.sprite.Group
            The sprite group this NPC is part of
        pos: tuple
            The starting (x, y) coordinates for the NPC
        sprite_sheet_path: str
            The path to the sprite sheet image
        image_rect: pygame.Rect
            The size of the individual images in the sprite_sheet
        obstacle_sprites: pygame.sprite.Group
            The sprite group containing all obstacle sprites
        """
        super().__init__(group, pos, sprite_sheet_path, image_rect, obstacle_sprites)

        # init empty player
        self._player: Player = pygame.sprite.Sprite()

        # setting up state machine
        self._states: Enum = Enum(
            "states",
            [
                "Default",
                "Patrol",
                "Attack",
                "Flee",
                "Follow",
                "Thrown",
                "Tracking",
                "Charging",
            ],
        )
        self._current_state: Enum = self._states.Default
        self._initial_charge_compass: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self._hud = HeadsUpDisplay()

        # the closest sprite on our radar
        self._target_sprite: pygame.sprite.Sprite = pygame.sprite.Sprite()

        # default constants
        self.DEFAULT_SPEED: int = 1
        self.DEFAULT_SPEED_FAST: int = 5
        self.DEFAULT_SPEED_ZERO: int = 0
        self.DEFAULT_VECTOR2: pygame.Vector2 = pygame.Vector2(0, 0)
        self.DEFAULT_TIMER_VALUE: int = -1

        # vars for targetting and charging
        self.TRACKING_TIMER_SECONDS: int = 2
        self.CHARGING_TIMER_SECONDS: int = 3
        self._initial_tracking_time: int = self.DEFAULT_TIMER_VALUE
        self._initial_charge_time: int = self.DEFAULT_TIMER_VALUE

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
            collisions: bool = self._radar.colliderect(entity_rect_list)
        else:
            # sprites as a list of sprites, not a Group of sprites
            sprite_group_list: list[pygame.sprite.Sprite] = pygame.sprite.Group.sprites(
                entities
            )
            hitbox_list: list[pygame.Rect] = [
                sprite._hitbox for sprite in sprite_group_list
            ]
            # list of all NPC collisions
            collisions: bool = self._radar.collidelistall(hitbox_list)

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
            # try to track
            elif set_active_state == self.set_state_track:
                if self._current_state != self._states.Tracking:
                    set_active_state()
            # try to charge
            elif set_active_state == self.set_state_charge:
                if self._current_state != self._states.Charging:
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
        if self._current_state == self._states.Default:
            self.default_movement()

        elif self._current_state == self._states.Attack:
            self.attack_movement()

        elif self._current_state == self._states.Flee:
            self.flee_movement()

        elif self._current_state == self._states.Patrol:
            self.patrol_movement()

        elif self._current_state == self._states.Follow:
            self.follow_movement()

        elif self._current_state == self._states.Thrown:
            self.thrown_movement()

        elif self._current_state == self._states.Tracking:
            self.tracking_movement()

        # separate conditional because tracking may be over
        if self._current_state == self._states.Charging:
            self.charge_movement()

    def default_movement(self) -> None:
        """Behavior for default movement."""
        pass

    def patrol_movement(self) -> None:
        """Move back and forth."""
        if self._current_state == self._states.Patrol:
            current_time_in_seconds = time.perf_counter()

            # make sure speed is default
            if self.speed != self.DEFAULT_SPEED:
                self.speed = self.DEFAULT_SPEED

            if self.is_timer_finished(
                self._last_time_stored, timer_threshold_seconds=3
            ):
                # 10 seconds passed
                if self.compass.x != 1 or self.compass.x != 1:
                    self.compass.x = 1
                else:
                    self.compass.x *= -1
                self.compass.y = 0
                self._last_time_stored = current_time_in_seconds

            self.collision_handler()
            self.move(self.speed)

    def flee_movement(self) -> None:
        """Change direction based on where target is."""
        if self._current_state == self._states.Flee:
            if self.facing_towards_entity(self._target_sprite):
                # must set to copy or it gives the entity a shared compass
                self.compass = self._target_sprite.compass.copy()
                self.collision_handler()

            # move according to the compass direction
            self.move(self.speed)

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
        # if NPC is thrown long enough. TODO: make far enough (number of tiles)
        if self.is_timer_finished(self._last_time_stored, timer_threshold_seconds=1):
            self._current_state = self._states.Default
        else:
            collision_dictionary: dict = self.collision_detection(
                self._obstacle_sprites
            )
            if collision_dictionary["collision_detected"]:
                self.die()
            else:
                self.speed = self.DEFAULT_SPEED_FAST
                self.move(self.speed)
                self.flip_current_image()

    def tracking_movement(self) -> None:
        """Stop moving and track nearest entity."""
        # if we are in the tracking state
        if self._current_state == self._states.Tracking:
            # stop moving
            if self.speed != self.DEFAULT_SPEED_ZERO:
                self.speed = self.DEFAULT_SPEED_ZERO
            # rotate compass to target sprite
            self.rotate_compass_to_target_sprite()
            self._initial_charge_compass = self.compass.copy()

            # check if any good_sprites are on the tracker's radar
            collision_dictionary: dict = self.collision_detection(
                self._obstacle_sprites
            )

            # if there is a good_sprite on tracker's radar
            if collision_dictionary["collision_detected"]:
                # if first loop, set _initial_tracking_time
                if self._initial_tracking_time == self.DEFAULT_TIMER_VALUE:
                    self._initial_tracking_time = int(time.perf_counter())

                # if we've tracked the target long enough, switch to charge
                if self.is_timer_finished(
                    self._initial_tracking_time, self.TRACKING_TIMER_SECONDS
                ):
                    self.set_state_charge()
            # else nothing has hit the NPC rect, go back to patrolling
            else:
                self.reset_charge_variables()

    def charge_movement(self) -> None:
        """Charge from current position until charge is disrupted."""
        if self._current_state == self._states.Charging:
            # protect compass to prevent it from being overwritten
            self.compass = self._initial_charge_compass

            # if first loop, set _initial_charge_time
            if self._initial_charge_time == self.DEFAULT_TIMER_VALUE:
                self._initial_charge_time = int(time.perf_counter())

            # if NPC charges long enough or hit an obstacle, go back to default state
            if (
                self.is_timer_finished(
                    self._initial_charge_time, self.CHARGING_TIMER_SECONDS
                )
                or self.charged_into_obstacle()
            ):
                self.reset_charge_variables()
                self.set_state_default()
            else:
                # charge fast if first time in charge loop
                if self.speed == self.DEFAULT_SPEED or self.DEFAULT_SPEED_ZERO:
                    self.speed = self.DEFAULT_SPEED_FAST
                self.move(self.speed)

    def reset_charge_variables(self) -> None:
        """Reset all variables used in tracking and charging."""
        if self.speed != self.DEFAULT_SPEED:
            self.speed = self.DEFAULT_SPEED
        self._target_sprite = pygame.sprite.Sprite()
        self._initial_tracking_time = self.DEFAULT_TIMER_VALUE
        self._initial_charge_time = self.DEFAULT_TIMER_VALUE

    def is_timer_finished(
        self, initial_timer: int, timer_threshold_seconds: int
    ) -> bool:
        """Check that a time has elapsed based on current_time.

        Parameters
        ----------
        initial_timer: int
            The initial time, in seconds
        timer_threshold_seconds: int
            Number to seconds to be added to initial timer

        Raises
        ------
        ValueError: initial timer must not be default value (-1)
        """
        # timer validation
        if initial_timer == self.DEFAULT_TIMER_VALUE:
            raise ValueError("ERROR: initial timer still set to default.")
        # get current time
        current_time = int(time.perf_counter())
        if current_time >= initial_timer + timer_threshold_seconds:
            return True
        else:
            return False

    def charged_into_obstacle(self) -> bool:
        """Check if we collided with an obstacle sprite."""
        collision = False
        if self.collision_detection(self._obstacle_sprites, self._hitbox)[
            "collision_detected"
        ]:
            collision = True
        return collision

    def charged_into_good_sprite(self) -> bool:
        """Check if charging NPC has collided with a good_sprite."""
        collision = False
        if self.collision_detection(self._good_sprites, self._hitbox)[
            "collision_detected"
        ]:
            collision = True
        return collision

    def rotate_compass_to_target_sprite(self) -> None:
        """Rotate compass to point towards the target sprite."""
        if self._target_sprite is not None:
            opposite = self._target_sprite.rect.centerx - self.rect.centerx
            adjecent = self.rect.centery - self._target_sprite.rect.centery
            radians = math.atan2(opposite, adjecent)
            # compass direction must be facing up for rotate_ip_rad to work correctly
            self._compass.x = Direction.stop
            self._compass.y = Direction.up
            self._compass.rotate_ip_rad(radians)
        else:
            raise ValueError("ERROR: _target_sprite not set.")

    def move_towards_target_sprite(self) -> None:
        """Move towards the target sprite."""
        if self.rect.x < self._target_sprite.rect.x:
            self.move_right(self.speed)
        elif self.rect.x > self._target_sprite.rect.x:
            self.move_left(self.speed)

        if self.rect.y < self._target_sprite.rect.y:
            self.move_down(self.speed)
        elif self.rect.y > self._target_sprite.rect.y:
            self.move_up(self.speed)

        self.compass = self._target_sprite.compass.copy()

    def set_state_default(self) -> None:
        """Set state to intermediary state, reset variables."""
        self._current_state = self._states.Default

    def set_state_patrol(self) -> None:
        """Set state machine to 'Patrol'."""
        if self._current_state != self._states.Thrown and not self._states.Charging:
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
        self.compass = self._player.compass.copy()

    def set_state_track(self) -> None:
        """Set state machine to 'Tracking'."""
        if self._current_state == self._states.Patrol:
            self._current_state = self._states.Tracking

    def set_state_charge(self) -> None:
        """Set state machine to 'Charge'."""
        if self._current_state == self._states.Tracking:
            self._current_state = self._states.Charging

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

    def flip_current_image(self):
        """Spin the current image 180 degrees."""
        spin_angle = 180
        self.image = pygame.transform.rotate(self.image, spin_angle)
