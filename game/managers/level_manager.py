"""This module contains the LevelManager class."""
import pygame
from levels.level import Level
from levels.test_level.test_level import TestLevel
from managers.asset_manager import AssetManager
from menus.main_menu.main_menu import MainMenu
from settings import FPS
from enums.user_selection import UserSelection


class LevelManager:
    """LevelManager class.

    Created by Game. Loads levels and menus. Default opens to MainMenu.

    Attributes
    ----------
    _surface: pygame.Surface
        The screen to display levels and menu to
    _clock: pygame.time.Clock
        Clock to track time in levels
    _asset_manager: AssetManager
        AssetManager to handle game assets such as music and all renderable sprites
    _menu: MainMenu
        MainMenu is the default menu to display from levelManager
    _level: object
        The level the user is playing. Initialized when MainMenu returns with "Level"
    _user_input: UserSelection
        Enum used to determine user input
    _quit_game: bool
        Quit flag when returning to game

    Methods
    -------
    run(self) -> bool
        Run the currently loaded menu or level and return user menu selection
    """

    def __new__(cls):
        """Create a singleton object.

        If singleton already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(LevelManager, cls).__new__(cls)
            print("A new level manager is made!")
        return cls.instance

    def __init__(self) -> None:
        """Construct the LevelManager class.

        This LevelManager will instantiate a level's contents
        onto the pygame display surface.
        """
        self._screen: pygame.Surface = pygame.display.get_surface()
        # TODO: move clock to setter/getter style
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._asset_manager: AssetManager = AssetManager()
        self._user_input: UserSelection = UserSelection.none
        # main menu is the first thing that is loaded
        self._menu: MainMenu = MainMenu()
        self._asset_manager.load_music("menu", "main_menu")
        self._level: Level = object()

        # quit flag returned to game
        self._quit_game: bool = False

    def run(self) -> bool:
        """Refresh the screen and run the level."""
        # running the menu check
        if self._menu.is_enabled():
            self._menu.run()
        self._user_input = self._menu.user_selection

        if self._user_input == UserSelection.level:
            # check is menu is finished disabling
            if not self._menu.is_enabled():
                # if the level is not loaded yet, then initialize it
                if not isinstance(self._level, Level):
                    # TODO: safely access and give asset_manager's stuff to level
                    self._level = TestLevel(
                        self._asset_manager.universal_sprites,
                        "test_level",
                    )
                    # unload music and load in new music
                    level_key: str = "test_level"
                    self._asset_manager.load_music("level", level_key)
                self._level.run()
        elif self._user_input == UserSelection.quit:
            self._quit_game is not self._quit_game

        self._clock.tick(FPS)
        return self._quit_game
