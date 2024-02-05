"""This module contains the LevelManager class."""
import pygame
from m1wengine.enums.user_selection import UserSelection
from m1wengine.managers.asset_manager import AssetManager
from m1wengine.menus.main_menu.main_menu import MainMenu
from m1wengine.settings import FPS


class LevelManager:
    """LevelManager class.

    Created by Game. Loads levels and menus. Default opens to MainMenu.

    Attributes
    ----------
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
    __new__(cls) -> object()
        Check if singleton LevelManager already exists, return the instance
    run(self) -> bool
        Run the currently loaded menu or level and return user input selection
    """

    def __new__(cls) -> object():
        """Create a singleton object.

        If singleton already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(LevelManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """Construct the LevelManager class.

        This LevelManager will instantiate a level's contents
        onto the pygame display surface.
        """
        # TODO: move clock to setter/getter style
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._asset_manager: AssetManager = AssetManager()
        self._user_input: UserSelection = UserSelection.none
        # main menu is the first thing that is loaded
        self._menu: MainMenu = MainMenu()
        self._asset_manager.load_music("menu", "main_menu")
        self._level: object = object()

        self._user_input: str = "None"
        # quit flag returned to game
        self._quit_game: bool = False

    @property
    def level(self) -> str:
        """Get the current level hint text."""
        return self._level

    @level.setter
    def level(self, new_value: str):
        """Set the current level hint text.

        Parameters
        ----------
        new_value: str
            New level hint to set
        """
        self._level = new_value

    # TODO: add method to change the music

    def run(self) -> bool:
        """Refresh the screen and run the level.

        Returns
        -------
        _quit_game: bool
            Returns true if user wants to quit the game
        """
        # running the menu check
        if self._menu.is_enabled():
            self._menu.run()
        self._user_input = self._menu.user_selection

        if self._user_input == UserSelection.level:
            # check is menu is finished disabling
            if not self._menu.is_enabled():
                self._level.run()
        elif self._user_input == UserSelection.quit:
            self._quit_game is not self._quit_game

        self._clock.tick(FPS)
        return self._quit_game
