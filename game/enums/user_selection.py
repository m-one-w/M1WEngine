"""This module contains the UserSelection class."""
from enum import Enum, auto


class UserSelection(Enum):
    """UserSelection class which contains the enum of all possible user selections.

    Attributes
    ----------
    none: UserSelection
        The value representing the no user selection
    level: UserSelection
        The value representing the level user selection
    quit: UserSelection
        The value represening the quit user selection
    """

    none = auto()
    level = auto()
    quit = auto()
