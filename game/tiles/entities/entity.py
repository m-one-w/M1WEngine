"""This module contains the Entity class."""
import math
import pygame
from direction import Direction
from filemanagement.spriteSheet import SpriteSheet
from scoreController import ScoreController
from tiles.tile import Tile
import settings


class Entity(Tile):
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
    collision_set_compass(self, collided_coords: tuple)
        Bounce a compass off the wall collided with
    """

    def __init__(self, groups: pygame.sprite.Group):
        """Initialize base class."""
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.speed = 1
        self.compass.x = Direction.right
        self.status = "right"
        self.scoreController = ScoreController()

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
            x_dist_out_hitbox = 0
            # collided sprite is on the right
            if self.hitbox.centerx < collision_rect.centerx:
                # teleport to the left
                if collision_rect.left - (self.hitbox.right + 1) < 0:
                    x_dist_out_hitbox = -1
            # collided sprite is on the left
            else:
                # teleport to the right of the sprite
                if collision_rect.right - (self.hitbox.left - 1) > 0:
                    x_dist_out_hitbox = 1

            if x_dist_out_hitbox != 0:
                self.rect.move_ip(x_dist_out_hitbox, 0)
        else:
            y_dist_out_hitbox = 0
            # collided sprite is below
            if self.hitbox.centery < collision_rect.centery:
                # teleport above the bottom of the sprite
                if collision_rect.top - (self.hitbox.bottom + 1) < 0:
                    y_dist_out_hitbox = -1
            # collided sprite is above
            else:
                # teleport below the top of the sprite
                if collision_rect.bottom - (self.hitbox.top - 1) > 0:
                    y_dist_out_hitbox = 1

            if y_dist_out_hitbox != 0:
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

    def collision_handler(self):
        """Collision handler for entity.

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.
        """
        collision_dictionary = self.collision_detection(self.obstacle_sprites)
        if collision_dictionary["collision_detected"]:
            collided_coords = self.average_collision_coordinates(collision_dictionary)
            self.collision_set_compass(collided_coords)

    def collision_set_compass(self, collided_coords: tuple):
        """Set the compass away from the position of the collision.

        Parameters
        ----------
        collided_coords: tuple
            A tuple containing the x and y of the average collision point
        """
        # used to flip x and y by the given amounts in the below vectors
        horizontal_reflect_vect = pygame.math.Vector2(Direction.right, 0)
        vertical_reflect_vect = pygame.math.Vector2(0, Direction.down)

        abs_distance_to_x = abs(self.rect.centerx - collided_coords[0])
        abs_distance_to_y = abs(self.rect.centery - collided_coords[1])
        distance_to_x = collided_coords[0] - self.rect.centerx
        distance_to_y = collided_coords[1] - self.rect.centery

        # if to the left or right
        if abs_distance_to_x > abs_distance_to_y:
            # if collided with sprite to the right of self
            if distance_to_x > 0:
                # if compass pointing right
                if self.compass.x > 0:
                    # bounce the compass off a horizontal vector
                    self.compass = self.compass.reflect(horizontal_reflect_vect)
            # if collided with sprite to the left of self
            else:
                # if compass pointing left
                if self.compass.x < 0:
                    # bounce the compass off a horizontal vector
                    self.compass = self.compass.reflect(horizontal_reflect_vect)

        # if up or down
        else:
            # if collided with sprite above self
            if distance_to_y < 0:
                # if compass pointing up
                if self.compass.y < 0:
                    # bounce the compass off a vertical vector
                    self.compass = self.compass.reflect(vertical_reflect_vect)
            # if collided with sprite below self
            else:
                # if compass pointing down
                if self.compass.y > 0:
                    # bounce the compass off a vertical vector
                    self.compass = self.compass.reflect(vertical_reflect_vect)
