"""This module contains the Level class."""
from typing import List
import pygame
from tiles.entities.player import Player
from tiles.entities.NPCs.damsel import Damsel
from tiles.entities.NPCs.skeleton import Skeleton
from tiles.tile import Tile
from filemanagement.support import import_csv_layout
from settings import TILESIZE, LOOP_MUSIC
from cameraControl.cameraManager import CameraManager
from levels.gameData import level_data
from levels.gameData import character_keys


class Level(object):
    """Level class.

    The Level class will instantiate all objects required for a single level to run.
    """

    def __init__(
        self, universal_assets: List, music_handler: pygame.mixer, level_key: str
    ):
        """Construct the level class.

        This method will instantiate all required sprite groups for the current level

        Parameters
        ----------
        surface: pygame.Surface
            The surface that contains the game's full window
        """
        # display surface
        self.display_surface = pygame.display.get_surface()

        # TODO: move any level specific setup steps into gameData.py
        self._universal_assets = universal_assets

        # extract data from level_data dictionary in gameData.py
        self.create_map(level_key)
        # sprite groups
        self.create_sprite_groups()
        # add fence_sprites to obstacle_sprites
        self.add_obstacles()

        # load and play level's music
        self._mixer = music_handler
        self._mixer.music.load(
            "levels/level_data/inspiring-cinematic-ambient-116199.ogg", "ogg"
        )
        self._mixer.music.play(LOOP_MUSIC)
        # TODO: have destructor unload/fade out music to main menu music

        self.create_entities_from_layout(self._character_layout)
        # self.player initialized in create_entities_from_layout()
        self.camera = CameraManager(self.player)
        # add sprites to camera
        self.add_sprites_to_camera()

        # pause flag used to display pause menu
        self._paused = False

    def create_map(self, level_key: str) -> None:
        """Read level data from gameData.py and stage it for rendering."""
        # setup map
        terrain_layout = import_csv_layout(level_data[level_key]["ground"])
        rocks_layout = import_csv_layout(level_data[level_key]["rocks"])
        raised_ground_layout = import_csv_layout(level_data[level_key]["raised_ground"])
        plants_layout = import_csv_layout(level_data[level_key]["plants"])
        fence_layout = import_csv_layout(level_data[level_key]["fence"])
        extra_layout = import_csv_layout(level_data[level_key]["extra"])
        self._character_layout = import_csv_layout(level_data[level_key]["characters"])

        self._terrain_sprites = self.create_tile_group(terrain_layout)
        self._terrain_sprites.add(self.create_tile_group(rocks_layout))
        self._terrain_sprites.add(self.create_tile_group(raised_ground_layout))
        self._plant_sprites = self.create_tile_group(plants_layout)
        self._fence_sprites = self.create_tile_group(fence_layout)
        self._extra_sprites = self.create_tile_group(extra_layout)

    def create_sprite_groups(self) -> None:
        """Create and initialize all sprite groups for the level."""
        self._obstacle_sprites = pygame.sprite.Group()
        self._bad_sprites = pygame.sprite.Group()
        self._good_sprites = pygame.sprite.Group()
        self._attack_sprites = pygame.sprite.Group()
        self._player_group = pygame.sprite.GroupSingle()

    def create_entities_from_layout(self, layout: List[int]):
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
                        [self._player_group],
                        self._obstacle_sprites,
                    )
                # initialize damsels
                elif val == character_keys["damsel"]:
                    Damsel(position, self._good_sprites, self._obstacle_sprites)
                # initialize skeletons
                elif val == character_keys["skeleton"]:
                    Skeleton(position, self._bad_sprites, self._obstacle_sprites)

        # add player awareness to friendly_sprites
        for entity in self._good_sprites:
            entity.set_player(self.player)

        # add player awareness to enemy_sprites
        for entity in self._bad_sprites:
            entity.set_player(self.player)

    def create_tile_group(self, layout: List[int]) -> pygame.sprite.Group:
        """Create the :func:`Sprite group<pygame.sprite.Group>` for a layout.

        Parameters
        ----------
        layout: List[int]
            List of values each representing an individual sprite
        """
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    coords = (col_index * TILESIZE, row_index * TILESIZE)

                    tile_surface = self._universal_assets[int(val)]
                    sprite = Tile(sprite_group)
                    sprite.set_tile(coords, tile_surface)
                    sprite.image.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)
                    sprite_group.add(sprite)

        return sprite_group

    def add_obstacles(self) -> None:
        """Add all obstacle sprites for the level to self._obstacle_sprites."""
        self._obstacle_sprites.add(self._fence_sprites)

    def add_sprites_to_camera(self) -> None:
        """Add all visible sprites to the CameraManager."""
        self.camera.add(self._terrain_sprites)
        self.camera.add(self._plant_sprites)
        self.camera.add(self._fence_sprites)
        self.camera.add(self._extra_sprites)

        self.camera.add(self._good_sprites)
        self.camera.add(self._bad_sprites)

    def pauseMenu(self) -> None:
        """Pauses the game and opens the pause menu."""
        print("PAUSED!")
        pass

    def run(self):
        """Draw and update all sprite groups."""
        # TODO: change run to return bool. if paused, return paused flag.
        self.display_surface.fill("black")

        # pause check
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self._paused is not self._paused

        if self._paused:
            self.pauseMenu()
        else:
            self._player_group.update(self._bad_sprites, self._good_sprites)
            self._bad_sprites.update(self._bad_sprites, self._good_sprites)
            self._good_sprites.update(self._bad_sprites, self._good_sprites)

            # draw the game behind the player character
            self.camera.camera_update()
            self.camera.draw(self.display_surface)
            # draw the player chacter
            self._player_group.draw(self.display_surface)
