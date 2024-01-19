"""This module contains the Direction class."""
from enum import IntEnum


class Direction(IntEnum):
    """Direction class which contains the enum of all possible directions.

    Attributes
    ----------
    up : int
        the value representing up on a entity compass
    down : int
        the value representing down on a entity compass
    left : int
        the value representing left on a entity compass
    right : int
        the value representing right on a entity compass
    """

    up = -1
    down = 1
    left = -1
    right = 1
    stop = 0
