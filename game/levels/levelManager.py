"""This module contains the LevelManager class."""

import pygame
from levels.AssetManager import AssetManager
from levels.level import Level


class LevelManager:
    """LevelManager class.

    Created by Game. Loads levels and manages its assets.
    Default level is MainMenu.
    """

    def __init__(self, surface: pygame.Surface) -> None:
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
        # TODO: AssetManager requires path to MainMenu music. In gameData.py
        self._asset_manager: AssetManager = AssetManager("ook")
        self._screen = surface
        # TODO: boot to MainMenu instead of Level
        self._level = Level(surface)

        # pause flag used to display pause menu
        self._paused: bool = False

    def run(self) -> None:
        """Refresh the screen and run the level."""
        self._screen.fill("black")
        self._level.run()
