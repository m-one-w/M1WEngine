import pygame
from entities.player import Player
from filemanagement.support import import_cut_graphic
from tile import StaticTile
from filemanagement.support import import_csv_layout
from settings import TILESIZE, LOOP_MUSIC


class Level:
    def __init__(self, level_data, surface):
        # display surface
        self.display_surface = surface

        # setup map
        terrain_layout = import_csv_layout(level_data["ground"])
        rocks_layout = import_csv_layout(level_data["rocks"])
        raised_ground_layout = import_csv_layout(level_data["raised_ground"])
        plants_layout = import_csv_layout(level_data["plants"])
        fence_layout = import_csv_layout(level_data["fence"])
        extra_layout = import_csv_layout(level_data["extra"])
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

        # background music
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.load(
            "levels/level_data/inspiring-cinematic-ambient-116199.ogg", "ogg"
        )
        self.mixer.music.play(LOOP_MUSIC)

        # map size in number of 16 pixels = (20x, 20y size)
        self.map_size = pygame.math.Vector2(20, 20)

        sizeOfLandBlock = 16
        self.player = Player(
            (sizeOfLandBlock * 8, sizeOfLandBlock * 14),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.map_size,
        )

    def create_tile_group(self, layout):
        """Create the :func:`Sprite group<pygame.sprite.Group>` for a layout.

        Parameters
        ----------
        layout: array of values to represent a individual sprite
        type: indentifier to read in the correct graphics
        """

        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE

                    terrain_tile_list = import_cut_graphic(
                        "graphics/tilesets/original_atlas.png"
                    )
                    # val will be the terrain tile index

                    tile_surface = terrain_tile_list[int(val)]
                    sprite = StaticTile(TILESIZE, x, y, tile_surface)
                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        # update and draw the game
        self.terrain_sprites.draw(self.display_surface)
        self.plant_sprites.draw(self.display_surface)
        self.fence_sprites.draw(self.display_surface)
        self.extra_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)
        # TODO: These values will be determined by a camera manager
        shiftx = 0
        shifty = 0
        self.terrain_sprites.update(shiftx, shifty)

        self.visible_sprites.update(self.enemy_sprites, self.friendly_sprites)
        self.enemy_sprites.update(self.enemy_sprites, self.friendly_sprites)
