"""This module contains the HUD class."""
import pygame
from button import Button
from score_controller import ScoreController
from text import Text


class HeadsUpDisplay(pygame.sprite.Group):
    """Heads Up Display class.

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
    init_score_info(self)
        Init score information
    toggle_pause_level(self)
        Toggle the level pause value
    add_box(self, rect, height, width) -> pygame.sprite.Sprite
        Add a box to the HUD
    update(self)
        Update sprites on the HUD
    add_level_hint(self)
        Display level hint value getter
    display_level_hint(self, new_value: bool)
        Display level hint value setter
    pause_level(self)
        Pause level value getter
    pause_level(self, new value: bool)
        Pause level value setter
    """

    SCORE_BOX_X_PX = 20
    SCORE_BOX_Y_PX = 50
    SCORE_BOX_HEIGHT = 150
    SCORE_BOX_WIDTH = 50
    SCORE_BOX_VALUE_X_SCORE = SCORE_BOX_X_PX + 107
    SCORE_BOX_VALUE_X_BOREDOM = SCORE_BOX_X_PX + 120

    LEVEL_HINT_BOX_X_PX = 500
    LEVEL_HINT_BOX_Y_PX = 600
    LEVEL_HINT_BOX_HEIGHT = 50
    LEVEL_HINT_BOX_WIDTH = 400

    PAUSE_BUTTON_X = 700
    PAUSE_BUTTON_Y = 30
    PAUSE_BUTTON_WIDTH = 50
    PAUSE_BUTTON_HEIGHT = 30

    BOX_ALPHA = 100

    def __new__(cls):
        """Create a singleton object.

        If instance already exists returns the previous singleton object
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(HeadsUpDisplay, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Construct the first singleton instance."""
        super().__init__()
        self._score: ScoreController = ScoreController()
        self._show_level_hint: bool = False
        self._level_hint_added_flag: bool = False
        self._level_hint_text: str = ""
        self._level_paused: bool = False

        self.init_score_info()

        pause_button_sprite: Button = Button(
            self.PAUSE_BUTTON_X,
            self.PAUSE_BUTTON_Y,
            self.PAUSE_BUTTON_WIDTH,
            self.PAUSE_BUTTON_HEIGHT,
            "Pause",
            self.toggle_pause_level,
        )
        self.add(pause_button_sprite)

    def init_score_info(self) -> None:
        """Initialize the score information area."""
        score_rect: pygame.Rect = pygame.Rect(
            self.SCORE_BOX_X_PX,
            self.SCORE_BOX_Y_PX,
            self.SCORE_BOX_WIDTH,
            self.SCORE_BOX_HEIGHT,
        )
        self.add(self.add_box(score_rect, self.SCORE_BOX_HEIGHT, self.SCORE_BOX_WIDTH))
        self.__current_score_sprite: Text = Text(
            self.SCORE_BOX_X_PX,
            self.SCORE_BOX_Y_PX,
            "Current Score:",
        )
        self.add(self.__current_score_sprite)
        self.__boredom_meter_spr: Text = Text(
            self.SCORE_BOX_X_PX,
            self.SCORE_BOX_Y_PX + 20,
            "Boredom Meter:",
        )
        self.add(self.__boredom_meter_spr)
        self.__current_score_value_sprite: Text = Text(
            self.SCORE_BOX_VALUE_X_SCORE,
            self.SCORE_BOX_Y_PX + 1,
            str(self._score.current_score),
        )
        self.add(self.__current_score_value_sprite)
        self.__boredom_meter_value_sprite: Text = Text(
            self.SCORE_BOX_VALUE_X_BOREDOM,
            self.SCORE_BOX_Y_PX + 21,
            str(self._score.boredom_meter),
        )
        self.add(self.__boredom_meter_value_sprite)

    def toggle_pause_level(self) -> None:
        """Toggle the pause level value."""
        self.pause_level = not self.pause_level

    def add_box(self, rect, height, width) -> pygame.sprite.Sprite:
        """Create a background box for HUD elements."""
        sprite: pygame.sprite.Sprite = pygame.sprite.Sprite()
        sprite.rect = rect
        sprite.image = pygame.Surface((height, width))
        sprite.image.fill(pygame.Color("grey"))
        sprite.image.set_alpha(self.BOX_ALPHA)
        return sprite

    def update(self):
        """Run the HUD."""
        super().update()
        self.__current_score_value_sprite.text_string = self._score.current_score
        self.__boredom_meter_value_sprite.text_string = self._score.boredom_meter
        self.add_level_hint()

    def add_level_hint(self):
        """Display the level hint if needed."""
        # if text to display, have level hint sprite added
        if self._show_level_hint:
            if not self._level_hint_added_flag:
                self._level_hint_added_flag = True

                level_hint_rect: pygame.Rect = pygame.Rect(
                    self.LEVEL_HINT_BOX_X_PX,
                    self.LEVEL_HINT_BOX_Y_PX,
                    self.LEVEL_HINT_BOX_WIDTH,
                    self.LEVEL_HINT_BOX_HEIGHT,
                )
                self._level_box_spr: pygame.sprite.Sprite = self.add_box(
                    level_hint_rect,
                    self.LEVEL_HINT_BOX_WIDTH,
                    self.LEVEL_HINT_BOX_HEIGHT,
                )
                self.add(self._level_box_spr)
                self._level_hint_txt_sprite: Text = Text(
                    self.LEVEL_HINT_BOX_X_PX,
                    self.LEVEL_HINT_BOX_Y_PX + 10,
                    str(self._level_hint_text),
                )
                self.add(self._level_hint_txt_sprite)

    @property
    def level_hint(self) -> str:
        """Get the current level hint text."""
        return self._level_hint_text

    @level_hint.setter
    def level_hint(self, new_value: bool):
        """Set the current level hint text.

        Parameters
        ----------
        new_value: str
            New level hint to set
        """
        self._level_hint_text = str(new_value)

    @property
    def display_level_hint(self) -> bool:
        """Get the display level hint value."""
        return self._show_level_hint

    @display_level_hint.setter
    def display_level_hint(self, new_value: bool):
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
    def pause_level(self, new_value: bool):
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
