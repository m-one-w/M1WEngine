class cameraManager:

    """Camera Manager

    This class will control the position of every rendered sprite in the game.

    As the positions are manipulated, there will be an illusion of camera movement.
    ...

    Attributes
    ----------
    playerCharacter : Player
        the currently shown frame represented by an index
    groups: pygame.sprite.Group
        the speed at which animations run

    Methods
    -------
    setPositions()
        Sets all sprite positions relative to the player character position

    """

    # initialize all groups and their current positions
    def __init__(self, groups, playerCharacter):
        """Constructor

        This method will instantiate the camera controller.

        A single camera controller should be used to manage all rendered sprites.

        Parameters
        ----------
        groups: All currently rendered sprite groups in the game
        playerCharacter: the player character

        """
        # hold each group of sprites in an array or list or whatever

        self.playerCharacter = playerCharacter
        self.sprite_groups = groups

    def setPositions():
        """setPositions

        This method will set the positions of each sprite under class control.

        """
        return
