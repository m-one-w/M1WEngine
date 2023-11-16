"""This module contains the Entity class."""
from enum import Enum
import math
import sys
import time
import pygame
from direction import Direction
from filemanagement.spriteSheet import SpriteSheet
from tile import Tile
import settings
from abc import (
    ABC,
    abstractmethod,
)


class Entity(Tile, ABC):
    """Entity abstract class.

    Base class for all entities including player, enemies, and damsels.

    Attributes
    ----------
    frameIndex : int
        The currently shown frame represented by an index
    animationSpeed : int
        The speed at which animations run
    speed : int
        The speed at which the sprite moves

    Methods
    -------
    set_sprite_sheet(self, path: str)
        Create sprite sheet from path
    import_assets(self)
        Import images into smaller images
    animate(self)
        Animation loop for entity
    set_status_by_current_rotation(self)
        Set status per current direction
    get_angle_from_direction(self, axis: str)
        Get the angle for sprite rotation per compass direction
    set_bad_sprites(self, bad_sprites: pygame.sprite.Group)
        Set the bad sprites group
    set_good_sprites(self, good_sprites: pygame.sprite.Group)
        Set the good sprites group
    set_image_rotation(self, image: pygame.Surface) -> pygame.Surface
        Rotate image per compass direction
    set_player(self, player: pygame.Sprite)
        Set the player
    collision_handler(self)
        Handle the collision check for entities
    """

    def __init__(self, groups):
        """Initialize base class."""
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.speed = 1
        self.compass.x = Direction.right.value
        self.status = "right"

        # damsels
        self.good_sprites = pygame.sprite.Group()
        # skeletons
        self.bad_sprites = pygame.sprite.Group()

        # init empty player
        self.player = pygame.sprite.Sprite()

        # setting up state machine
        self.states = Enum("skeleton_state", ["Patrol", "Attack", "Flee", "Follow"])
        self.current_state = self.states.Patrol

        # the skeleton is attacking
        self.sprite_to_attack = pygame.sprite.Sprite()

        # for automated movements, store a previous timestamp
        self.last_time_stored = 0

    def get_sprite_sheet(self, path: str):
        """Create sprite sheet from path."""
        return SpriteSheet(path)

    def import_assets(self):
        """Import and divide the animation image into it's smaller parts.

        Called at end of :func:'init()', takes the image with all character animations
        and divides it into its sub-images. Can be expanded with more images to fulfill
        idle and attack animations.
        """
        walkingUpRect = (
            0,
            settings.ENTITY_HEIGHT * 3,
            settings.ENTITY_WIDTH,
            settings.ENTITY_HEIGHT,
        )
        walkingDownRect = (0, 0, settings.ENTITY_WIDTH, settings.ENTITY_HEIGHT)
        walkingLeftRect = (
            0,
            settings.ENTITY_HEIGHT,
            settings.ENTITY_WIDTH,
            settings.ENTITY_HEIGHT,
        )
        walkingRightRect = (
            0,
            settings.ENTITY_HEIGHT * 2,
            settings.ENTITY_WIDTH,
            settings.ENTITY_HEIGHT,
        )

        # number of images for each directional animation
        IMAGE_COUNT = 3

        # animation states in dictionary
        self.animations = {
            "up": self.sprite_sheet.load_strip(walkingUpRect, IMAGE_COUNT),
            "down": self.sprite_sheet.load_strip(walkingDownRect, IMAGE_COUNT),
            "left": self.sprite_sheet.load_strip(walkingLeftRect, IMAGE_COUNT),
            "right": self.sprite_sheet.load_strip(walkingRightRect, IMAGE_COUNT),
        }

    def animate(self) -> pygame.Surface:
        """Animation loop for the entity.

        Loops through the images to show walking animation.
        Works for each cardinal direction.
        """
        animationStrip = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animationStrip):
            self.frameIndex = 0

        return animationStrip[int(self.frameIndex)]

    def set_status_by_curr_rotation(self):
        """Set the correct status based on the current direction.

        This function inspects the current direction and determines
        what the status should be.
        """
        # -- xy | xy +-
        # -+ xy | xy ++
        if self.compass.x > 0 and self.compass.y < 0.25 and self.compass.y > -0.25:
            self.status = "right"
        if self.compass.x < 0 and self.compass.y < 0.25 and self.compass.y > -0.25:
            self.status = "left"
        if self.compass.y > 0 and self.compass.x < 0.25 and self.compass.x > -0.25:
            self.status = "down"
        if self.compass.y < 0 and self.compass.x < 0.25 and self.compass.x > -0.25:
            self.status = "up"

    def get_angle_from_direction(self, axis):
        """Get the angle for sprite rotation based on the direction.

        Angle returned will need to be inverted for 'down' and 'left'.
        """
        angle = 0

        if axis == "x":
            angle = self.compass.y * 45
        if axis == "y":
            angle = self.compass.x * 45

        return -angle

    def set_bad_sprites(self, bad_sprites: pygame.sprite.Group):
        """Set bad_sprites."""
        self.bad_sprites = bad_sprites

    def set_good_sprites(self, good_sprites: pygame.sprite.Group):
        """Set good_sprites."""
        self.good_sprites = good_sprites

    def get_distance(self, coords: tuple) -> float:
        """Return the hypotenuse/distance away from another entity.

        Parameters
        ----------
        coords: tuple
            Coordinates of the entity we are testing
        """
        x = 0
        y = 1
        return math.hypot(coords[x] - self.rect[x], coords[y] - self.rect[y])

    def set_image_rotation(self, image):
        """Set a new image to the correct rotation.

        Return the rotated image correlating to the correct rotation.
        Rotation is based on the status, so image rotations are defined by the
        current status.
        """
        angle = 0

        if self.status == "right":
            angle = self.get_angle_from_direction("x")
        if self.status == "left":
            angle = -self.get_angle_from_direction("x")
        if self.status == "up":
            angle = self.get_angle_from_direction("y")
        if self.status == "down":
            angle = -self.get_angle_from_direction("y")

        return pygame.transform.rotate(image, angle)

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

    def radar_detect_player_entity(self, set_active_state, set_passive_state):
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

    def radar_detect_good_entities(self, set_active_state, set_passive_state):
        """Set state and selects which good_sprite to attack.

        Depending on what we detect on the radar, set the state of the skeleton.
        if good sprite is detected on radar, set state to "Attacking".
        """
        # good_sprites as a list of sprites, not a Group of sprites
        goodSpriteGroupList = self.good_sprites.sprites()
        # list of all damsel collisions
        collisions = self.radar.collidelistall(goodSpriteGroupList)

        # if there is an entity inside our radar
        if collisions:
            current_min_distance = float(sys.maxsize)
            indexOfClosest = -1

            # get list of rect tuple coordinates
            for collisionIndex in collisions:
                # get the coordinates of detected good_sprite
                coord = goodSpriteGroupList[collisionIndex].rect.center
                # distance between skeleton and entity on radar
                distance = self.get_distance(coord)
                # track if entity is closest to skeleton
                old_min = current_min_distance
                current_min_distance = min(distance, current_min_distance)
                # if current entity on radar is new closest entity
                if current_min_distance < old_min:
                    indexOfClosest = collisionIndex

            # set sprite_to_attack to closest sprite IF something detected
            if indexOfClosest != -1:
                self.sprite_to_attack = goodSpriteGroupList[indexOfClosest]
                if self.current_state != self.states.Attack:
                    # function for setting the active state
                    set_active_state()

        else:
            # else we are not attacking
            if self.current_state == self.states.Attack:
                # function for setting passive state
                set_passive_state()

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
                # must set to copy or it gives the skeleton a shared compass
                self.compass = self.player.compass.copy()

            # move according to the compass direction
            self.move(self.speed)

    def attack_movement(self):
        """Change compass based on where good_sprite is."""
        if self.current_state == self.states.Attack:
            if self.rect.x < self.sprite_to_attack.rect.x:
                self.move_right(self.speed)
            elif self.rect.x > self.sprite_to_attack.rect.x:
                self.move_left(self.speed)

            if self.rect.y < self.sprite_to_attack.rect.y:
                self.move_down(self.speed)
            elif self.rect.y > self.sprite_to_attack.rect.y:
                self.move_up(self.speed)

            self.compass = self.sprite_to_attack.compass.copy()

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
        """Set stae machine to 'Flee'."""
        self.current_state = self.states.Flee

    def set_player(self, player):
        """Set the player for the entity to track.

        Parameters
        ----------
        player: pygame.sprite
            Player sprite to track
        """
        self.player = player

    def facing_towards_entity(self, other_sprite):
        """Check if another sprite is looking at this sprite.

        Parameters
        ----------
        other_sprite: pygame.sprite
            the sprite to check against
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

    @abstractmethod
    def collision_handler(self):
        """Handle the collision check for entities.

        This method should be implemented in any child classes that use it.
        The method should handle the following:
        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.
        """
        raise Exception("Not Implemented")
