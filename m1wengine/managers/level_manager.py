"""This module contains the LevelManager class."""
import pygame
from m1wengine.abstract_HUD import AbstractHud
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
    __new__(cls) -> object
        Check if singleton LevelManager already exists, return the instance
    load_level(self) -> None
        Create the current level
    reload_level(self) -> None
        Load a new instance of the current level
    return_to_main_menu(self) -> None
        Unload the current level and enable the main menu
    run(self) -> bool
        Run the currently loaded menu or level and return user input selection
    """

    def __new__(cls) -> object:
        """Create a singleton object.

        If singleton already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(LevelManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, game_data, settings) -> None:
        """Construct the LevelManager class.

        This LevelManager will instantiate a level's contents
        onto the pygame display surface.

        Parameters
        ----------
        game_data: any
            Client side definition of the game data
        settings: any
            Client side definition of the game settings
        """
        # TODO: move clock to setter/getter style
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._asset_manager: AssetManager = AssetManager(game_data)
        self._user_input: UserSelection = UserSelection.none
        # main menu is the first thing that is loaded
        self._menu: MainMenu = MainMenu(settings)
        self._asset_manager.load_music("menu", "main_menu")
        self._level: object = object()

        self._user_input: str = "None"
        # quit flag returned to game
        self._quit_game: bool = False

        self._level_type = type(self._level)

        self._hud: AbstractHud = AbstractHud.global_hud

    @property
    def level(self) -> str:
        """Get the current level hint text."""
        # TODO: redo property tag or docstring comments
        return self._level

    @level.setter
    def level(self, new_value: str):
        """Set the current level hint text.

        Parameters
        ----------
        new_value: str
            New level hint to set
        """
        # TODO: redo property tag or docstring comments
        self._level = new_value

    @property
    def level_type(self) -> object:
        """Get the current level type.

        Returns
        -------
        _level_type: object
            Returns the level_type as an object. Should be level
        """
        # TODO: when refactor level into the engine, make return Level type
        return self._level_type

    @level_type.setter
    def level_type(self, new_value: object):
        """Set the current level type, assuming valid typing."""
        # TODO: set to Level type instead of object type
        if isinstance(new_value, object):
            self._level_type = new_value

    # TODO: add method to change the music

    def load_level(self) -> None:
        """When user selects to reload the level, start from the beginning again."""
        # TODO: make this not hard_coded to defeat_enemies
        if self._level_type == object():
            raise ValueError("Level is of object type. Should be of level type.")
        else:
            self.level = self._level_type(
                self._asset_manager._univeral_sprites, "defeat_enemies"
            )

    def reload_level(self) -> None:
        """Reload the current level."""
        # TODO: make this not hard_coded to defeat_enemies
        self._level = self._level_type(
            self._asset_manager._univeral_sprites, "defeat_enemies"
        )

    def return_to_main_menu(self) -> None:
        """Exit the current level and return to main_menu."""
        self._level = object()
        self._menu.enable()

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
        else:
            # run the level, and only update the clock when game runs
            # if level isn't loaded yet, load it
            if not isinstance(self._level, self._level_type):
                self.load_level()
            self._level.run()
            self._user_input = self._level._game_over_menu._user_selection
            self._clock.tick(FPS)

        # user selection check
        if self._user_input == UserSelection.none:
            pass
        elif self._user_input == UserSelection.restart:
            # restart the level by reloading it
            self.reload_level()
        elif self._user_input == UserSelection.main_menu:
            # enable menu and unload the current level
            self.return_to_main_menu()
        elif self._user_input == UserSelection.quit:
            self._quit_game is not self._quit_game

        return self._quit_game


global_level_manager: LevelManager = object()
