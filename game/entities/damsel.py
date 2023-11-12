import pygame
import random
import time
from filemanagement.spriteSheet import SpriteSheet
from entities.entity import Entity

# consts for damsel
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20


class Damsel(Entity):
    """Damsel in distress that the player saves
    Each damsel is initialized with their starting position,
    which sprite groups it is part of, boundary sprites,
    and enemy/interactable sprites.
    ...

    Methods
    -------
    import_damsel_assets(self)
        Handles importing damsel assets.
    move(self, speed)
        Handles movement of the damsel
    set_status_by_curr_direction(self)
        Updates state based on movement logic.
    set_image_direction(self, image)
        Updates the image sprite based on the current direction.
    animate(self)
        Controls animation loop.
    collision_check(self, direction)
        Handles interaction with environment.
    update(self)
        Update damsel with current game state information.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        """Initialize a Damsel with level info

        Each damsel is initialized with their starting position,
        which sprite groups it is part of, boundary sprites,
        and enemy/interactable sprites.

        Parameters
        ----------
            pos : Tuple
                starting x, y coordinates
            groups : list of sprite groups
                which groups in level it is a part of
            obstacle_sprites : list of sprite groups
                which sprites in the level damsel cannot walk through
        """

        super().__init__(groups)

        damselMovementImagePath = "graphics/damsel/damselWalking.png"
        self.damselAnimations = SpriteSheet(damselMovementImagePath)
        damselSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.image = self.damselAnimations.image_at(damselSelfImageRect)
        self.setColorKeyWhite()
        self.rect = self.image.get_rect(topleft=pos)
        # modify model rect to be a slightly less tall hitbox.
        self.hitbox = self.rect.inflate(0, -10)
        random.seed(time.time())
        self.timer = 100
        self.obstacle_sprites = obstacle_sprites
        self.import_damsel_assets()

    def import_damsel_assets(self):
        """Initializes all animations from the image"""

        walkingUpRect = (0, SPRITE_HEIGHT * 3, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingDownRect = (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingLeftRect = (0, SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingRightRect = (0, SPRITE_HEIGHT * 2, SPRITE_WIDTH, SPRITE_HEIGHT)

        # animation states in dictionary
        self.animations = {
            "up": self.damselAnimations.load_strip(walkingUpRect, 3),
            "down": self.damselAnimations.load_strip(walkingDownRect, 3),
            "left": self.damselAnimations.load_strip(walkingLeftRect, 3),
            "right": self.damselAnimations.load_strip(walkingRightRect, 3),
        }

    def set_status_by_curr_direction(self):
        """Sets the correct status based on the current direction

        This function inspects the current direction and determines
        what the status should be.
        """

        # will only display "up" and "down". Need to rework
        if self.compass.x > 0 and self.status != "right":
            self.status = "right"
        elif self.compass.x < 0 and self.status != "left":
            self.status = "left"
        if self.compass.y > 0 and self.status != "down":
            self.status = "down"
        elif self.compass.y < 0 and self.status != "up":
            self.status = "up"

    def set_image_direction(self, image):
        """Sets a new image to the correct cardinal direction

        Return the image correlating to the correct cardinal direction.

        Parameters
        ----------
        image : png file
            image facing the current direction that will be displayed
        """

        if self.status == "right":
            self.compass.x = 1
            direction = "x"
        if self.status == "left":
            self.compass.x = -1
            direction = "x"
        if self.status == "up":
            self.compass.y = -1
            direction = "y"
        if self.status == "down":
            self.compass.y = 1
            direction = "y"

        if direction == "y":
            return pygame.transform.rotate(image, self.compass.y)
        if direction == "x":
            return pygame.transform.rotate(image, self.compass.x)

    def animate(self):
        """Method to loop through damsel animations"""

        animation = self.animations[self.status]
        # loop over fram index
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = self.set_image_direction(animation[int(self.frameIndex)])

    def collision_handler(self, direction):
        """Method to handle interaction with environment

        Parameter required for vertical and horizontal checking.

        Parameters
        ----------
        direction : string
            used to determine horizontal/vertical check.
        """

        # horizontal collision detection
        if direction == "horizontal":
            # look at all obstacle sprites
            for sprite in self.obstacle_sprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.compass.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.compass.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        # vertical collision detection
        if direction == "vertical":
            # look at all sprites
            for sprite in self.obstacle_sprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.compass.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.compass.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self, enemy_sprites, friendly_sprites):
        """Updates damsel behavior based on entities on the map

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        enemy_sprites : pygame.sprite.Group()
            group of enemy entities used to for behavior
        """

        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.set_status_by_curr_direction()
        self.animate()
        self.move(self.speed)
