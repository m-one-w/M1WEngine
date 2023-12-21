"""This module contains the LevelManager class."""
import pygame
from levels.level import Level
from levels.test_level.testLevel import TestLevel
from managers.AssetManager import AssetManager
from menus.main_menu.mainMenu import MainMenu
from settings import FPS


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
    _user_input: str
        User input used to load levels and menus
    _quit_game: bool
        Quit flag when returning to game

    Methods
    -------
    run(self) -> bool
        Run the currently loaded menu or level and return user menu selection
    """

    def __init__(self) -> None:
        """Construct the LevelManager class.

        This LevelManager will instantiate a level's contents
        onto the pygame display surface.
        """
        self._screen: pygame.Surface = pygame.display.get_surface()
        # TODO: move clock to setter/getter style
        self._clock: pygame.time.Clock = pygame.time.Clock()
        # TODO: AssetManager requires path to MainMenu music. In gameData.py
        self._asset_manager: AssetManager = AssetManager("ook")
        # main menu is the first thing that is loaded
        self._menu: MainMenu = MainMenu()
        self._level: object = object()
        self._user_input: str = "None"

        # quit flag returned to game
        self._quit_game: bool = False

    def run(self) -> bool:
        """Refresh the screen and run the level."""
        # running the menu check
        if self._menu.is_enabled():
            self._menu.run()
        self._user_input: str = self._menu.get_user_selection()

        if self._user_input == "Level":
            # check is menu is finished disabling
            if not self._menu.is_enabled():
                # if the level is not loaded yet, then initialize it
                if not isinstance(self._level, Level):
                    # TODO: safely access and give asset_manager's stuff to level
                    self._level = TestLevel(
                        self._asset_manager._univeral_sprites,
                        self._asset_manager._music_manager,
                        "test_level",
                    )
                self._level.run()
        elif self._user_input == "Quit":
            self._quit_game is not self._quit_game

        self._clock.tick(FPS)
        return self._quit_game
