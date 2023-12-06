"""This module contains the MainMenu class."""
import pygame
import pygame_menu
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, MAIN_MENU_BACKGROUND_PATH


class MainMenu(pygame_menu.Menu):
    """Main Menu Level.

    This class will manage and load all sprites for the main menu level.

    Attributes
    ----------
    _menu_image: pygame.Surface
        The background image for the main menu

    Methods
    -------
    set_user_selection(self, selection: str)
    """

    def __init__(self):
        """Construct the main menu class.

        This method will instantiate all required sprite groups for the main menu level
        """
        super().__init__("Main Menu", WINDOW_WIDTH, WINDOW_HEIGHT)
        self._menu_image: pygame.Surface = pygame.image.load(MAIN_MENU_BACKGROUND_PATH)
        self._display_surface = pygame.display.get_surface()
        # create pygame_menu options for the main menu
        self.add_menu_options()
        # TODO: self._user_selection should be Enum
        self._user_selection: str = "None"

    def set_user_selection(self, selection: str) -> None:
        """Set user selection for MainMenu.

        Intended for use in LevelManager.

        Parameters
        ----------
        selection: str
            New incoming value to set
        """
        self._user_selection = selection

    def get_user_selection(self) -> str:
        """Get user selection for LevelManager."""
        return self._user_selection

    def add_menu_options(self) -> None:
        """Add all menu options to the main menu."""
        # add 'Play' button to load a level
        self.add.button(title="Play", action=self.start_game)
        # add a difficulty selector
        self.add.selector(
            "Difficulty: ",
            [("EASY", 0), ("NORMAL", 1), ("HARD", 2)],
            onchange=self.set_difficulty,
        )
        # add 'Quit' button
        self.add.button(title="Quit", action=pygame_menu.events.EXIT)

    def start_game(self) -> None:
        """Change status of user_selection to load a level and disable main menu."""
        self.set_user_selection("Level")
        self.disable()

    def set_difficulty(self, value: tuple, difficulty: str) -> None:
        """Handle side effects of changing difficulty selector."""
        pass

    def run(self) -> None:
        """Draw and update all sprite groups."""
        self._display_surface.blit(self._menu_image, (0, 0))
        # run the menu, create infinite loop until menu is closed
        self.mainloop(self._display_surface)
