"""This module contains the abstract HUD class.

AbstractHud will need further definition in the client side code.
"""
import time
import pygame
from m1wengine.builders.hud_builder import HudBuilder
from abc import ABC, abstractmethod

LEVEL_HINT_COORDINATES: tuple = (500, 400)


class AbstractHud(pygame.sprite.Group, ABC):
    """Heads Up Display class.

    Class for holding the basic HUD definition.

    Attributes
    ----------
    _hud_builder: HudBuilder
        Contains tools to define a custom HUD
    _show_level_hint: bool
        Flag representing if level hint is showing
    _level_paused: bool
        Flag representing if level is paused
    _level_prompt_timer: int
        Contains the timers until level prompt is hidden
    _level_box: pygame.sprite.Sprite
        Contains the level box sprite
    _level_hint_text: pygame.sprite.Sprite
        Contains the level hint prompt string

    Methods
    -------
    __init__(self)
        Initialize the singleton object's starting instance
    start_prompt_timer(self) -> None
        Start timer for displaying level prompt
    add_level_hint(self) -> None
        Display the level hint if needed
    try_close_level_prompt(self) -> None
        Attempt to close out the level prompt
    level_hint(self) -> str
        Get the current level hint
    level_hint(self, new_value: str) -> None
        Set the current level hint
    display_level_hint(self) -> bool
        Display level hint value getter
    display_level_hint(self, new_value: bool) -> None
        Display level hint value setter
    pause_level(self) -> bool
        Pause level value getter
    pause_level(self, new value: bool) -> None
        Pause level value setter
    """

    def __init__(self):
        """Construct the abstract HUD."""
        super().__init__()
        self._hud_builder: HudBuilder = HudBuilder()
        self._show_level_hint: bool = False
        self._level_paused: bool = False
        self._level_prompt_timer: int = 0
        self._level_box: pygame.sprite.Sprite = pygame.sprite.Sprite()
        self._level_hint_text: pygame.sprite.Sprite = pygame.sprite.Sprite()

    @abstractmethod
    def start_prompt_timer(self) -> None:
        """Start the timer for displaying level prompts.

        Raises
        ------
        NotImplementedError: Hud must have a prompt timer method
        """
        raise NotImplementedError("This method must be implemented.")

    def attempt_level_hint_display(self) -> None:
        """Display the level hint if needed."""
        # if text to display, have level hint sprite added
        if self._show_level_hint:
            if not self._level_hint_added_flag:
                self._level_hint_added_flag = True

                level_hint_sprites = self._hud_builder.build_level_hint_box(
                    LEVEL_HINT_COORDINATES, self.level_hint
                )
                self._level_box = level_hint_sprites[0]
                self._level_hint_text = level_hint_sprites[1]
                for sprite in level_hint_sprites:
                    self.add(sprite)
        else:
            # remove level hint prompt sprites
            self._level_box.kill()
            self._level_hint_text.kill()
            self._level_hint_added_flag = False

    def try_close_level_prompt(self) -> None:
        """Check if the prompt timer has ended."""
        current_time = int(time.perf_counter())
        if self._level_prompt_timer < current_time:
            self.display_level_hint = False

    @property
    def level_hint(self) -> str:
        """Get the current level hint text."""
        return self._level_hint_text.text_string

    @level_hint.setter
    def level_hint(self, new_value: str) -> None:
        """Set the current level hint text.

        Parameters
        ----------
        new_value: str
            New level hint to set
        """
        self._level_hint_text.text_string = str(new_value)

    @property
    def display_level_hint(self) -> bool:
        """Get the display level hint value."""
        return self._show_level_hint

    @display_level_hint.setter
    def display_level_hint(self, new_value: bool) -> None:
        """Set the display level hint value.

        Parameters
        ----------
        new_value: bool
            New value to set
        """
        if new_value:
            self._show_level_hint = True
        else:
            self._show_level_hint = False

    @property
    def pause_level(self) -> bool:
        """Get the level paused value."""
        return self._level_paused

    @pause_level.setter
    def pause_level(self, new_value: bool) -> None:
        """Set the level paused value.

        Parameters
        ----------
        new_value: bool
            New value to set
        """
        if new_value:
            self._level_paused = True
        else:
            self._level_paused = False

    def toggle_pause_level(self) -> None:
        """Toggle the pause level value."""
        self.pause_level = not self.pause_level


global_hud: AbstractHud = object()
