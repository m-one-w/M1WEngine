"""This module contains the Entity class."""

from enum import Enum
import sys
import time
from typing import Callable, List
import pygame
from enums.actions import Actions
from tiles.entities.entity import Entity
import settings


class NPC(Entity):
    """Entity abstract class.

    Base class for all NPC entities including skeletons, damsels, and more.

    Attributes
    ----------
    player: Entity
        The player character, tracked by each NPC
    states: Enum
        The state machine for automated movement
    current_state: states
        The current NPC state
    target_sprite: Entity
        The currently tracked sprite detected in radar
    last_time_stored: int
        The last time an automated state used a timer

    Methods
    -------
    radar_set_states(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    )
        Set the state on a radar detection of entities
    radar_set_state(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
    )
        Set the state on a radar detection of entities
    set_target_sprite_from_list(self, spriteGroupList: List, collisions: List)
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
    set_player(self, player: pygame.sprite)
        Set player for NPC to track
    facing_towards_entity(self, other_sprite: pygame.sprite)
        Determine if a sprite is facing towards another sprite
    teleport_out_of_sprite(self, collision_rect: pygame.Rect)
        Teleport out of a collided wall - NPC specific
    """

    def __init__(self, groups: pygame.sprite.Group):
        """Initialize NPC class."""
        super().__init__(groups)
        self.rect = pygame.Rect(0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT)

        # init empty player
        self.player: Entity = pygame.sprite.Sprite()

        # setting up state machine
        self.states = Enum("states", ["Patrol", "Attack", "Flee", "Follow"])
        self.current_state = self.states.Patrol

        # the closest sprite on our radar
        self.target_sprite = pygame.sprite.Sprite()

        # for automated movements, store a previous timestamp
        self.last_time_stored = 0

        # modify model rect to be a slightly less tall hitbox.
        # this will be used for movement.
        self.hitbox = self.rect.inflate(0, settings.ENTITY_HITBOX_OFFSET)
        # TODO: find sweet spot inflation size for radar detection
        inflation_size = 8
        self.radar = self.rect.inflate(
            settings.TILESIZE * inflation_size, settings.TILESIZE * inflation_size
        )

    def radar_set_states(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    ):
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
        collided = self.radar_set_state(entities, set_active_state)
        if not collided:
            # no radar hit and not in passive state
            if self.current_state != set_passive_state:
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
        """
        isPlayerCheck = entities.__class__.__name__ == "Player"

        if isPlayerCheck:
            collisions = self.radar.colliderect(entities)
        else:
            # sprites as a list of sprites, not a Group of sprites
            spriteGroupList = entities.sprites()
            hitbox_list = [sprite.hitbox for sprite in spriteGroupList]
            # list of all NPC collisions
            collisions = self.radar.collidelistall(hitbox_list)

        # if there is an entity inside our radar
        if collisions:
            if not isPlayerCheck:
                self.set_target_sprite_from_list(spriteGroupList, collisions)
            else:
                self.target_sprite = self.player

            # try to attack
            if set_active_state == self.set_state_attack:
                if self.current_state != self.states.Attack:
                    set_active_state()
            # try to flee
            elif set_active_state == self.set_state_flee:
                if self.current_state != self.states.Flee:
                    set_active_state()
            # try to follow
            elif set_active_state == self.set_state_follow:
                if self.current_state != self.states.Follow:
                    set_active_state()
            # cannot try to patrol as an active state
            elif set_active_state == self.set_state_patrol:
                raise Exception("Invalid active state of patrol has been found!")

        return collisions

    def set_target_sprite_from_list(self, spriteGroupList: List, collisions: List):
        """Set the target sprite from a radar collision.

        Parameters
        ----------
        sprite_group_list: List
            List of all sprites that might have collided
        collisions: List
            List of indices for which sprites have collided
        """
        current_min_distance = float(sys.maxsize)
        indexOfClosest = -1

        for collisionIndex in collisions:
            # get the coordinates of detected sprite
            coord = spriteGroupList[collisionIndex].rect.center
            # distance between self and the entity on radar
            distance = self.get_distance(coord)
            # track if entity is closest to self
            old_min = current_min_distance
            current_min_distance = min(distance, current_min_distance)
            # if current entity on radar is new closest entity
            if current_min_distance < old_min:
                indexOfClosest = collisionIndex

        # set target sprite to closest sprite IF something detected
        if indexOfClosest != -1:
            # some states will use a target sprite
            self.target_sprite = spriteGroupList[indexOfClosest]

    def move_based_on_state(self):
        """Logic to determine which _movement() method to call."""
        if self.current_state == self.states.Attack:
            self.attack_movement()

        elif self.current_state == self.states.Flee:
            self.flee_movement()

        elif self.current_state == self.states.Patrol:
            self.patrol_movement()

        elif self.current_state == self.states.Follow:
            self.follow_movement()

    def patrol_movement(self):
        """Move back and forth."""
        if self.current_state == self.states.Patrol:
            current_time_in_seconds = time.perf_counter()

            seconds_per_direction = 3
            if current_time_in_seconds - self.last_time_stored > seconds_per_direction:
                # 10 seconds passed
                if self.compass.x != 1 or self.compass.x != 1:
                    self.compass.x = 1
                else:
                    self.compass.x *= -1
                self.compass.y = 0
                self.last_time_stored = current_time_in_seconds

            self.collision_handler()
            self.move(self.speed)

    def flee_movement(self):
        """Change direction based on where player is."""
        if self.current_state == self.states.Flee:
            if self.facing_towards_entity(self.target_sprite):
                # must set to copy or it gives the entity a shared compass
                self.compass = self.target_sprite.compass.copy()
                self.collision_handler()

            # move according to the compass direction
            self.move(self.speed)

    def attack_movement(self):
        """Change compass based on where good_sprite is."""
        if self.current_state == self.states.Attack:
            self.move_towards_target_sprite()

    def follow_movement(self):
        """Follow behind another entity."""
        # TODO: only follow at a set distance
        if self.current_state == self.states.Follow:
            self.move_towards_target_sprite()

    def move_towards_target_sprite(self):
        """Move towards the target sprite."""
        if self.rect.x < self.target_sprite.rect.x:
            self.move_right(self.speed)
        elif self.rect.x > self.target_sprite.rect.x:
            self.move_left(self.speed)

        if self.rect.y < self.target_sprite.rect.y:
            self.move_down(self.speed)
        elif self.rect.y > self.target_sprite.rect.y:
            self.move_up(self.speed)

        self.compass = self.target_sprite.compass.copy()

    def set_state_patrol(self):
        """Set state machine to 'Patrol'."""
        self.current_state = self.states.Patrol

    def set_state_attack(self):
        """Set state machine to 'Attack'."""
        self.current_state = self.states.Attack

    def set_state_flee(self):
        """Set state machine to 'Flee'."""
        self.current_state = self.states.Flee

    def set_state_follow(self):
        """Set state machine to 'Follow'."""
        self.current_state = self.states.Follow

    def set_player(self, player: pygame.sprite):
        """Set the player for the entity to track.

        Parameters
        ----------
        player: pygame.sprite
            Player sprite to track
        """
        self.player = player

    def facing_towards_entity(self, other_sprite: pygame.sprite) -> bool:
        """Check if another sprite is looking at this sprite.

        Parameters
        ----------
        other_sprite: pygame.sprite
            The sprite to check against
        """
        is_same_direction = False

        # find greater distance, x or y
        delta_x = abs(self.rect.x - other_sprite.rect.x)
        delta_y = abs(self.rect.y - other_sprite.rect.y)

        # further left or right
        if delta_x >= delta_y:
            # current sprite is to the left
            if self.rect.x < other_sprite.rect.x:
                if other_sprite.status == "left":
                    is_same_direction = True
            else:
                if other_sprite.status == "right":
                    is_same_direction = True

        # further up or down
        if delta_y > delta_x:
            # current sprite is above
            if self.rect.y < other_sprite.rect.y:
                if other_sprite.status == "up":
                    is_same_direction = True
            else:
                if other_sprite.status == "down":
                    is_same_direction = True

        return is_same_direction

    def collision_set_compass(self, collided_coords: tuple):
        """Set the compass away from the position of the collision.

        Parameters
        ----------
        collided_coords: tuple
            A tuple containing the x and y of the average collision point
        """
        super().collision_set_compass(collided_coords)
        # TODO: time should be retrieved from levelManager
        self.last_time_stored = time.perf_counter()

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

        axis = self.further_axis((collision_rect.centerx, collision_rect.centery))

        if axis == "horizontal":
            # collided sprite is on the right
            if self.hitbox.centerx < collision_rect.centerx:
                # teleport to the left
                if collision_rect.left - (self.hitbox.right + 1) < 0:
                    self.move_left()
            # collided sprite is on the left
            else:
                # teleport to the right of the sprite
                if collision_rect.right - (self.hitbox.left - 1) > 0:
                    self.move_right()

        else:
            # collided sprite is below
            if self.hitbox.centery < collision_rect.centery:
                # teleport above the bottom of the sprite
                if collision_rect.top - (self.hitbox.bottom + 1) < 0:
                    self.move_up()
            # collided sprite is above
            else:
                # teleport below the top of the sprite
                if collision_rect.bottom - (self.hitbox.top - 1) > 0:
                    self.move_down()
