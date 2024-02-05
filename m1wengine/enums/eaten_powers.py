"""This module contains the eaten powers class."""
from enum import Enum, auto


class EatenPowers(Enum):
    """Direction class which contains the enum of all possible directions.

    Attributes
    ----------
    empty_stomach: Enum
        The value representing an empty stomach
    basic_skeleton: Enum
        The value representing that a basic skeleton was eaten
    damsel: Enum
        The value representing that a damsel was eaten
    """

    empty_stomach = auto()
    basic_skeleton = auto()
    damsel = auto()
    minotaur = auto()
