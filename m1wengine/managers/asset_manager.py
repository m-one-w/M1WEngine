"""AssetManager class."""
import pygame
from m1wengine.file_managers.support import import_cut_graphic


class AssetManager:
    """Asset Manager class.

    One instance of AssetManager is loaded from levelManager
    to load/handle the game assets.

    Attributes
    ----------
    _universal_sprites: list[pygame.sprite]
        The list of pygame.sprites that will be used by levels
    _music_manager: pygame.mixer
        The mixer that loads and plays music

    Methods
    -------
    universal_sprites(self) -> list[pygame.sprite]
        Get the universal sprites
    load_music(self, menu_flag: str, key: str)
        Unload previous music and loads new music
    """

    def __init__(self, game_data) -> None:
        """Load sprite and music assets."""
        # csv file with sprites used in every level, like player.
        self._univeral_sprites: list[pygame.Surface] = import_cut_graphic(
            game_data.tileset_path
        )

        self._music_manager: pygame.mixer = pygame.mixer
        self._music_manager.init()
        self._game_data = game_data

    @property
    def universal_sprites(self) -> list:
        """Get the universal sprites."""
        return self._univeral_sprites

    def load_music(self, menu_flag: str, key: str) -> None:
        """Unload previous music and loads menu music."""
        self._music_manager.music.unload()
        if menu_flag == "menu":
            self._music_manager.music.load(
                self._game_data.menu_data.get(key).get("music")
            )
        else:
            self._music_manager.music.load(
                self._game_data.level_data.get(key).get("music")
            )
        self._music_manager.music.play()
