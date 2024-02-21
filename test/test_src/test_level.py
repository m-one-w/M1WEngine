"""TestLevel class for development."""
from level import Level
from m1wengine.managers.asset_manager import AssetManager
import game_data


class TestLevel(Level):
    """TestLevel class.

    TestLevel class will instantiate all objects to be tested.
    """

    def __init__(self, universal_assets: list, level_key: str):
        """Initialize base Level class then add in assets to test.

        Parameters
        ----------
        universal_assets: list[pygame.sprite]
            The list containing all game assets which the level will select from
        level_key: str
            The key to the specific level data when parsing gameData.py
        """
        super().__init__(universal_assets, level_key)

        # TODO: this logic should be handled in the level controller
        # and called via methods here. No direct assetmanager access needed.
        self._asset_manager = AssetManager(game_data)
        level_key: str = "test_level"
        self._asset_manager.load_music("level", level_key)
