import pygame
from entities.player import Player
from filemanagement.support import import_cut_graphic
from entities.damsel import Damsel
from entities.skeleton import Skeleton
from tile import StaticTile
from filemanagement.support import import_csv_layout
from settings import TILESIZE, LOOP_MUSIC
from cameraControl.cameraManager import CameraManager
from levels.gameData import level_1 as level_data
from levels.gameData import character_keys


class Level:

    """Level class

    The Level class will instantiate all objects required for a single level to run.

    """

    def __init__(self, surface):
        """Constructor

        This method will instantiate all required sprite groups for the current level

        Parameters
        ----------
        level_data: the game asset information for the current level
        surface: the surface to contain the game screen's full window
        """

        # display surface
        self.display_surface = surface

        # TODO: move any level specific setup steps into a method

        # setup map
        terrain_layout = import_csv_layout(level_data["ground"])
        rocks_layout = import_csv_layout(level_data["rocks"])
        raised_ground_layout = import_csv_layout(level_data["raised_ground"])
        plants_layout = import_csv_layout(level_data["plants"])
        fence_layout = import_csv_layout(level_data["fence"])
        extra_layout = import_csv_layout(level_data["extra"])
        character_layout = import_csv_layout(level_data["characters"])
        self.terrain_sprites = self.create_tile_group(terrain_layout)
        self.terrain_sprites.add(self.create_tile_group(rocks_layout))
        self.terrain_sprites.add(self.create_tile_group(raised_ground_layout))
        self.plant_sprites = self.create_tile_group(plants_layout)
        self.fence_sprites = self.create_tile_group(fence_layout)
        self.extra_sprites = self.create_tile_group(extra_layout)

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.friendly_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # add fence_sprites to obstacle_sprites
        self.obstacle_sprites.add(self.fence_sprites)

        # background music
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.load(
            "levels/level_data/inspiring-cinematic-ambient-116199.ogg", "ogg"
        )
        self.mixer.music.play(LOOP_MUSIC)

        # map size in number of 16 pixels = (20x, 20y size)
        self.map_size = pygame.math.Vector2(80, 80)

        self.create_entities_from_layout(character_layout)
        self.visible_sprites.add(self.friendly_sprites)
        self.visible_sprites.add(self.enemy_sprites)

        self.camera = CameraManager(self.player)
        self.camera.add(self.terrain_sprites)
        self.camera.add(self.plant_sprites)
        self.camera.add(self.fence_sprites)
        self.camera.add(self.extra_sprites)

    def create_entities_from_layout(self, layout):
        """Initialize the entities on a layout.

        Parameters
        ----------
        layout: array of values each representing an individual entity
        """

        # default location of top left corner should never be used
        x = 0
        y = 0
        position = (x, y)
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # all logic for every entity
                if val != -1:
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    position = (x, y)
                # initialize the player
                if val == character_keys["player"]:
                    self.player = Player(
                        position,
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        self.map_size,
                    )
                # initialize damsels
                elif val == character_keys["damsel"]:
                    Damsel(position, self.friendly_sprites, self.obstacle_sprites)
                # initialize skeletons
                elif val == character_keys["skeleton"]:
                    Skeleton(position, self.enemy_sprites, self.obstacle_sprites)

    def create_tile_group(self, layout):
        """Create the :func:`Sprite group<pygame.sprite.Group>` for a layout.

        Parameters
        ----------
        layout: array of values each representing an individual sprite
        type: indentifier to read in the correct graphics

        """

        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    terrain_tile_list = import_cut_graphic(
                        "graphics/tilesets/tiny_atlas.png"
                    )
                    # val will be the terrain tile index

                    tile_surface = terrain_tile_list[int(val)]
                    sprite = StaticTile(sprite_group, x, y, tile_surface)
                    sprite.setColorKeyBlack()
                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        """Draw and update all sprite groups"""

        self.visible_sprites.update(self.enemy_sprites, self.friendly_sprites)
        self.enemy_sprites.update(self.enemy_sprites, self.friendly_sprites)

        # draw the game behind the player character
        self.camera.camera_update()
        self.camera.draw(self.display_surface)
        # draw the player chacter
        self.visible_sprites.draw(self.display_surface)
