"""This module contains the Button class."""


import pygame
from text import Text


class Button(pygame.sprite.Sprite):
    """Button class.

    Class for holding in game buttons.

    Attributes
    ----------
    _x: int
        The x position of the sprite
    _y: int
        The y position of the sprite
    _width: int
        The width of the button
    _height: int
        The height of the button
    _on_click_function: callable
        The function to execute on button clicks
    _one_press: boolean
        If buttons are pressed once per click
    _already_pressed: boolean
        If the button is already pressed
    _button_text_string: str
        Button text to display
    image: pygame.Surface
        Image to display
    rect: pygame.rect
        Rect to store button position
    _text: Text
        Object holding the Text
    _fill_colors: dict
        What colors the button can have

    Methods
    -------
    __init__(self)
        Initialize the button object
    update(self)
        Update the button state
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        button_text: str = "Button",
        on_click_function: callable = None,
        one_press: bool = False,
    ):
        """Initialize a button.

        Parameters
        ----------
        x: int
            The x position of the button
        y: int
            The y position of the button
        width: int
            The width of the button
        height: int
            The height of the button
        button_text
            The string to display on the button
        on_click_function: callable
            The method to run when the button is clicked
        one_press: bool
            Should the button click once or call repeatedly when held
        """
        super().__init__()
        self._x: int = x
        self._y: int = y
        self._width: int = width
        self._height: int = height
        self._on_click_function: callable = on_click_function
        self._one_press: bool = one_press
        self._already_pressed: bool = False
        self._button_text_string: str = button_text
        self.image: pygame.Surface = pygame.Surface((self._width, self._height))
        self.rect: pygame.Rect = pygame.Rect(
            self._x, self._y, self._width, self._height
        )
        self._text: Text = Text(x, y, button_text)

        self._fill_colors = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

    def update(self):
        """Update the state of the button as needed."""
        mouse_position: tuple = pygame.mouse.get_pos()
        self.image.fill(self._fill_colors["normal"])
        if self.rect.collidepoint(mouse_position):
            self.image.fill(self._fill_colors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.image.fill(self._fill_colors["pressed"])
                if self._one_press:
                    self._on_click_function()
                elif not self._already_pressed:
                    self._on_click_function()
                    self._already_pressed = True
            else:
                self._already_pressed = False
        self._text.render_font()
        self.image.blit(self._text.image, (0, 0))
