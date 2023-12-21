"""This module contains the SpriteSheet class."""
import pygame


class SpriteSheet:
    """This class handles sprite sheets.

    Note: When calling images_at the rect is the format:
    (x, y, x + offset, y + offset)

    Attributes
    ----------
    _color_key: pygame.Color
        The background color for the sprite
    _sheet: pygame.Surface
        The animation sheet to display
    """

    def __init__(
        self, image_path: str = None, color_key: pygame.Color | tuple = None
    ) -> None:
        """Load the sheet.

        file_name: str
            The path to the image to load
        color_key: pygame.Color | Tuple
            The color to make the background transparent
        """
        if isinstance(color_key, pygame.Color):
            self._color_key: tuple = (color_key.r, color_key.g, color_key.b)
        else:
            self._color_key: pygame.Color = color_key
        if image_path:
            try:
                self._sheet: pygame.Surface = pygame.image.load(image_path).convert()
            except pygame.error as e:
                print(f"Unable to load spritesheet image: {image_path}")
                raise SystemExit(e)

    def image_at(self, rectangle: tuple) -> pygame.Surface:
        """Load a specific image from a specific rectangle.

        Parameters
        ----------
        rectangle: tuple
            The tuple containing the length and width of image rectangle

        Returns
        -------
        image: pygame.Surface
            The surface containing the image of the specified rect from the animations
        """
        # Loads image from x, y, x+offset, y+offset.
        rect: pygame.Rect = pygame.Rect(rectangle)
        image: pygame.Surface = pygame.Surface(rect.size)
        if self._sheet:
            image.blit(self._sheet, (0, 0), rect)
            image.set_colorkey(self._color_key)
            return image
        else:
            print("Fatal ERROR!! No sprite sheet was set!")

    def images_at(self, rects: list[tuple[int]]) -> list[pygame.Surface]:
        """Load multiple images and return them as a list.

        Parameters
        ----------
        rects: list[tuple[int]]
            The list of rects containing images to go through

        Returns
        -------
        list[pygame.Surface]
            The list of images that were just loaded
        """
        return [self.image_at(rect) for rect in rects]

    def load_strip(self, rect: pygame.Rect, image_count: int) -> list[pygame.Surface]:
        """Load a strip of images, and return them as a list.

        Parameters
        ----------
        rect: pygame.Rect
            The rectangle dimensions for the images
        image_count: int
            The number of images to load

        Returns
        -------
        list[pygame.Surface]
            All loaded images as a list
        """
        tuples: list[tuple] = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tuples)
