"""TestLevel class for development."""
from levels.level import Level


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
