"""This module contains the HUD class.

A HUD definition is provided within this module and used to
set the M1WEngine global hud.
"""
import time
from m1wengine.abstract_HUD import AbstractHud
from m1wengine.text import Text
from m1wengine.score_controller import ScoreController
import pygame


class HeadsUpDisplay(AbstractHud):
    """Heads Up Display class.

    Class for holding the basic HUD definition.

    Attributes
    ----------
    _score_controller: ScoreController
        Contains score information needed by the HUD elements
    _current_score: pygame.sprite.Sprite
        Contains the current score sprite
    _boredom_meter: pygame.sprite.Sprite
        Contains the boredom meter sprite

    Methods
    -------
    __new__(cls) -> AbstractHud
        Create the class as a singleton object
    __init__(self) -> AbstractHud
        Initialize the singleton object's starting instance
    start_prompt_timer(self) -> None
        Start timer for displaying level prompt
    update(self) -> None
        Update the displayed HUD information
    """

    PAUSE_BUTTON_COORDINATES: pygame.Vector2 = pygame.Vector2(700, 50)
    SCORE_INFO_COORDINATES: pygame.Vector2 = pygame.Vector2(10, 10)
    LEVEL_PROMPT_SHOW_TIME_SECONDS: int = 4

    def __new__(cls) -> AbstractHud:
        """Create a singleton object.

        If singleton already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(HeadsUpDisplay, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> AbstractHud:
        """Construct the first singleton instance."""
        super().__init__()
        self._score_controller: ScoreController = ScoreController()
        score_sprites: list[pygame.sprite.Sprite] = self._hud_builder.build_score_info(
            self.SCORE_INFO_COORDINATES
        )
        self._current_score: Text = score_sprites[1]
        self._boredom_meter: Text = score_sprites[2]

        for sprite in score_sprites:
            self.add(sprite)

        pause_sprites: list[
            pygame.sprite.Sprite
        ] = self._hud_builder.build_pause_game_button(
            self.PAUSE_BUTTON_COORDINATES, self.toggle_pause_level
        )
        for sprite in pause_sprites:
            self.add(sprite)

        AbstractHud.global_hud: HeadsUpDisplay = self

    def start_prompt_timer(self) -> None:
        """Start the timer for displaying level prompts."""
        self._level_prompt_timer: int = (
            int(time.perf_counter()) + self.LEVEL_PROMPT_SHOW_TIME_SECONDS
        )
        self.display_level_hint: bool = True

    def update(self) -> None:
        """Run the HUD."""
        super().update()
        self._current_score.text_string: str = "Current Score: " + str(
            self._score_controller.current_score
        )
        self._boredom_meter.text_string: str = "Boredom Meter: " + str(
            self._score_controller.current_score
        )
        self.attempt_level_hint_display()
