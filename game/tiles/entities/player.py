"""This module contains the Player class."""
import pygame
from tiles.entities.entity import Entity
from direction import Direction
import settings

# Defines how fast the player object can rotate while running
PLAYER_ROTATION_SPEED = 5


class Player(Entity):
    """Player class which contains the object players will directly control.

    The player class will handle movement logic and sprite changing logic for the player
    object. The player class will also handle any collision logic that influences the
    player object.
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
        self.image = self.sprite_sheet.image_at(playerSelfImageRect)
        self.setColorKeyBlack()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, settings.ENTITY_HITBOX_OFFSET)

        # speed can be any integer
        self.attacking = False
        self.attackCooldown = 400
        self.attackTime = 0

        self.obstacleSprites = obstacle_sprites
        self.import_assets()

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

    def collision_handler(self):
        """Collision handler for entity.

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.
        """
        collision_dictionary = self.collision_detection(self.obstacleSprites)
        if collision_dictionary["collision_detected"]:
            collided_coords = self.average_collision_coordinates(collision_dictionary)
            self.collision_set_compass(collided_coords)
            self.set_status_by_curr_rotation()
            image = self.animate()
            self.image = self.set_image_rotation(image)

    def collision_set_compass(self, collided_coords: tuple):
        """Set the compass away from the position of the collision.

        Parameters
        ----------
        collided_coords: tuple
            a tuple containing the x and y of the average collision point
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

    def update(
        self, bad_sprites: pygame.sprite.Group, good_sprites: pygame.sprite.Group
    ):
        """Update player behavior based on player input.

        Controls and movement logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501
        """
        self._bad_sprites = bad_sprites
        self._good_sprites = good_sprites
        self.input()
        self.set_status_by_curr_rotation()
        image = self.animate()
        self.image = self.set_image_rotation(image)
        # a new direction may be set by the collision handler
        self.collision_handler()
        # will move twice as fast as any other entity at the same speed due to camera.
        self.move(self.speed)
