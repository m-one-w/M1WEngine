"""TestLevel class for development."""
from typing import List
import pygame
from levels.level import Level


class TestLevel(Level):
    """TestLevel class.

    TestLevel class will instantiate all objects to be tested.
    """

    def __init__(
        self, universal_assets: List, music_handler: pygame.mixer, level_key: str
    ):
        """Initialize base Level class then add in assets to test.

        Parameters
        ----------
        universal_assets: List[pygame.sprite]
            The list containing all game assets which the level will select from
        music_handler: pygame.mixer
            LevelManager's music mixer to play this level's music
        level_key: str
            The key to the specific level data when parsing gameData.py
        """
        super().__init__(universal_assets, music_handler, level_key)
