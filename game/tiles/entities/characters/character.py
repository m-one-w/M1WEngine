"""This module contains the Character class."""
import math
import pygame
from enums.direction import Direction
from dict_structures.animation_dict import AnimationDict
from tiles.entities.entity import Entity
from score_controller import ScoreController
from tiles.tile import Tile

# number of images for each directional animation
WALKING_IMAGE_COUNT = 3


class Character(Entity):
    """Character class.

    Base class for all characters including player, enemies, and damsels.

    Attributes
    ----------
    _speed: int
        The speed at which the sprite moves
    _score_controller: ScoreController
        The score controller to track the score
    _obstacle_sprites: pygame.sprite.Group
        The sprite group containing all obstacles
    _bad_sprites: pygame.sprite.Group
        The sprite group containing all bad sprites
    _good_sprites: pygame.sprite.Group
        The sprite group containing all good sprites

    Methods
    -------
    speed(self) -> int
        Return _speed value
    speed(self, new_value: int) -> None
        Assign new value to _speed
    set_sprite_sheet(self, path: str)
        Create sprite sheet from path
    import_assets(self)
        Import animation strip and divide into smaller images
    animate(self) -> pygame.Surface
        Animation loop for character
    set_status_by_current_rotation(self)
        Set status per current direction
    get_angle_from_direction(self, axis: str) -> float
        Get the angle for sprite rotation based on compass direction
    get_distance(self, coords: tuple) -> float
        The hypotenuse of how far away the other character is from this character
    set_image_rotation(self, image: pygame.Surface) -> pygame.Surface
        Rotate image per compass direction
    collision_detection(self, sprite_group: pygame.sprite.Group) -> dict
        Get a dictionary of collided sprites.
    teleport_out_of_sprite(self, collision_rect: pygame.Rect)
        Move the sprite outside of the collision bounds of a collided sprite
    further_axis(self, coord: tuple) -> str
        Find if the given coordinate is further horizontally or vertically
    average_collision_coordinates(self, collision_coordinates: dict) -> tuple
        Get the average coordinates of all collisions from a dictionary of coordinates
    collision_handler(self)
        Handle the collision check for entities
    collision_set_compass(self, collided_coords: tuple)
        Bounce a compass off the wall collided with
    """

    def __init__(
        self,
        group: pygame.sprite.Group,
        pos: tuple,
        sprite_sheet_path: str,
        image_rect: pygame.Rect,
        obstacle_sprites: pygame.sprite.Group,
    ):
        """Initialize character class.

        Parameters
        ----------
        group: pygame.sprite.Group
            The sprite group this character is a part of
        pos: tuple
            The (x, y) position the character spawns at
        sprite_sheet_path: str
            The filepath where the sprite sheet is stored
        image_rect: pygame.Rect
            The rectangle representing the character
        obstacle_sprites: pygame.sprite.Group
            The sprite group containing all obstacle sprites
        """
        self.setup_import_assets(image_rect.height, image_rect.width)
        super().__init__(group, pos, sprite_sheet_path, image_rect)
        self._speed: int = 1
        self.compass.x: Direction = Direction.right
        self._score_controller: ScoreController = ScoreController()
        self._obstacle_sprites: pygame.sprite.Group = obstacle_sprites
        self._bad_sprites: pygame.sprite.Group
        self._good_sprites: pygame.sprite.Group

    @property
    def speed(self) -> int:
        """Return speed value."""
        return self._speed

    @speed.setter
    def speed(self, new_value: int) -> None:
        """Set the new speed value.

        Raises
        ------
        TypeError: new_value must be an int

        ValueError: speed must be at least 0
        """
        if type(new_value) is not int:
            raise TypeError("ERROR: speed must be of type int.")

        if new_value >= 0:
            self._speed = new_value
        else:
            raise ValueError("ERROR: speed cannot be less than 0.")

    def setup_import_assets(self, height, width) -> None:
        """Import and divide the animation image into it's smaller parts.

        Takes the image with all character animations and divides it into its
        sub-images.
        """
        animation_up: AnimationDict = {
            "name": "up",
            "image_rect": (
                0,
                height * 3,
                width,
                height,
            ),
            "image_count": 3,
        }
        animation_down: AnimationDict = {
            "name": "down",
            "image_rect": (0, 0, width, height),
            "image_count": 3,
        }
        animation_left: AnimationDict = {
            "name": "left",
            "image_rect": (
                0,
                height,
                width,
                height,
            ),
            "image_count": 3,
        }
        animation_right: AnimationDict = {
            "name": "right",
            "image_rect": (
                0,
                height * 2,
                width,
                height,
            ),
            "image_count": 3,
        }

        self._animation_dict = [
            animation_up,
            animation_down,
            animation_left,
            animation_right,
        ]

    def set_status_by_curr_rotation(self) -> None:
        """Set the correct status based on the current compass direction.

        This function inspects the current compass direction and determines
        what the status should be.
        """
        # handle all edge cases first
        if self.compass.y < 0:
            self._status = "up"
        else:
            self._status = "down"

        if self.compass.x < 0:
            self._status = "left"
        else:
            self._status = "right"

        # -- xy | xy +-
        # -+ xy | xy ++
        if self.compass.x > 0 and self.compass.y < 0.25 and self.compass.y > -0.25:
            self._status = "right"
        if self.compass.x < 0 and self.compass.y < 0.25 and self.compass.y > -0.25:
            self._status = "left"
        if self.compass.y > 0 and self.compass.x < 0.25 and self.compass.x > -0.25:
            self._status = "down"
        if self.compass.y < 0 and self.compass.x < 0.25 and self.compass.x > -0.25:
            self._status = "up"

    def get_angle_from_direction(self, axis: str) -> float:
        """Get the angle for sprite rotation based on the direction.

        Angle returned will need to be inverted for 'down' and 'left'.

        Parameters
        ----------
        axis: str
            The axis to inspect

        Returns
        -------
        angle: float
            The inverted angle from the compass
        """
        angle: float = 0.0

        if axis == "x":
            angle = self.compass.y * 45
        if axis == "y":
            angle = self.compass.x * 45

        return -angle

    def get_distance(self, coords: tuple) -> float:
        """Return the hypotenuse/distance away from another character.

        Parameters
        ----------
        coords: tuple
            The coordinates to compare our position with

        Returns
        -------
        hypotenuse: float
            The distance the coordinates are from this character
        """
        x: int = 0
        y: int = 1
        hypotenuse: float = math.hypot(
            coords[x] - self.rect[x], coords[y] - self.rect[y]
        )
        return hypotenuse

    def set_image_rotation(self, image: pygame.Surface) -> pygame.Surface:
        """Set an image to the correct orietation.

        Return the rotated image correlating to the correct rotation.
        Rotation is based on the status, so image rotations are defined by the
        current status.

        Parameters
        ----------
        image: pygame.Surface
            The animation image to rotate

        Returns
        -------
        rotated_image: pygame.Surface
            The rotated image passed into this method
        """
        angle: float = 0.0

        if self._status == "right":
            angle = self.get_angle_from_direction("x")
        if self._status == "left":
            angle = -self.get_angle_from_direction("x")
        if self._status == "up":
            angle = self.get_angle_from_direction("y")
        if self._status == "down":
            angle = -self.get_angle_from_direction("y")

        rotated_image: pygame.Surface = pygame.transform.rotate(image, angle)
        return rotated_image

    def collision_detection(self, sprite_group: pygame.sprite.Group) -> dict:
        """Get a dictionary of collision coordinates.

        Detect all the collisions between self and a sprite group, and
        return a dictionary of where those collisions occured.

        Parameters
        ----------
        sprite_group: pygame.sprite.Group
            The group of sprites to check for collisions against

        Returns
        -------
        sorted_collisions: dict[str, any]
            All the collision information between this sprite and a group.
        """
        # get list of sprites from the passed in sprite group
        obstacle_sprites: list = sprite_group.sprites()
        # extract list of rects from obstacle_sprites
        sprite_rects: list[pygame.Rect] = list()
        for sprite in obstacle_sprites:
            sprite_rects.append(sprite.rect)

        # list of all obstacle sprite indicies player has collisions with
        collision_indicies: list[int] = self.rect.collidelistall(obstacle_sprites)

        left_coords: list = []
        right_coords: list = []
        up_coords: list = []
        down_coords: list = []
        sorted_collisions: dict = {
            "collision_detected": False,
            "collision_x_avg": 0,
            "collision_y_avg": 0,
            "left": left_coords,
            "right": right_coords,
            "up": up_coords,
            "down": down_coords,
        }

        # if collisions are detected
        if collision_indicies:
            sorted_collisions["collision_detected"] = True
            for collision_index in collision_indicies:
                collided_sprite: Tile = obstacle_sprites[collision_index]
                collided_coord: tuple[int, int] = (
                    collided_sprite._hitbox.centerx,
                    collided_sprite._hitbox.centery,
                )
                # check status then add to appropriate collision direction
                if self.further_axis(collided_coord) == "vertical":
                    if collided_sprite._hitbox.centery < self.hitbox.centery:
                        sorted_collisions["up"].append(collided_coord)
                    elif collided_sprite._hitbox.centery > self.hitbox.centery:
                        sorted_collisions["down"].append(collided_coord)

                # if self.status == "left" or self.status == "right":
                if self.further_axis(collided_coord) == "horizontal":
                    if collided_sprite._hitbox.centerx < self.hitbox.centerx:
                        sorted_collisions["left"].append(collided_coord)
                    elif collided_sprite._hitbox.centerx > self.hitbox.centerx:
                        sorted_collisions["right"].append(collided_coord)

                # call method to teleport outside of collision sprite
                self.teleport_out_of_sprite(collided_sprite._hitbox)

        return sorted_collisions

    def teleport_out_of_sprite(self, collision_rect: pygame.Rect) -> None:
        """Remove self from the collided sprite's collision bounds.

        Parameters
        ----------
        collision_rect: pygame.Rect
            The hitbox of the sprite that was collided with
        """
        axis: str = self.further_axis((collision_rect.centerx, collision_rect.centery))

        if axis == "horizontal":
            x_dist_out_hitbox: int = 0
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
            y_dist_out_hitbox: int = 0
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

    def further_axis(self, coord: tuple) -> str:
        """Find the further axis.

        Parameters
        ----------
        coord: tuple
            A tuple with an X and Y coordinates to compare distances

        Returns
        -------
        further: str
            The string of the further axis away from our coords
        """
        distance_to_x: float = abs(self.rect.centerx - coord[0])
        distance_to_y: float = abs(self.rect.centery - coord[1])
        further: str = "vertical"
        if distance_to_x > distance_to_y:
            further = "horizontal"
        return further

    def average_collision_coordinates(self, collision_coordinates: dict) -> tuple:
        """Set the average coordinate in a dictionary of coordinates.

        Parameters
        ----------
        collision_coordinates: dict[str, any]
            All the collision coordinates information

        Returns
        -------
        average_collided_point: tuple
            The average collision point for all detected collisions
        """
        collision_point_x: int = 0
        collision_point_y: int = 0
        count: int = 0
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
            collision_point_x: int = collision_point_x / count
            collision_point_y: int = collision_point_y / count

        average_collided_point: tuple = (collision_point_x, collision_point_y)
        return average_collided_point

    def collision_handler(self) -> None:
        """Collision handler for entity.

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.
        """
        collision_dictionary: dict = self.collision_detection(self._obstacle_sprites)
        if collision_dictionary["collision_detected"]:
            collided_coords: tuple = self.average_collision_coordinates(
                collision_dictionary
            )
            self.collision_set_compass(collided_coords)

    def collision_set_compass(self, collided_coords: tuple) -> None:
        """Set the compass away from the position of the collision.

        Parameters
        ----------
        collided_coords: tuple
            A tuple containing the x and y of the average collision point
        """
        # used to flip x and y by the given amounts in the below vectors
        horizontal_reflect_vect: pygame.math.Vector2 = pygame.math.Vector2(
            Direction.right, 0
        )
        vertical_reflect_vect: pygame.math.Vector2 = pygame.math.Vector2(
            0, Direction.down
        )

        abs_distance_to_x: int = abs(self.rect.centerx - collided_coords[0])
        abs_distance_to_y: int = abs(self.rect.centery - collided_coords[1])
        distance_to_x: int = collided_coords[0] - self.rect.centerx
        distance_to_y: int = collided_coords[1] - self.rect.centery

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
