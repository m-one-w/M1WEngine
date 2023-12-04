"""AssetManager class."""


import pygame
from filemanagement.support import import_cut_graphic


class AssetManager:
    """Asset Manager class.

    One instance of AssetManager is loaded from levelManager
    to load/handle the game assets.
    """

    def __init__(self, main_menu_music: str) -> None:
        """Load sprite and music assets."""
        # csv file with sprites used in every level, like player.
        self._univeral_sprites: pygame.sprite = import_cut_graphic(
            "graphics/tilesets/tiny_atlas.png"
        )

        # TODO: music mixer initialized with MainMenu music
        self._music_manager: pygame.mixer = pygame.mixer
        self._music_manager.init()
