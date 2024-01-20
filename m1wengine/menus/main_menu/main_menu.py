"""This module contains the MainMenu class."""
import pygame
import pygame_menu
from m1wengine.settings import WINDOW_WIDTH, WINDOW_HEIGHT, MAIN_MENU_BACKGROUND_PATH
from m1wengine.enums.user_selection import UserSelection


class MainMenu(pygame_menu.Menu):
    """Main Menu Level.

    This class will create menu options for the main menu in addition to
    handling user input and returning to LevelManager.

    Attributes
    ----------
    _menu_image: pygame.Surface
        The background image for the main menu
    _display_surface: pygame.Surface
        The surface window the game is rendered on
    _user_selection: str
        Exit condition flag returned to LevelManager

    Methods
    -------
    __init__(self)
        Initialize the menu
    user_selection(self) -> UserSelection
        Get the _user_selection
    user_selection(self, selection: UserSelection) -> None
        Sets the _user_selection
    add_menu_options(self, selection: str)
        Create all buttons and selectors for the menu
    start_game(self)
        Changes user selection to Level instance and disables the menu
    set_difficulty(self, value: tuple, difficulty: str)
        Handle side effects of changing the difficulty selector
    run(self)
        Draw the menu to the display surface and start the menuLoop
    """

    def __init__(self) -> None:
        """Construct the main menu class.

        This method will instantiate all required sprite groups for the main menu level
        """
        self._menu_image: pygame.Surface = pygame.image.load(MAIN_MENU_BACKGROUND_PATH)
        super().__init__("Main Menu", WINDOW_WIDTH, WINDOW_HEIGHT)
        self._display_surface: pygame.Surface = pygame.display.get_surface()
        # create pygame_menu options for the main menu
        self.add_menu_options()
        # TODO: self._user_selection should be Enum
        self._user_selection: UserSelection = UserSelection.none

    @property
    def user_selection(self) -> UserSelection:
        """Get user selection for LevelManager."""
        return self._user_selection

    @user_selection.setter
    def user_selection(self, selection: UserSelection) -> None:
        """Set user selection for MainMenu.

        Intended for use in LevelManager.

        Parameters
        ----------
        selection: UserSelection
            New incoming value to set

        Raises
        ------
        TypeError: parameter must be of UserSelection type
        """
        if type(selection) is not UserSelection:
            raise TypeError(
                "ERROR: a UserSelection enum value must be passed in as the selection."
            )
        else:
            self._user_selection = selection

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
        self.user_selection = UserSelection.level
        self.disable()

    def set_difficulty(self, value: tuple, difficulty: str) -> None:
        """Handle side effects of changing difficulty selector.

        Parameters
        ----------
        value: tuple
            The selector difficulty as a (str, int)
        difficulty: str
            The string representing the difficulty
        """
        pass

    def run(self) -> None:
        """Draw and update all sprite groups."""
        self._display_surface.blit(self._menu_image, (0, 0))
        # run the menu, create infinite loop until menu is closed
        self.mainloop(self._display_surface)
