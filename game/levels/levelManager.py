"""This module contains the LevelManager class."""

import pygame
from levels.level import Level
from levels.mainMenu import MainMenu
from settings import FPS
from levels.AssetManager import AssetManager


class LevelManager:
    """LevelManager class.

    Created by Game. Loads levels and manages its assets.
    Default level is MainMenu.
    """

    def __init__(self) -> None:
        """Construct the LevelManager class.

        This LevelManager will instantiate a level's contents
        onto the pygame display surface.

        Parameters
        ----------
        surface: pygame.Surface
            The surface to draw a level's assets
        gameData: str
            Path to gameData.py. Parse file for specific level info. MainManu is default
        """
        self._screen = pygame.display.get_surface()
        # TODO: move clock to setter/getter style
        self.clock = pygame.time.Clock()
        # TODO: AssetManager requires path to MainMenu music. In gameData.py
        self._asset_manager: AssetManager = AssetManager("ook")
        # main menu is the first thing that is loaded
        self._menu: MainMenu = MainMenu()
        self._level = object()
        self._user_input = "None"

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
                    self._level = Level(
                        self._asset_manager._univeral_sprites,
                        self._asset_manager._music_manager,
                        "level_1",
                    )
                # run the level
                self._level.run()
        elif self._user_input == "Quit":
            self._quit_game is not self._quit_game

        self.clock.tick(FPS)
        return self._quit_game
