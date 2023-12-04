"""This module contains the main game class."""
import pygame
import sys
from settings import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from levels.levelManager import LevelManager


class Game:
    """Game class."""

    def __init__(self):
        """Construct the Game class."""
        # general setup
        pygame.init()
        # display setup
        self._screen: pygame.surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Reluctant Hero")
        pygame.display.set_icon(self._screen)

        self.level = LevelManager(self._screen)

    def run(self):
        """Run the main game loop."""
        while True:
            # check game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # run level
            self.level.run()

            # update display based on events
            pygame.display.update()
            self.clock.tick(FPS)


# Start of program
if __name__ == "__main__":
    game = Game()
    game.run()
