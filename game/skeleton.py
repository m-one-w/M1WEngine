import pygame
import random
import time
from spriteSheet import SpriteSheet
from entity import Entity

IMAGE_WIDTH = 48
IMAGE_HEIGHT = 64

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20

# modify model rect to have slightly less tall hitbox. Used for movement
SPRITE_HITBOX_OFFSET = -4
COLOR_BLACK = (0, 0, 0)


class Skeleton(Entity):
    """First enemy class. Called Skeleton

    Inherits from Entity. Move method is overwritten using logic described
    in the docs. Still uses Entity's collision_check method.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # grab self image
        skeletonMovementsPath = "graphics/skeleton/skeleton.png"
        self.skeletonAnimations = SpriteSheet(skeletonMovementsPath)
        skeletonSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.colorKeyBlack = COLOR_BLACK
        self.image = self.skeletonAnimations.image_at(
            skeletonSelfImageRect, self.colorKeyBlack
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # modify model rect to be a slightly less tall hitbox.
        # this will be used for movement.
        self.hitbox = self.rect.inflate(0, SPRITE_HITBOX_OFFSET)

        self.attacking = False
        self.attackCooldown = 100
        self.attackTime = 0
        self.speed = 0.5
        random.seed(time.time())

        self.obstacleSprites = obstacle_sprites
        self.timer = 100

        # starting position is facing and running down
        self.direction.y = 1
        self.status = "down"
        self.import_skeleton_assets()

    def import_skeleton_assets(self):
        """Import and divide the animation image into it's smaller parts.

        Called at end of :func:'init()', takes the image with all character animations
        and divides it into its sub-images. Can be expanded with more images to fulfill
        idle and attack animations.
        """

        walkingUpRect = (0, SPRITE_HEIGHT * 3, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingDownRect = (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingLeftRect = (0, SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingRightRect = (0, SPRITE_HEIGHT * 2, SPRITE_WIDTH, SPRITE_HEIGHT)

        # number of images for each directional animation
        IMAGE_COUNT = 3

        # animation states in dictionary
        self.animations = {
            "up": self.skeletonAnimations.load_strip(
                walkingUpRect, IMAGE_COUNT, self.colorKeyBlack
            ),
            "down": self.skeletonAnimations.load_strip(
                walkingDownRect, IMAGE_COUNT, self.colorKeyBlack
            ),
            "left": self.skeletonAnimations.load_strip(
                walkingLeftRect, IMAGE_COUNT, self.colorKeyBlack
            ),
            "right": self.skeletonAnimations.load_strip(
                walkingRightRect, IMAGE_COUNT, self.colorKeyBlack
            ),
        }

    def get_status(self):
        """Check current status and update status based on current

        Checks whether entity is attacking. If yes, then stop movement, change status to
        "attacking". If not attacking but status is still "attack" update status to be
        attacking.
        """

        # attack animation
        if self.attacking:
            # no moving while attacking
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                    self.status = self.status + "_attack"

        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def move(self, speed):
        """Movement logic method

        Handles movement logic. Currently random movement.
        See documentation for actual movement logic.

        Parameters
        ----------
        speed : int
            Skeleton enemy's current speed. May be modified by items or by player.
        """

        self.timer += 1
        # update direction every 100 ticks. Still moves every tick
        if self.timer >= 10:
            # update/randomize direction
            # get random number
            seed = random.randint(1, 1000)
            # if odd turn left else right
            if seed % 2:
                self.direction.x = -1
            else:
                self.direction.x = 1
            # if %3 false turn up else down
            if seed % 3:
                self.direction.y = -1
            else:
                self.direction.y = 1
            self.timer = 0

        # prevent diagonal moving from increasing speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # update
        self.hitbox.x += self.direction.x * speed
        self.collision_check("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision_check("vertical")
        self.rect.center = self.hitbox.center

    def animate(self):
        """Animation loop for the skeleton

        Loops through the 3 images to show walking animation.
        Works for each cardinal direction.
        """

        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldowns(self):
        """Prevent entity from doing anything while it is attacking

        This method prevents the entity from doing multiple actions while attacking.
        """
        currentTime = pygame.time.get_ticks()

        if self.attacking:
            if currentTime - self.attackTime >= self.attackCooldown:
                self.attacking = False

    def collision_check(self, direction):
        """Collision check for entity

        Handles collision checks for entities and other entities/the environment.
        Prevents entity from moving through obstacles.

        Parameters
        ----------
        direction: str
            the axis to check for collisions on. It can be 'horizontal' or 'vertical'.
        """

        # horizontal collision detection
        if direction == "horizontal":
            # look at all sprites
            for sprite in self.obstacleSprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        # vertical collision detection
        if direction == "vertical":
            # look at all sprites
            for sprite in self.obstacleSprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self, enemy_sprites, friendly_sprites):
        """Updates skeleton behavior based on entities on the map

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        friendly_sprites : pygame.sprite.Group()
            group of entities friendly to the player used for behavior
        """

        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.get_status()
        self.animate()
        self.move(self.speed)
