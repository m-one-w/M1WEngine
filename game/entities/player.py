import pygame
from entities.entity import Entity
from filemanagement.spriteSheet import SpriteSheet
from direction import Direction

# Defines how fast the player object can rotate while running
PLAYER_ROTATION_SPEED = 5

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20

# modify model rect to have slightly less tall hitbox. Used for movement
SPRITE_HITBOX_OFFSET = -26


class Player(Entity):

    """Player class which contains the object players will directly control

    The player class will handle movement logic and sprite changing logic for the player
    object. The player class will also handle any collision logic that influences the
    player object.

    """

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # grab self image
        playerMovementsPath = "graphics/player/playerWalking.png"
        self.playerAnimations = SpriteSheet(playerMovementsPath)
        playerSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.image = self.playerAnimations.image_at(playerSelfImageRect)
        self.setColorKeyBlack()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, SPRITE_HITBOX_OFFSET)

        # speed can be any integer
        self.attacking = False
        self.attackCooldown = 400
        self.attackTime = 0

        self.obstacleSprites = obstacle_sprites
        self.import_player_asset()

    def import_player_asset(self):
        walkingUpRect = (0, SPRITE_HEIGHT * 3, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingDownRect = (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingLeftRect = (0, SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingRightRect = (0, SPRITE_HEIGHT * 2, SPRITE_WIDTH, SPRITE_HEIGHT)

        # number of images for each directional animation
        IMAGE_COUNT = 3

        # animation states in dictionary
        self.animations = {
            "up": self.playerAnimations.load_strip(walkingUpRect, IMAGE_COUNT),
            "down": self.playerAnimations.load_strip(walkingDownRect, IMAGE_COUNT),
            "left": self.playerAnimations.load_strip(walkingLeftRect, IMAGE_COUNT),
            "right": self.playerAnimations.load_strip(walkingRightRect, IMAGE_COUNT),
        }

    def input(self):
        """Input function to handle keyboard input to the player class

        This function will handle turning the player object as input is received.
        """
        keys = pygame.key.get_pressed()

        # left/right input
        if keys[pygame.K_LEFT]:
            self.compass.rotate_ip(-PLAYER_ROTATION_SPEED)
        elif keys[pygame.K_RIGHT]:
            self.compass.rotate_ip(PLAYER_ROTATION_SPEED)

    # animation loop for the player
    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = self.set_image_rotation(animation[int(self.frameIndex)])

    def collision_handler(self):
        """Collision handler for entity

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.

        Parameters
        ----------
        direction: str
            the axis to check for collisions on. It can be 'horizontal' or 'vertical'.

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
        """Changes self.direction based off of the collision_direction

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
        """Update player behavior based on player input

        Controls and movement logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        """

        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.input()
        self.set_status_by_curr_rotation()
        self.animate()
        # a new direction may be set by the collision handler
        self.collision_handler()
        self.move(self.speed)
