"""This module contains the CameraManager class."""
import pygame
from tiles.entities.characters.player import Player


class CameraManager(pygame.sprite.Group):
    """Camera Manager class.

    This class will render each sprite in the game at an offset relative to the players
    x and y. As the positions are manipulated, there will be an illusion of camera
    movement.

    Attributes
    ----------
    _player_character: Player
        The currently shown frame represented by an index
    _display_surface: pygame.Surface
        The game surface in which to render all sprites
    _offset: vector2
        The offset at which to render all sprites
    _half_width: int
        Half the display surface width
    _half_height: int
        Half the display surface height
    _offset: vector2
        The offset at which to render all sprites
    _player_character: Player
        The currently shown frame represented by an index

    Methods
    -------
    camera_update(self)
        Renders all sprites relative to the player character position
    """

    # initialize all groups and their current positions
    def __init__(self, player_character: Player) -> None:
        """Construct a CameraManager object.

        This method will instantiate the camera controller.
        A single camera controller should be used to manage all rendered sprites.

        Parameters
        ----------
        player_character: Player
            The player character that entities move around
        """
        super().__init__()
        surfaceX = 0
        surfaceY = 1
        self._display_surface = pygame.display.get_surface()
        self._half_width = (
            self._display_surface.get_size()[surfaceX] // 2
        )  # floor division, returns int
        self._half_height = (
            self._display_surface.get_size()[surfaceY] // 2
        )  # floor division, returns int

        self._offset = pygame.math.Vector2()
        self._player_character = player_character

    def camera_update(self) -> None:
        """Update the camera sprites.

        This method will set the direction of camera sprites to be the
        opposite direction of the player's heading.
        Note that non-player entities will move at a slower speed than the player
        due to being moved in the opposite direction of the player at the
        player's speed.
        """
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # offset = sprite.rect.topleft - self.offset
            prevDirection = sprite.compass.copy()
            sprite.compass = self._player_character.compass.copy() * -1
            sprite.move(self._player_character.speed)
            sprite.compass = pygame.math.Vector2(prevDirection.x, prevDirection.y)
