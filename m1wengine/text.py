"""This module contains the text class."""
import pygame


class Text(pygame.sprite.Sprite):
    """Text class.

    Class for holding in game text.

    Attributes
    ----------
    _text: str
        The text to display
    _font: pygame.font.Font
        The font object to build
    rect: pygame.Rect
        The sprite location rect
    image: pygame.Surface
        The sprite image to render

    Methods
    -------
    __init__(self)
        Initialize the text object
    text_str(self) -> str
        Get the text string value
    text_str(self, new_value)
        Set the text string value
    render_font(self)
        Set the surface for text rendering
    """

    def __init__(self, x_pos, y_pos, text) -> None:
        """Construct the first singleton instance."""
        super().__init__()
        size: int = 20
        self.color: pygame.Color = pygame.Color("black")
        self._text: str = text
        self._font: pygame.font.Font = pygame.font.SysFont("Arial", size)
        self.render_font()
        self.rect: pygame.Rect = pygame.Rect(x_pos, y_pos, 50, 50)

    @property
    def text_string(self) -> str:
        """Get the text string value."""
        return self._text

    @text_string.setter
    def text_string(self, new_value) -> None:
        """Set the text string value.

        Parameters
        ----------
        new_value: int
            New incoming value to set
        """
        self._text = str(new_value)
        self.render_font()

    def render_font(self) -> None:
        """Set the current font for rendering."""
        self.image: pygame.Surface = self._font.render(self._text, 1, self.color)
