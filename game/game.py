"""This module contains the main game class."""
import pygame
import sys
from settings import STUDIO_SPLASH_SCREEN_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from managers.level_manager import LevelManager


class Game:
    """Game class.

    Class for starting the game and loading the LevelManager to handle menus and levels.

    Attributes
    ----------
    _screen: pygame.Surface
        The window the game will run on
    _studio_splash_screen: pygame.Surface
        The studio splash screen to display while booting the game
    _quit_game: bool
        Flag whether to quit the game or continue the game loop
    _level_manager: LevelManager
        The LevelManager which will handle all menu and game assets

    Methods
    -------
    run(self)
        Run the LevelManager and check for exiting game
    """

    def __init__(self):
        """Construct the Game class."""
        # general setup
        pygame.init()
        # display setup
        self._screen: pygame.Surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Reluctant Hero")
        pygame.display.set_icon(self._screen)

        # display studio splash screen while loading game stuff
        self._studio_splash_screen: pygame.Surface = pygame.image.load(
            STUDIO_SPLASH_SCREEN_PATH
        )
        self._screen.blit(
            self._studio_splash_screen,
            (
                (WINDOW_WIDTH - self._studio_splash_screen.get_width()) / 2,
                (WINDOW_HEIGHT - self._studio_splash_screen.get_height()) / 2,
            ),
        )
        pygame.display.update()

        self._quit_game: bool = False
        self._level_manager: LevelManager = LevelManager()

    def run(self):
        """Run the main game loop."""
        while not self._quit_game:
            # check game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self._quit_game = self._level_manager.run()
            pygame.display.update()
        pygame.quit()
        sys.exit()


# Start of program
if __name__ == "__main__":
    game = Game()
    game.run()
