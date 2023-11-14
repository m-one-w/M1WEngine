"""This module contains the Player class."""
import pygame
from entities.entity import Entity
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

    def __init__(self, pos, groups, obstacle_sprites):
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
        collision_count = {"left": 0, "right": 0, "up": 0, "down": 0}

        # get list of sprites from obstacleSprites
        obstacleSpritesList = self.obstacleSprites.sprites()

        # list of all obstacleSprite indicies player has collisions with
        collisions = self.rect.collidelistall(obstacleSpritesList)

        # if collisions are detected
        if collisions:
            for collisionIndex in collisions:
                collided_sprite = obstacleSpritesList[collisionIndex]
                # check status then add to appropriate collision direction
                if self.status == "up" or self.status == "down":
                    if collided_sprite.hitbox.centery < self.hitbox.centery:
                        collision_count["up"] += 1
                    elif collided_sprite.hitbox.centery > self.hitbox.centery:
                        collision_count["down"] += 1

                if self.status == "left" or self.status == "right":
                    if collided_sprite.hitbox.centerx < self.hitbox.centerx:
                        collision_count["left"] += 1
                    elif collided_sprite.hitbox.centerx > self.hitbox.centerx:
                        collision_count["right"] += 1

            # update self.direction based on direction with most collisions
            most_collided_direction = max(collision_count, key=collision_count.get)
            self.collision_update_direction(most_collided_direction)

    def collision_update_direction(self, collision_direction):
        """Change self.compass based off of the collision_direction.

        Parameters
        ----------
        collision_direction : str
            a string representing which direction the collision issue is taking place.
        """
        # change self.direction value
        if collision_direction == "up":
            self.compass.y = Direction.down.value
            self.status = "down"
        elif collision_direction == "down":
            self.compass.y = Direction.up.value
            self.status = "up"
        elif collision_direction == "left":
            self.compass.x = Direction.right.value
            self.status = "right"
        elif collision_direction == "right":
            self.compass.x = Direction.left.value
            self.status = "left"

    def update(self, enemy_sprites, friendly_sprites):
        """Update player behavior based on player input.

        Controls and movement logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501
        """
        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.input()
        self.set_status_by_curr_rotation()
        image = self.animate()
        self.image = self.set_image_rotation(image)
        # a new direction may be set by the collision handler
        self.collision_handler()
        # will move twice as fast as any other entity at the same speed due to camera.
        self.move(self.speed)
