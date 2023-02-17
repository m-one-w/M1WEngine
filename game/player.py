import pygame
from spriteSheet import SpriteSheet
from settings import TILESIZE

# Defines how fast the player object can rotate while running
PLAYER_ROTATION_SPEED = 5

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20


class Player(pygame.sprite.Sprite):
    """Player class which contains the object players will directly control

    The player class will handle movement logic and sprite changing logic for the player
    object. The player class will also handle any collision logic that influences the
    player object.
    """

    def __init__(self, pos, groups, obstacle_sprites, map_size):
        super().__init__(groups)

        # grab self image
        playerMovementsPath = "graphics/player/playerWalking.png"
        self.playerAnimations = SpriteSheet(playerMovementsPath)
        playerSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.colorKeyBlack = (0, 0, 0)
        self.image = self.playerAnimations.image_at(
            playerSelfImageRect, self.colorKeyBlack
        )
        self.rect = self.image.get_rect(topleft=pos)
        # modify model rect to be a slightly less tall hitbox.
        # this will be used for movement.
        self.hitbox = self.rect.inflate(0, -26)
        self.map_size = pygame.math.Vector2(map_size)
        # graphics setup
        # self.import_player_asset()#TODO
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        self.obstacle_sprites = obstacle_sprites

        # starting position is running north
        self.direction.y = -1
        self.status = "up"
        self.import_player_asset()

    def import_player_asset(self):
        walkingUpRect = (0, SPRITE_HEIGHT * 3, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingDownRect = (0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingLeftRect = (0, SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        walkingRightRect = (0, SPRITE_HEIGHT * 2, SPRITE_WIDTH, SPRITE_HEIGHT)

        # animation states in dictionary
        self.animations = {
            "up": self.playerAnimations.load_strip(
                walkingUpRect, 3, self.colorKeyBlack
            ),
            "down": self.playerAnimations.load_strip(
                walkingDownRect, 3, self.colorKeyBlack
            ),
            "left": self.playerAnimations.load_strip(
                walkingLeftRect, 3, self.colorKeyBlack
            ),
            "right": self.playerAnimations.load_strip(
                walkingRightRect, 3, self.colorKeyBlack
            ),
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],
        }

    def input(self):
        """Input function to handle keyboard input to the player class

        This function will handle turning the player object as input is recieved.
        """
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # left/right input
            if keys[pygame.K_LEFT]:
                self.direction.rotate_ip(-PLAYER_ROTATION_SPEED)
                # TODO: Check current rotation for status change
            elif keys[pygame.K_RIGHT]:
                self.direction.rotate_ip(PLAYER_ROTATION_SPEED)
                # TODO: Check current rotation for status change

    def get_status(self):
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

    # animation loop for the player
    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def move(self, speed):
        # prevent diagonal moving from increasing speed
        # check if vector has magnitude
        if self.direction.magnitude() != 0:
            # normalize
            self.direction = self.direction.normalize()
        # update
        self.hitbox.x += self.direction.x * speed
        self.collision_check("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision_check("vertical")
        self.rect.center = self.hitbox.center

        # if we go beyond the map size, wrap around to the other side.
        # Need to test hitbox collisions if wrap around into a wall or enemy..
        # may need to be before the collision checks..
        if self.hitbox.x >= self.map_size.x * TILESIZE:
            self.hitbox.x = TILESIZE
        if self.hitbox.y >= self.map_size.y * TILESIZE:
            self.hitbox.y = TILESIZE

    def collision_check(self, direction):
        # horizontal collision detection
        if direction == "horizontal":
            # look at all sprites
            for sprite in self.obstacle_sprites:
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
            for sprite in self.obstacle_sprites:
                # check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    # check direction of collision
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
