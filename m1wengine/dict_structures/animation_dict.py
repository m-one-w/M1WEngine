"""This module contains the Animation Dictionary class."""
from typing import TypedDict
import pygame


class AnimationDict(TypedDict):
    """Animation Dictionary class.

    This class is used to define the dictionary structure for animation dictionaries.
    .. code-block::
        {
            'name': str
            'image_rect': pygame.Rect
            'image_count': int
        }
    """

    name: str
    image_rect: pygame.Rect
    image_count: int
