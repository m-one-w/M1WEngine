"""This module contains the Button class."""


import pygame
from text import Text


class Button(pygame.sprite.Sprite):
    """Button class.

    Class for holding in game buttons.

    Attributes
    ----------
    __x: int
        The x position of the sprite
    __y: int
        The y position of the sprite
    __width: int
        The width of the button
    __height: int
        The height of the button
    _on_click_function: callable
        The function to execute on button clicks
    __on_press: bool
        If buttons are pressed once per click
    __already_pressed: bool
        If the button is already pressed
    image: pygame.Surface
        Image to display
    rect: pygame.Rect
        Rect to store button position
    __text: Text
        Object holding the Text
    __fill_colors: dict[str, str]
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
        self.__x: int = x
        self.__y: int = y
        self.__width: int = width
        self.__height: int = height
        self._on_click_function: callable = on_click_function
        self.__on_press: bool = one_press
        self.__already_pressed: bool = False
        self.image: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.rect: pygame.Rect = pygame.Rect(
            self.__x, self.__y, self.__width, self.__height
        )
        self.__text: Text = Text(x, y, button_text)

        self.__fill_colors: dict[str, str] = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

    def update(self):
        """Update the state of the button as needed."""
        mouse_position: tuple = pygame.mouse.get_pos()
        self.image.fill(self.__fill_colors["normal"])
        if self.rect.collidepoint(mouse_position):
            self.image.fill(self.__fill_colors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.image.fill(self.__fill_colors["pressed"])
                if self.__on_press:
                    self._on_click_function()
                elif not self.__already_pressed:
                    self._on_click_function()
                    self.__already_pressed = True
            else:
                self.__already_pressed = False
        self.__text.render_font()
        self.image.blit(self.__text.image, (0, 0))
