"""This module contains the LevelManager class."""
from m1wengine.managers.level_manager import LevelManager
from test_level import TestLevel


class LevelController(LevelManager):
    def __init__(self) -> None:
        super().__init__()
        starting_level = TestLevel(
            self._asset_manager._univeral_sprites,
            "test_level",
        )
        self.level = starting_level

        LevelManager.global_level_manager: LevelController = self
