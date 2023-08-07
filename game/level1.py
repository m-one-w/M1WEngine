import pygame
from settings import TILESIZE, LOOP_MUSIC
from wall import Wall
from berryBush import BerryBush
from player import Player
from skeleton import Skeleton
from damsel import Damsel


class Level:
    def __init__(self):
        # display surface
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.friendly_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # background music
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.load(
            "levels/level_data/inspiring-cinematic-ambient-116199.ogg", "ogg"
        )
        self.mixer.music.play(LOOP_MUSIC)

        # default world map
        # KEY: x = wall, p = player
        self.world_map = [
            [
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                "p",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                "t",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "e",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "d",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "e",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "t",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                "x",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
                "x",
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                ",",
                "x",
            ],
            [
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
                "x",
            ],
        ]
        # map size in number of 64 pixels = (20x, 20y size)
        self.map_size = pygame.math.Vector2(20, 20)

        # sprite setup
        self.create_map()

    def create_map(self):
        """Creates a map based on a level matrix

        This method turns the level matrix into a map of objects to be used
        by other classes.
        """
        for row_index, row in enumerate(self.world_map):  # in enumerate(WORLD_MAP)
            for col_index, col in enumerate(row):  # in enumerate(row)
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == "x":
                    Wall((x, y), [self.visible_sprites, self.obstacle_sprites])

                if col == "t":
                    # berry bush image is 20x20 pixels
                    BerryBush((x, y), [self.visible_sprites, self.obstacle_sprites])

                if col == "e":
                    # skeleton image is 16x20 pixels
                    Skeleton(
                        (x, y),
                        [self.visible_sprites, self.enemy_sprites],
                        self.obstacle_sprites,
                    )

                if col == "d":
                    # damsel image is 16x20 pixels
                    Damsel(
                        (x, y),
                        [self.visible_sprites, self.friendly_sprites],
                        self.obstacle_sprites,
                    )
        sizeOfLandBlock = 64

        # pass in map size so player can do wrap around if needed
        self.player = Player(
            (sizeOfLandBlock * 8, sizeOfLandBlock * 14),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.map_size,
        )

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(self.enemy_sprites, self.friendly_sprites)
        self.enemy_sprites.update(self.enemy_sprites, self.friendly_sprites)
        # debug(self.player.direction)


# Class to handle camera movement centered around player
# Called YSort because of sprite overlap
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = (
            self.display_surface.get_size()[0] // 2
        )  # floor div, returns int
        self.half_height = (
            self.display_surface.get_size()[1] // 2
        )  # floor div, returns int
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surface = pygame.image.load(
            "graphics/floor_surface/ground.png"
        ).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    # Drawing the map with the offset of the player, keeps screen centered on player
    def custom_draw(self, player):
        # calculate offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # draw floor and give camera offset
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)

        # draw the sprites, sort by center y-coord for overlap
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset)
