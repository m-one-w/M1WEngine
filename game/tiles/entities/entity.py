"""This module contains the Entity class."""
from enum import Enum
import math
import sys
import time
from typing import Callable
import pygame
from direction import Direction
from filemanagement.spriteSheet import SpriteSheet
from tiles.tile import Tile
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
    frameIndex: int
        The currently shown frame represented by an index
    animationSpeed: int
        The speed at which animations run
    speed: int
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
    collision_detection(self, sprite_group: pygame.sprite.Group) -> dict
        Get a dictionary of collided sprites.
    teleport_out_of_sprite(self, collision_rect: pygame.Rect)
        Move the sprite outside of the collision bounds of a collided sprite
    further_axis(self, coord: tuple) -> str
        Find if the given coordinate is further horizontally or vertically
    average_collision_coordinates(self, collision_coordinates: dict) -> tuple
        Get the average coordinates from a dictionary of coordinates
    collision_handler(self)
        Handle the collision check for entities
    """

    def __init__(self, groups: pygame.sprite.Group):
        """Initialize base class."""
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.speed = 1
        self.compass.x = Direction.right
        self.status = "right"

        # init empty player
        self.player = pygame.sprite.Sprite()

        # setting up state machine
        self.states = Enum("states", ["Patrol", "Attack", "Flee", "Follow"])
        self.current_state = self.states.Patrol

        # the closest sprite on our radar
        self.target_sprite = pygame.sprite.Sprite()

        # for automated movements, store a previous timestamp
        self.last_time_stored = 0

    def get_sprite_sheet(self, path: str) -> SpriteSheet:
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
        # handle all edge cases first
        if self.compass.y < 0:
            self.status = "up"
        else:
            self.status = "down"

        if self.compass.x < 0:
            self.status = "left"
        else:
            self.status = "right"

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

    def get_angle_from_direction(self, axis: str) -> float:
        """Get the angle for sprite rotation based on the direction.

        Angle returned will need to be inverted for 'down' and 'left'.
        """
        angle = 0.0

        if axis == "x":
            angle = self.compass.y * 45
        if axis == "y":
            angle = self.compass.x * 45

        return -angle

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

    def set_image_rotation(self, image: pygame.Surface) -> pygame.Surface:
        """Set a new image to the correct rotation.

        Return the rotated image correlating to the correct rotation.
        Rotation is based on the status, so image rotations are defined by the
        current status.

        Parameters
        ----------
        image: pygame.Surface
            The animation image to rotate
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

    def radar_detect_entities(
        self,
        entities: pygame.sprite.Group,
        set_active_state: type(Callable[[], None]),
        set_passive_state: type(Callable[[], None]),
    ):
        """Set state and selects which good_sprite to attack.

        Depending on what we detect on the radar, set the state of the skeleton.
        if good sprite is detected on radar, set state to "Attacking".
        """
        # good_sprites as a list of sprites, not a Group of sprites
        spriteGroupList = entities.sprites()
        # list of all damsel collisions
        collisions = self.radar.collidelistall(spriteGroupList)

        # if there is an entity inside our radar
        if collisions:
            current_min_distance = float(sys.maxsize)
            indexOfClosest = -1

            # get list of rect tuple coordinates
            for collisionIndex in collisions:
                # get the coordinates of detected good_sprite
                coord = spriteGroupList[collisionIndex].rect.center
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
                self.target_sprite = spriteGroupList[indexOfClosest]
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

    def collision_detection(self, sprite_group: pygame.sprite.Group) -> dict:
        """Get a dictionary of collision coordinates.

        Detect all the collisions between self and a sprite group, and
        return a dictionary of where those collisions occured.

        Parameters
        ----------
        sprite_group: pygame.sprite.Group
            the group of sprites to check for collisions against

        Returns a dictionary containing all the collision coordinates between
        a sprite and a group.
        """
        # get list of sprites from the passed in sprite group
        obstacleSpritesList = sprite_group.sprites()

        # list of all obstacleSprite indicies player has collisions with
        collisions = self.rect.collidelistall(obstacleSpritesList)

        left_coords = []
        right_coords = []
        up_coords = []
        down_coords = []
        coords = {
            "collision_detected": False,
            "collision_x_avg": 0,
            "collision_y_avg": 0,
            "left": left_coords,
            "right": right_coords,
            "up": up_coords,
            "down": down_coords,
        }

        # if collisions are detected
        if collisions:
            coords["collision_detected"] = True
            for collisionIndex in collisions:
                collided_sprite: Tile = obstacleSpritesList[collisionIndex]
                collided_coord = (
                    collided_sprite.hitbox.centerx,
                    collided_sprite.hitbox.centery,
                )
                # check status then add to appropriate collision direction
                if self.further_axis(collided_coord) == "vertical":
                    if collided_sprite.hitbox.centery < self.hitbox.centery:
                        coords["up"].append(collided_coord)
                    elif collided_sprite.hitbox.centery > self.hitbox.centery:
                        coords["down"].append(collided_coord)

                # if self.status == "left" or self.status == "right":
                if self.further_axis(collided_coord) == "horizontal":
                    if collided_sprite.hitbox.centerx < self.hitbox.centerx:
                        coords["left"].append(collided_coord)
                    elif collided_sprite.hitbox.centerx > self.hitbox.centerx:
                        coords["right"].append(collided_coord)

                # call method to teleport outside of collision sprite
                self.teleport_out_of_sprite(collided_sprite.hitbox)

        return coords

    def teleport_out_of_sprite(self, collision_rect: pygame.Rect):
        """Remove self from the collided sprite's collision bounds.

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
                x_dist_out_hitbox = collision_rect.left - (self.hitbox.right + 1)
                self.rect.move_ip(x_dist_out_hitbox, 0)
            # collided sprite is on the left
            else:
                # teleport to the right of the sprite
                x_dist_out_hitbox = collision_rect.right - (self.hitbox.left - 1)
                self.rect.move_ip(x_dist_out_hitbox, 0)
        else:
            # collided sprite is below
            if self.hitbox.centery < collision_rect.centery:
                # teleport below the bottom of the sprite
                y_dist_out_hitbox = collision_rect.top - (self.hitbox.bottom + 1)
                self.rect.move_ip(0, y_dist_out_hitbox)
            # collided sprite is above
            else:
                # teleport above the top of the sprite
                y_dist_out_hitbox = collision_rect.bottom - (self.hitbox.top - 1)
                self.rect.move_ip(0, y_dist_out_hitbox)

        return

    def further_axis(self, coord: tuple) -> str:
        """Find the further axis.

        Parameters
        ----------
        coord: tuple
            A tuple with an X and Y coordinate stored.
        """
        distance_to_x = abs(self.rect.centerx - coord[0])
        distance_to_y = abs(self.rect.centery - coord[1])
        further = "vertical"
        if distance_to_x > distance_to_y:
            further = "horizontal"
        return further

    def average_collision_coordinates(self, collision_coordinates: dict) -> tuple:
        """Set the average coordinate in a dictionary of coordinates.

        Parameters
        ----------
        collision_coordinates: pygame.sprite.Group
            a dictionary containing all the collision coordinates between
            a sprite and a group.

        Returns the same dictionary with updated average collision coordinates.
        """
        collision_point_x = 0
        collision_point_y = 0
        count = 0
        for key in collision_coordinates:
            # meta data starts with 'collision', ignore this
            if "collision" not in key:
                coord_tuple_list: list = collision_coordinates[key]

                for coord_tuple in coord_tuple_list:
                    count += 1
                    # sum all collision
                    collision_point_x += coord_tuple[0]
                    collision_point_y += coord_tuple[1]

        # divide by number of collisions
        if count != 0:
            collision_point_x = collision_point_x / count
            collision_point_y = collision_point_y / count

        return (collision_point_x, collision_point_y)

    @abstractmethod
    def collision_handler(self):
        """Handle the collision check for entities.

        This method should be implemented in any child classes that use it.
        The method should handle the following:
        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.
        """
        raise Exception("Not Implemented")
