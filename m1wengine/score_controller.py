"""This module contains the ScoreController class."""


class ScoreController(object):
    """ScoreController class.

    Class for holding all game score information.

    Attributes
    ----------
    score_dictionary: static dict[str, dict[str, int]]
        The NPC death score and boredom meter numbers
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
    current_score(self, new_value: int)
        Set the current score
    boredom_meter(self)
        Get the boredom meter
    boredom_meter(self, new_value: int)
        Set the boredom meter
    """

    score_dictionary = {
        "damsel_death": {
            "score": 6,
            "boredom": 10,
        },
        "skeleton_death": {
            "score": 1,
            "boredom": 5,
        },
        "minotaur_death": {"score": 1, "boredom": 5},
    }

    def __new__(cls):
        """Create a singleton object.

        If singleton already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(ScoreController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Construct the first singleton instance."""
        self._current_score: int = 0
        self._boredom_meter: int = 100

    @property
    def current_score(self) -> int:
        """Get the current score of the player."""
        return self._current_score

    @current_score.setter
    def current_score(self, new_value: int):
        """Set the new current score.

        Parameters
        ----------
        new_value: int
            New incoming value to set

        Raises
        ------
        ValueError: the current score must be a non-negative integer
        """
        if isinstance(new_value, int) and new_value >= 0:
            self._current_score = new_value
        else:
            raise ValueError("Current score cannot be a negative value.")

    @property
    def boredom_meter(self) -> int:
        """Get the boredom_meter of the player."""
        return self._boredom_meter

    @boredom_meter.setter
    def boredom_meter(self, new_value: int):
        """Set the new boredom meter.

        Parameters
        ----------
        new_value: int
            New incoming value to set

        Raises
        ------
        ValueError: Boredom meter must be a non-negative integer
        """
        if isinstance(new_value, int) and new_value >= 0:
            self._boredom_meter = new_value
        else:
            raise ValueError("Boredom meter cannot be a negative value.")

    def bad_entity_destroyed_update_score(self, entity_name: str) -> None:
        """Update meta data on bad entity destroyed.

        Checks each individual entity when making updates.

        Parameters
        ----------
        entity_name: str
            The name of the entity

        Raises
        ------
        ValueError: entity_name was not found in the score_dictionary
        """
        check = entity_name
        if check == "Skeleton":
            self.current_score += self.score_dictionary["skeleton_death"]["score"]
            self.boredom_meter += self.score_dictionary["skeleton_death"]["boredom"]
        elif check == "Minotaur":
            self.current_score += self.score_dictionary["minotaur_death"]["score"]
            self.boredom_meter += self.score_dictionary["minotaur_death"]["boredom"]
        else:
            raise ValueError("Unknown entity type. Not found in score_dictionary.")

    def good_entity_destroyed_update_score(self, entity_name: str) -> None:
        """Update meta data on good entity destroyed.

        Checks each individual entity when making updates.

        Parameters
        ----------
        entity_name: str
            The name of the entity

        Raises
        ------
        ValueError: Entity name not found in score_dictionary
        """
        if entity_name == "Damsel":
            score_reduce: int = self.score_dictionary["damsel_death"]["score"]
            if self.current_score - score_reduce < 0:
                self.current_score = 0
            else:
                self.current_score -= score_reduce

            if self.boredom_meter - score_reduce < 0:
                self.boredom_meter = 0
            else:
                self.boredom_meter -= score_reduce
        else:
            raise ValueError("Entity type not found in score_dictionary.")
