import pygame
import sys
from settings import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from levels.level import Level
from levels.gameData import level_1


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        # display setup
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Reluctant Hero")
        pygame.display.set_icon(self.screen)
        self.clock = pygame.time.Clock()

        # level csv's are saved in game data
        self.level = Level(level_1, self.screen)

    def run(self):
        while True:
            # check game events
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            # run level
            self.level.run()
            # event handler for menu selection
            # if self.menu_selection == 1:

            # update display based on events
            pygame.display.update()
            self.clock.tick(FPS)


# Start of program
if __name__ == "__main__":
    game = Game()
    game.run()
