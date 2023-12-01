"""This module contains the Entity class."""

from enum import Enum
import sys
import time
from typing import Callable
import pygame
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
    radar_detect_entities(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    )
        Set the state on a radar detection of entities
    radar_detect_player_entity(
        self,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    )
        Set a state on a radar detection of the player
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
    """

    def __init__(self, groups: pygame.sprite.Group):
        """Initialize NPC class."""
        super().__init__(groups)
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

    def radar_detect_entities(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    ):
        """Set state and selects which sprite to apply an active state to.

        Depending on what we detect on the radar, set the state of the NPC.
        """
        # sprites as a list of sprites, not a Group of sprites
        spriteGroupList = entities.sprites()
        # list of all NPC collisions
        collisions = self.radar.collidelistall(spriteGroupList)

        # if there is an entity inside our radar
        if collisions:
            current_min_distance = float(sys.maxsize)
            indexOfClosest = -1

            # get list of rect tuple coordinates
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
                self.target_sprite = spriteGroupList[indexOfClosest]
                if self.current_state != self.states.Attack:
                    # function for setting the active state
                    set_active_state()

        else:
            # else we are not attacking
            if self.current_state == self.states.Attack:
                # function for setting passive state
                set_passive_state()

    def radar_detect_player_entity(
        self,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    ):
        """Check whether player is within our radar."""
        # set state to 'Flee' if player detected
        collision = self.radar.colliderect(self.player)
        # if player on radar, set state
        if collision:
            if self.current_state != self.states.Flee:
                # set state when player detected
                set_active_state()
        else:
            if (
                self.current_state != self.states.Attack
                and self.current_state != self.states.Patrol
            ):
                # set state when no player detected
                set_passive_state()

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

            self.move(self.speed)

    def flee_movement(self):
        """Change direction based on where player is."""
        if self.current_state == self.states.Flee:
            if self.facing_towards_entity(self.player):
                # must set to copy or it gives the entity a shared compass
                self.compass = self.player.compass.copy()

            # move according to the compass direction
            self.move(self.speed)

    def attack_movement(self):
        """Change compass based on where good_sprite is."""
        if self.current_state == self.states.Attack:
            if self.rect.x < self.target_sprite.rect.x:
                self.move_right(self.speed)
            elif self.rect.x > self.target_sprite.rect.x:
                self.move_left(self.speed)

            if self.rect.y < self.target_sprite.rect.y:
                self.move_down(self.speed)
            elif self.rect.y > self.target_sprite.rect.y:
                self.move_up(self.speed)

            self.compass = self.target_sprite.compass.copy()

    def follow_movement(self):
        """Follow behind another entity."""
        # TODO: implement
        return

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
