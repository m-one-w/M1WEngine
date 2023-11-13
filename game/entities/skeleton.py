"""This module contains the Skeleton class."""
from enum import Enum
import math
import sys
import pygame
from filemanagement.spriteSheet import SpriteSheet
from entities.entity import Entity
from settings import TILESIZE

IMAGE_WIDTH = 48
IMAGE_HEIGHT = 64

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 20

# modify model rect to have slightly less tall hitbox. Used for movement
SPRITE_HITBOX_OFFSET = -4


class Skeleton(Entity):
    """First enemy class. Called Skeleton.

    Inherits from Entity. Move method is overwritten using logic described
    in the docs. Still uses Entity's collision_check method.
    """

    def __init__(self, pos, groups, obstacle_sprites):
        """Construct the skeleton class."""
        super().__init__(groups)

        # init empty player
        self.player = pygame.sprite.Sprite()

        # grab self image
        skeletonMovementsPath = "graphics/skeleton/skeleton.png"
        self.skeletonAnimations = SpriteSheet(skeletonMovementsPath)
        skeletonSelfImageRect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        self.image = self.skeletonAnimations.image_at(
            skeletonSelfImageRect
        ).convert_alpha()
        self.setColorKeyBlack()
        self.rect = self.image.get_rect(topleft=pos)

        # modify model rect to be a slightly less tall hitbox.
        # this will be used for movement.
        self.hitbox = self.rect.inflate(0, SPRITE_HITBOX_OFFSET)
        # TODO: find sweet spot inflation size for radar detection
        inflation_size = 20
        self.radar = self.rect.inflate(
            TILESIZE * inflation_size, TILESIZE * inflation_size
        )

        self.obstacleSprites = obstacle_sprites
        self.import_skeleton_assets()

        # the skeleton is attacking
        self.sprite_to_attack = pygame.sprite.Sprite()

        # setting up state machine
        self.states = Enum("skeleton_state", ["Patrol", "Attack", "Flee"])
        self.current_state = self.states.Patrol

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
            "up": self.skeletonAnimations.load_strip(walkingUpRect, IMAGE_COUNT),
            "down": self.skeletonAnimations.load_strip(walkingDownRect, IMAGE_COUNT),
            "left": self.skeletonAnimations.load_strip(walkingLeftRect, IMAGE_COUNT),
            "right": self.skeletonAnimations.load_strip(walkingRightRect, IMAGE_COUNT),
        }

    def automate_movement(self):
        """Movement logic method.

        Handles movement logic. Currently random movement.
        See documentation for actual movement logic.
        """
        # update radar with new pos
        self.radar.center = self.rect.center

        # change state if player is nearby
        self.radar_detect_player_entity()
        # change state if there is good_entity nearby
        self.radar_detect_good_entities()

        self.move_based_on_state()

    def radar_detect_player_entity(self):
        """Check whether player is within our radar."""
        # set state to 'Flee' if player detected
        collision = self.radar.colliderect(self.player)
        # if player on radar, set state
        if collision:
            if self.current_state != self.states.Flee:
                self.set_state_flee()
        else:
            if (
                self.current_state != self.states.Attack
                and self.current_state != self.states.Patrol
            ):
                self.set_state_patrol()

    def radar_detect_good_entities(self):
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
                    self.set_state_attack()

        else:
            # else we are not attacking
            if self.current_state == self.states.Attack:
                self.set_state_patrol()

    def patrol_movement(self):
        """Move in random direction."""
        # TODO: finish movement logic
        if self.current_state == self.states.Patrol:
            # down direction
            self.compass.x = 0
            self.compass.y = -1

            self.move(self.speed)

    def flee_movement(self):
        """Change direction based on where player is."""
        if self.current_state == self.states.Flee:
            self.compass = self.player.compass
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

            self.compass.x = self.sprite_to_attack.compass.x

    def move_based_on_state(self):
        """Logic to determine which _movement() method to call."""
        if self.current_state == self.states.Attack:
            self.attack_movement()

        elif self.current_state == self.states.Flee:
            self.flee_movement()

        elif self.current_state == self.states.Patrol:
            self.patrol_movement()

    def set_state_patrol(self):
        """Set state machine to 'Patrol'."""
        self.current_state = self.states.Patrol

    def set_state_attack(self):
        """Set state machine to 'Attack'."""
        self.current_state = self.states.Attack

    def set_state_flee(self):
        """Set stae machine to 'Flee'."""
        self.current_state = self.states.Flee

    def move_towards_entity(self, coordinates: pygame.math.Vector2):
        """Change self.compass to move towards an entity's coordinates.

        Parameters
        ----------
        coordinates : pygame.math.Vector2
            coordinates that skeleton will face and walk towards
        """
        # TODO: finish movement logic
        # choose angle for compass. Where is player/damsel located
        # x-axis logic. < means left of skeleton, > means right of skeleton
        if coordinates.x < self.rect.centerx:
            print("entity is left of skeleton")
        elif coordinates.x > self.rect.centerx:
            print("entity is right of skeleton")

        # y-axis logic. > means entity is below skeleton
        if coordinates.y < self.rect.centery:
            print("entity is above skeleton")
        elif coordinates.y > self.rect.centery:
            print("entity is below skeleton")

    def animate(self):
        """Animation loop for the skeleton.

        Loops through the 3 images to show walking animation.
        Works for each cardinal direction.
        """
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]

    def get_distance(self, coords: tuple) -> float:
        """Return the hypotenuse/distance away from another entity.

        Parameters
        ----------
        coords: tuple
            coordinates of the entity we are testing
        """
        x = 0
        y = 1
        return math.hypot(coords[x] - self.rect[x], coords[y] - self.rect[y])

    def collision_handler(self):
        """Handle collision interactions with environment."""
        return

    def update(self, enemy_sprites, friendly_sprites):
        """Update skeleton behavior based on entities on the map.

        Reaction logic is described in the [documentation](https://github.com/Sean-Nishi/Lunk-Game/blob/main/docs/specSheet.md#player-movement).# noqa: E501

        Parameters
        ----------
        friendly_sprites : pygame.sprite.Group()
            group of entities friendly to the player used for behavior
        """
        self.enemy_sprites = enemy_sprites
        self.friendly_sprites = friendly_sprites
        self.animate()
        # will move half as fast as player at the same speed
        self.move(self.speed)
