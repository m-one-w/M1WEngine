"""This module contains the Action class."""
from enum import Enum, auto


class Actions(Enum):
    """Action class which contains the enum of all possible actions.

    Attributes
    ----------
    throw: Actions
        The value representing the action of throwing
    destroy: Actions
        The value representing the action of destroying
    consume: Actions
        The value representing the action of eating/consuming
    """

    throw = auto()
    destroy = auto()
    consume = auto()
    none = auto()
