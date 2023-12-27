"""AssetManager class."""
import pygame
from file_managers.support import import_cut_graphic
from game_data import level_data, menu_data


class AssetManager:
    """Asset Manager class.

    One instance of AssetManager is loaded from levelManager
    to load/handle the game assets.

    Attributes
    ----------
    _universal_sprites: pygame.sprite
        The list of pygame.sprites that will be used by levels
    _music_manager: pygame.mixer
        The mixer that loads and plays music

    Methods
    -------
    load_music(self, menu_flag: str, key: str)
        Unload previous music and loads new music
    """

    def __init__(self) -> None:
        """Load sprite and music assets."""
        # csv file with sprites used in every level, like player.
        self._univeral_sprites: pygame.sprite = import_cut_graphic(
            "game_assets/graphics/tilesets/tiny_atlas.png"
        )

        self._music_manager: pygame.mixer = pygame.mixer
        self._music_manager.init()

    def load_music(self, menu_flag: str, key: str) -> None:
        """Unload previous music and loads menu music."""
        self._music_manager.music.unload()
        if menu_flag == "menu":
            self._music_manager.music.load(menu_data.get(key).get("music"))
        else:
            self._music_manager.music.load(level_data.get(key).get("music"))
        self._music_manager.music.play()
