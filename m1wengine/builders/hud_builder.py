"""This module contains the tools to build the HUD class."""
from typing import Callable
import pygame
from m1wengine.text import Text
from m1wengine.button import Button


class HudBuilder(object):
    """Heads Up Display class.

    Class for holding all game score information.

    Methods
    -------
    __new__(cls)
        Create the class as a singleton object
    __init__(self)
        Initialize the singleton object's starting instance
    build_score_info(
        self, coordinates: pygame.Vector2
    ) -> list[pygame.sprite.Sprite]
        Return all sprites in the score info
    build_level_hint_box(
        self, coordinates: pygame.Vector2, hint_str: str
    ) -> list[pygame.sprite.Sprite]
        Return all sprites in the level hint
    build_pause_game_button(
        self, coordinates: pygame.Vector2, method: Callable)
    ) -> list[pygame.sprite.Sprite]
        Return all sprites in the pause button
    add_box(self, rect: pygame.rect.Rect) -> pygame.sprite.Sprite
        Add a box to the HUD
    """

    LEVEL_HINT_DIMENSIONS: pygame.Vector2 = pygame.Vector2(400, 50)
    PAUSE_BUTTON_DIMENSIONS: pygame.Vector2 = pygame.Vector2(50, 30)

    BOX_ALPHA: int = 100

    SIDE_INDENT: int = 5
    LINE_INDENT: int = 20

    def __new__(cls):
        """Create a singleton object.

        If instance already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(HudBuilder, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Construct the first singleton instance."""
        super().__init__()

    def build_score_info(
        self, coordinates: pygame.Vector2
    ) -> list[pygame.sprite.Sprite]:
        """Create all sprites for the HUD score info.

        Parameters
        ----------
        coordinates: pygame.Vector2
            The x and y coordinates to display the pause menu

        Returns
        -------
        score_sprite_list: list[pygame.sprite.Sprite]
            A list of all sprites in the score info section of the HUD
        """
        SCORE_BOX_DIMENSIONS: pygame.Vector2 = pygame.Vector2(150, 50)

        score_sprite_list: list = []

        # define out box rect
        score_rect: pygame.Rect = pygame.Rect(
            coordinates.x,
            coordinates.y,
            SCORE_BOX_DIMENSIONS.x,
            SCORE_BOX_DIMENSIONS.y,
        )

        # add outer box
        score_sprite_list.append(self.add_box(score_rect))

        # define current score text
        self._current_score_sprite: Text = Text(
            coordinates.x + self.SIDE_INDENT,
            coordinates.y,
            "Current Score:",
        )
        score_sprite_list.append(self._current_score_sprite)

        # define current boredom meter
        self._boredom_meter_spr: Text = Text(
            coordinates.x + self.SIDE_INDENT,
            coordinates.y + self.LINE_INDENT,
            "Boredom Meter:",
        )
        score_sprite_list.append(self._boredom_meter_spr)

        return score_sprite_list

    def build_level_hint_box(
        self, coordinates: pygame.Vector2, hint_str: str = "No string provided"
    ) -> list[pygame.sprite.Sprite]:
        """Create all sprites for the level hint box.

        Parameters
        ----------
        coordinates: pygame.Vector2
            The x and y coordinates to display the level hint
        hint_str: str
            The text to display within the level hint

        Returns
        -------
        level_hint_sprites: list[pygame.sprite.Sprite]
            A list of all sprites in the level hint section of the HUD
        """
        level_hint_sprites: list = []

        level_hint_rect: pygame.Rect = pygame.Rect(
            coordinates.x,
            coordinates.y,
            self.LEVEL_HINT_DIMENSIONS.x,
            self.LEVEL_HINT_DIMENSIONS.y,
        )
        level_hint_text: Text = Text(
            coordinates.x + self.SIDE_INDENT,
            coordinates.y,
            hint_str,
        )

        level_hint_sprites.append(self.add_box(level_hint_rect))
        level_hint_sprites.append(level_hint_text)
        return level_hint_sprites

    def build_pause_game_button(
        self, coordinates: pygame.Vector2, method: Callable
    ) -> list[pygame.sprite.Sprite]:
        """Create pause button.

        Parameters
        ----------
        coordinates: pygame.Vector2
            The x and y coordinates to display the pause menu
        method: Callable
            A bound method to run on button clicks

        Returns
        -------
        pause_button_sprites: list[pygame.sprite.Sprite]
            A list of all sprites in the pause button section of the HUD
        """
        pause_button_sprites: list = []

        pause_button_sprites.append(
            Button(
                coordinates.x,
                coordinates.y,
                self.PAUSE_BUTTON_DIMENSIONS.x,
                self.PAUSE_BUTTON_DIMENSIONS.y,
                "Pause",
                method,
            )
        )

        return pause_button_sprites

    def add_box(self, rect: pygame.rect.Rect) -> pygame.sprite.Sprite:
        """Create a background box for HUD elements.

        Parameters
        ----------
        rect: pygame.rect.Rect)
            A rect to fill in as a surface

        Returns
        -------
         sprite: pygame.sprite.Sprite
            A background box sprite component of the HUD
        """
        sprite: pygame.sprite.Sprite = pygame.sprite.Sprite()
        sprite.rect: pygame.rect.Rect = rect
        sprite.image: pygame.surface.Surface = pygame.Surface((rect.width, rect.height))
        sprite.image.fill(pygame.Color("grey"))
        sprite.image.set_alpha(self.BOX_ALPHA)
        return sprite
