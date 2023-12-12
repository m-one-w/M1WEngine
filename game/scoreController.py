"""This module contains the ScoreController class."""
SCORE_REDUCE_DAMSEL_DEATH = 6
BOREDOM_REDUCE_DAMSEL_DEATH = 10
SCORE_INCREASE_SKELETON_DEATH = 1
BOREDOM_INCREASE_SKELETON_DEATH = 5


class ScoreController(object):
    """ScoreController class.

    Class for holding all game score information.

    Attributes
    ----------
    _current_score: int
        The current score for the game
    _boredom_meter: int
        The current boredom meter for the game

    Methods
    -------
    __new__(cls)
        Create the class as a singleton object
    __init__(self)
        Initialize the singleton object's starting instance
    current_score(self)
        Get the current score
    current_score(self, new_value)
        Set the current score
    boredom_meter(self)
        Get the boredom meter
    boredom_meter(self, new_value)
        Set the boredom meter
    """

    def __new__(cls):
        """Create a singleton object.

        If singleton already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(ScoreController, cls).__new__(cls)
        return cls.instance

    def __init__(
        self,
    ):
        """Construct the first singleton instance."""
        self._current_score: int = 0
        self._boredom_meter: int = 0

    @property
    def current_score(self) -> int:
        """Get the current score of the player."""
        return self._current_score

    @current_score.setter
    def current_score(self, new_value):
        """Set the new current score.

        Parameters
        ----------
        new_value: int
            New incoming value to set
        """
        if new_value >= 0:
            self._current_score = new_value
        else:
            raise ValueError("Current score cannot be a negative value.")

    @property
    def boredom_meter(self) -> int:
        """Get the boredom_meter of the player."""
        return self._boredom_meter

    @boredom_meter.setter
    def boredom_meter(self, new_value):
        """Set the new boredom meter.

        Parameters
        ----------
        new_value: int
            New incoming value to set
        """
        if new_value >= 0:
            self._boredom_meter = new_value
        else:
            raise ValueError("Boredom meter cannot be a negative value.")

    def bad_entity_destroyed_update_score(self, entity_name: str):
        """Update meta data on bad entity destroyed.

        Checks each individual entity when making updates.

        Parameters
        ----------
        entity_name: str
            The name of the entity
        """
        check = entity_name
        if check == "Skeleton":
            self.current_score += SCORE_INCREASE_SKELETON_DEATH
            self.boredom_meter += BOREDOM_INCREASE_SKELETON_DEATH

    def good_entity_destroyed_update_score(self, entity_name: str):
        """Update meta data on good entity destroyed.

        Checks each individual entity when making updates.

        Parameters
        ----------
        entity_name: str
            The name of the entity
        """
        if entity_name == "Damsel":
            if self.current_score - SCORE_REDUCE_DAMSEL_DEATH < 0:
                self.current_score = 0
            else:
                self.current_score -= SCORE_REDUCE_DAMSEL_DEATH

            if self.boredom_meter - BOREDOM_REDUCE_DAMSEL_DEATH < 0:
                self.boredom_meter = 0
            else:
                self.boredom_meter -= BOREDOM_REDUCE_DAMSEL_DEATH
