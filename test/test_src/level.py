"""This module contains the Level class."""
from typing import List
import pygame
from m1wengine.managers.camera_manager import CameraManager
from m1wengine.tiles.tile import Tile
from m1wengine.file_managers.support import import_csv_layout
from m1wengine.settings import TILESIZE
from m1wengine.game_data import character_keys, item_keys, level_data
from m1wengine.tiles.entities.characters.player import Player
from m1wengine.abstract_HUD import AbstractHud
from bad_NPCs.minotaur import Minotaur
from bad_NPCs.skeleton import Skeleton
from good_NPCs.damsel import Damsel
from items.crystal import Crystal
from neutral_NPCs.postman import Postman


class Level(object):
    """Level class.

    The Level class will instantiate all objects required for a single level to run.

    Attributes
    ----------
    _display_surface: pygame.Surface
        The surface which to display the level
    _camera: CameraManager
        CameraManager handles sprite movement across the screen relative to the player
    _terrain_sprites: pygame.sprite.Group
        The sprite group containing all terrain sprites
    _plant_sprites: pygame. sprite.Group
        The sprite group containing all plant sprites
    _fence_sprites: pygame.sprite.Group
        The sprite group containing all the fence sprites
    _extra_sprites
        The sprite group containing all the extra sprites
    _obstacle_sprites: pygame.sprite.Group
        The sprites group containing all sprites that Characters cannot move through
    _bad_sprites: pygame.sprite.Group
        The sprite group for all bad aligned sprites
    _good_sprites: pygame.sprite.Group
        The sprite group for all good aligned sprites
    _neutral_sprites: pygame.sprite.Group
        The sprite group for all neutral aligned sprites
    _attack_sprites: pygame.sprite.Group
        The sprites group used for projectiles made from attacks
    _player_group: pygame.sprite.GroupSingle
        The single sprite group containing the player
    _item_sprites: pygame.sprite.Group
        The sprite group used for items

    Methods
    -------
    create_map(self, level_dict: dict)
        Parses gameData.py's level_data using level_key to get this level's sprites
    create_sprite_groups(self)
        Create all sprites groups used in the level
    create_entities_from_layout(self, layout: List[int])
        Parse the level map's layout for entities and initialize them
    create_tile_group(self, layout: List[int]) -> pygame.sprite.Group
        Create tiles for the map using the layout and universal assets
    create_items_from_layout(self)
        Create all items
    add_obstacles(self)
        Add level specific obstacles to _obstacle_sprites
    add_sprites_to_camera(self)
        Add all visible sprites to the CameraManager
    run(self)
        Draw and update all sprite groups
    """

    def __init__(self, universal_assets: list[pygame.Surface], level_str: str):
        """Construct the level class.

        This method will instantiate all required sprite groups for the current level

        Parameters
        ----------
        universal_assets: list[pygame.Surface]
            The list containing all game assets which the level will select from
        level_str: str
            The key to the specific level data when parsing gameData.py
        """
        self._display_surface: pygame.Surface = pygame.display.get_surface()
        # extract data from level_data dictionary in gameData.py
        self.create_map(level_str, universal_assets)
        self.create_sprite_groups()
        self.add_obstacles()
        self.create_characters_from_layout(self._character_layout)
        self.create_items_from_layout()

        self._camera: CameraManager = CameraManager(self._player_group.sprite)
        self.add_sprites_to_camera()

        self._hud = AbstractHud.global_hud

    def create_map(
        self, level_key: str, universal_assets: list[pygame.Surface]
    ) -> None:
        """Read level data from gameData.py and stage it for rendering."""
        # setup map
        terrain_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("ground")
        )
        rocks_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("rocks")
        )
        raised_ground_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("raised_ground")
        )
        plants_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("plants")
        )
        fence_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("fence")
        )
        extra_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("extra")
        )
        self._character_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("characters")
        )
        self._items_layout: list[int] = import_csv_layout(
            level_data.get(level_key).get("items")
        )

        self._terrain_sprites: pygame.sprite.Group = self.create_tile_group(
            terrain_layout, universal_assets
        )
        self._terrain_sprites.add(
            self.create_tile_group(rocks_layout, universal_assets)
        )
        self._terrain_sprites.add(
            self.create_tile_group(raised_ground_layout, universal_assets)
        )
        self._plant_sprites: pygame.sprite.Group = self.create_tile_group(
            plants_layout, universal_assets
        )
        self._fence_sprites: pygame.sprite.Group = self.create_tile_group(
            fence_layout, universal_assets
        )
        self._extra_sprites: pygame.sprite.Group = self.create_tile_group(
            extra_layout, universal_assets
        )

    def create_sprite_groups(self) -> None:
        """Create all sprite groups for the level."""
        self._obstacle_sprites = pygame.sprite.Group()
        self._bad_sprites = pygame.sprite.Group()
        self._good_sprites = pygame.sprite.Group()
        self._neutral_sprites = pygame.sprite.Group()
        self._attack_sprites = pygame.sprite.Group()
        self._player_group = pygame.sprite.GroupSingle()
        self._item_sprites = pygame.sprite.Group()

    def create_characters_from_layout(self, layout: list[int]) -> None:
        """Initialize the entities on a layout.

        Parameters
        ----------
        layout: array of values each representing an individual entity
        """
        # default location of top left corner should never be used
        x: int = 0
        y: int = 0
        position: pygame.math.Vector2 = (x, y)
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # all logic for every entity
                if val != -1:
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    position = (x, y)
                # initialize the player
                if val == character_keys["player"]:
                    player: Player = Player(
                        position,
                        [self._player_group],
                        self._obstacle_sprites,
                    )
                    self._player_group.add(player)
                # initialize damsels
                elif val == character_keys["damsel"]:
                    Damsel(position, self._good_sprites, self._obstacle_sprites)
                # initialize skeletons
                elif val == character_keys["skeleton"]:
                    Skeleton(position, self._bad_sprites, self._obstacle_sprites)
                elif val == character_keys["minotaur"]:
                    Minotaur(position, self._bad_sprites, self._obstacle_sprites)
                elif val == character_keys["postman"]:
                    Postman(position, self._neutral_sprites, self._obstacle_sprites)

        # add player awareness to friendly_sprites
        for entity in self._good_sprites:
            entity.set_player(self._player_group.sprite)

        # add player awareness to enemy_sprites
        for entity in self._bad_sprites:
            entity.set_player(self._player_group.sprite)

        # add player awareness to neutral_sprites
        for entity in self._neutral_sprites:
            entity.set_player(self._player_group.sprite)

    def create_items_from_layout(self) -> None:
        """Initialize the entities on a layout."""
        # default location of top left corner should never be used
        x: int = 0
        y: int = 0
        position: tuple = (x, y)
        for row_index, row in enumerate(self._items_layout):
            for col_index, val in enumerate(row):
                # all logic for every entity
                if val != -1:
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    position = (x, y)
                # initialize the player
                if val == item_keys["crystal"]:
                    Crystal(self._item_sprites, position)

    def create_tile_group(
        self, layout: list[int], universal_assets: list[pygame.Surface]
    ) -> pygame.sprite.Group:
        """Create the :func:`Sprite group<pygame.sprite.Group>` for a layout.

        Parameters
        ----------
        layout: list[int]
            The list of values each representing an individual sprite
        universal_assets: list[pygame.Surface]
            The list of all pygame surfaces to be used
        """
        sprite_group: pygame.sprite.Group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    coords: tuple[int, int] = (
                        col_index * TILESIZE,
                        row_index * TILESIZE,
                    )
                    tile_surface: pygame.Surface = universal_assets[int(val)]
                    sprite: Tile = Tile(sprite_group)
                    sprite.set_tile(coords, tile_surface)
                    sprite.image.set_colorkey(pygame.Color("black"), pygame.RLEACCEL)
                    sprite_group.add(sprite)

        return sprite_group

    def add_obstacles(self) -> None:
        """Add all obstacle sprites for the level to self._obstacle_sprites."""
        self._obstacle_sprites.add(self._fence_sprites)

    def add_sprites_to_camera(self) -> None:
        """Add all visible sprites to the CameraManager."""
        self._camera.add(self._terrain_sprites)
        self._camera.add(self._plant_sprites)
        self._camera.add(self._fence_sprites)
        self._camera.add(self._extra_sprites)
        self._camera.add(self._item_sprites)

        self._camera.add(self._bad_sprites)
        self._camera.add(self._good_sprites)
        self._camera.add(self._neutral_sprites)

    def run(self) -> None:
        """Draw and update all sprite groups."""
        self._display_surface.fill("black")

        # pause check
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    print("found in level")

        if not self._hud.pause_level:
            self._player_group.update(self._bad_sprites, self._good_sprites)
            self._bad_sprites.update(self._bad_sprites, self._good_sprites)
            self._good_sprites.update(self._bad_sprites, self._good_sprites)
            self._neutral_sprites.update(self._bad_sprites, self._good_sprites)
            self._item_sprites.update()

            # draw the game behind the player character
            self._camera.camera_update()

        self._camera.draw(self._display_surface)
        # draw the player chacter
        self._player_group.draw(self._display_surface)
        self._hud.draw(self._display_surface)
        self._hud.update()
