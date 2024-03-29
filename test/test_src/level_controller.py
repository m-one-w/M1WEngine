"""This module contains the LevelManager class."""
from m1wengine.managers.level_manager import LevelManager
from test_level import TestLevel
import game_data


class LevelController(LevelManager):
    """Level Controller class."""

    def __init__(self) -> None:
        """Initialize the level controller."""
        super().__init__(game_data)
        starting_level = TestLevel(
            self._asset_manager._univeral_sprites,
            "test_level",
        )
        self.level = starting_level

        LevelManager.global_level_manager: LevelController = self
