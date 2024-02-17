"""This module contains the Button class."""


import pygame
from m1wengine.text import Text


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
        text,
        splitter: str = '',
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
        text: str
            The string or list to be displayed on the button
        splitter: str
            a char that would split the string into separate elements
        on_click_function: callable
            The method to run when the button is clicked
        one_press: bool
            Should the button click once or call repeatedly when held
        """

        super().__init__()
        # Splits text into a list
        self.index = 0
        self.Button_Texts_List = []
        self.button_text = ''
        if type(text) == str:
            if splitter != '':
                self.Button_Texts_List = text.split(splitter)
            else:
                self.Button_Texts_List = [text]
        elif type(text) == list:
            self.Button_Texts_List = text
        self.button_text = self.Button_Texts_List[self.index]
        # Dimensions
        self.__x: int = x
        self.__y: int = y
        self.__width: int = width
        self.__height: int = height
        # Clicking functionaliti
        self._on_click_function: callable = on_click_function
        self.__on_press: bool = one_press
        self.__already_pressed: bool = False
        self.image: pygame.Surface = pygame.Surface((self.__width, self.__height))
        self.rect: pygame.Rect = pygame.Rect(
            self.__x, self.__y, self.__width, self.__height
        )
        self.__text: Text = Text(x, y, self.button_text)
        self.__text: Text = Text(x, y, self.button_text)

        self.__fill_colors: dict[str, str] = {
            "normal": "#ffffff",
            "hover": "#666666",
            "pressed": "#333333",
        }

    def iterate_text_list(self):
        """Increase the index to change the displayed text and reset index if its already on the last element"""
        if self.Button_Texts_List[self.index] == self.Button_Texts_List[-1]:
            self.index = 0
        else:
            self.index += 1

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


