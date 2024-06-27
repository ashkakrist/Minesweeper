"""
README:
This script contains TWO object class definitions for playing the Mine Sweeper
game. The two classes are MineSweeper (which is the whole game) and
Tile (which makes up the board of the game).

ADDITIONAL PACKAGES:
random:     A python library used to randomly distribute the mines.
"""

import random


###########################################
############### MineSweeper ###############
###########################################
class MineSweeper:
    """
    DESCRIPTION of the class "MineSweeper":
    The MineSweeper class contains the logic behind the Mine Sweeper game.

    PARAMETERS:
    The parameters that are needed in the __init__ are:
    n_rows (int):       The vertical size of the board.
    n_cols (int):       The horizontal size of the board.
    n_mines (int):      The amount of mines to be distributed on the board.
    safe_radius(int):   The square radius around the first revealed tile where
                        there will be no mines.

    LIMITATIONS:
    1.  The randomly generated games can not always be solved without guessing.
    2.  Tiles that are flagged are not revealed when the reveal method will
        recurse around empty tiles.
    3.  Width of the board changes when an entire column is revealed.

    METHODS:
    self.__init__(n_rows: int, n_cols: int, n_mines: int, safe_radius):
                                Initialises the class.
    self.valid_pos(row, col):   Checks if given row/column coordinates exist on
                                the board.
    self.adjacent(row, col, radius): Returns a set of adjacent tiles in a square
                                radius.
    self.create_board():        Creates a board of tiles in a list of lists.
    self.reveal(row, col):      Reveals a tile on the board, will recurse when
                                it reveals an empty tile.
    self.lay_mines(start_row, start_col): Places mines on the board.
    self.assign_numbers():      Counts the amount of adjacent mines for each tile.
    self.flag(row, col):        Places or removes flag on tile.
    self.game_over():           Checks if the game has been won or lost and
                                triggers corresponding event handlers.
    self.__iter__():            Makes MineSweeper object iterable, looping over a
                                MineSweeper object will go through each tile on
                                the board.
    self.__next__():            Calculates row/column indices and returns tile at
                                those coordinates.
    self.__str__():             Returns basic string representation of minesweeper
                                board.

    STRUCTURES:
    The structures used are elaborated on in the docstring of the methods
    themselves where applicable.

    OUTPUTS:
    The MineSweeper object.
    """

    def __init__(self, n_rows: int, n_cols: int, n_mines: int, safe_radius):
        """
        This method initialises class attributes and creates board:
        safe_radius (int):  The square radius around the first tile where no
                            mines are placed.
        pristine (bool):    True when the player has not revealed any tiles yet
        on_win (list):      Event handler that should be triggered when the game
                            ends in a win.
        on_loss (list):     Event handler that should be triggered when the game
                            ends in a loss.
        """

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_mines = n_mines
        self.safe_radius = safe_radius

        self.create_board()
        self.pristine = True

        # lists for event handlers that trigger when the game is over
        self.on_win = []
        self.on_loss = []

    # checks if specified position exists on the board
    def valid_pos(self, row, col):
        """
        DESCRIPTION:
        This method checks if specified position exists on the board.

        PARAMETERS:
        row (int):  The row coordinate that needs to be verified.
        col (int):  The column coordinate that needs to be verified.

        STRUCTURES:
        And-statement:  used to check if both the row and the column coordinate
                        are valid.

        OUTPUTS:
        Boolean value that is true if the specified position exists on the board,
        or false if it does not exist.
        """

        return row in range(self.n_rows) and col in range(self.n_cols)

    # returns a set of adjacent tiles (including the tile itself) in a square
    # radius
    def adjacent(self, row, col, radius=1):
        """
        DESCRIPTION:
        Returns a set of all adjacent tiles to a specified position on the board.

        PARAMETERS:
        row (int):      The row coordinate of the tile whose adjacent tiles need
                        to be returned.
        col (int):      The column coordinate of the tile whose adjacent tiles
                        need to be returned.
        radius (int):   The square radius around the specified position that needs
                        to be returned; default: 1.
                        When radius is 1, the method returns all tiles in a
                        3 x 3 grid centered around the specified position.
                        When radius is 2, the grid increases to 5 x 5, etc.
                        A set of only the specified tile itself will be returned
                        when the radius is 0.

        STRUCTURES:
        Embedded for-loop:  Is used to go through all row/column coordinates
                            around the specified position.
        If-statement:       Used to check if the row/column coordinates exist on
                            the board.

        OUTPUTS:
        A set of adjacent tiles to the specified position, including the tile at
        the specified position itself.
        """

        tiles = set()

        # loops all row/column indices around the tile
        for i in range(row - radius, row + radius + 1):
            for j in range(col - radius, col + radius + 1):

                # checks if the tile exists on the board, before adding it to
                # the output set
                if self.valid_pos(i, j):
                    tiles.add(self.board[i][j])

        return tiles

    # creates a board of empty tiles
    def create_board(self):
        """
        DESCRIPTION:
        This method creates a board of empty tiles.

        PARAMETERS:
        No additional parameters aside from the MineSweeper attributes itself.

        STRUCTURES:
        Embedded for-loop:  Used to go through all row/column coordinates on the
        board.

        OUTPUTS:
        The method has no output: the MineSweeper object is modified directly.
        """

        self.board = []

        # creates rows
        for i in range(self.n_rows):
            row = []

            # adds tiles to each row
            for j in range(self.n_cols):
                row += [Tile(i, j)]

            # places finished row on board
            self.board += [row]

    # reveals a specified tile
    def reveal(self, row, col):
        """
        DESCRIPTION:
        Reveals a specified tile.

        PARAMETERS:
        row (int):      The row coordinate of the tile that is to be revealed.
        col (int):      The column coordinate of the tile that is to be revealed.

        STRUCTURES:
        If-statement:   Used to check if this is the first time this method is
                        called.
        If-statement:   Used to check if the tile is neither revealed nor flagged.
        If-statement:   Used to check if the method should recurse.
        For-loop:       Used to go through all adjacent tiles.
        Recursion:      Used to reveal adjacent tiles.

        OUTPUTS:
        The method has no output: the Tile object is modified directly.
        """

        # lays mines after the first tile has been selected, so the first tile
        # will never be a mine
        if self.pristine:
            self.lay_mines(row, col)
            self.assign_numbers()
            self.pristine = False

        # selects tile
        tile = self.board[row][col]

        # only reveals tiles that are neither revealed nor flagged
        if not tile.revealed and not tile.flagged:
            tile.revealed = True

            # reveals all surrounding tiles recursively if no mines are adjacent
            if tile.number == 0:
                for neighbour in self.adjacent(row, col):
                    self.reveal(neighbour.row, neighbour.col)

            # checks for game over after reveal
            self.game_over()

    # creates mines on the board
    def lay_mines(self, start_row, start_col):
        """
        DESCRIPTION:
        Randomly distributes mines over the board.

        PARAMETERS:
        start_row (int):    The row coordinate of the first revealed tile.
        start_col (int):    The column coordinate of the first revealed tile.

        STRUCTURES:
        For-loop:   Used to make a set of all tiles on the board.
        For-loop:   Used to place mines on some tiles.

        OUTPUTS:
        The method has no output: the Tile objects are modified directly.
        """
        # creates set of all tiles
        tiles = set()
        for tile in self:
            tiles.add(tile)

        # removes tiles around starting position from the set of potential mines
        tiles = tiles - self.adjacent(start_row, start_col, self.safe_radius)

        # shuffles tiles
        tiles = list(tiles)
        random.shuffle(tiles)

        # lays mines at the first list elements
        for i in range(self.n_mines):
            tiles[i].is_mine = True

    # counts the amount of adjacent mines for each tile
    def assign_numbers(self):
        """
        DESCRIPTION:
        Reveals a specified tile.

        PARAMETERS:
        No additional parameters aside from the MineSweeper attributes itself.

        STRUCTURES:
        For-loop:       Used to go through all tiles.
        For-loop:       Used to count the mines among adjacent tiles.
        If-statement:   Used to check if a tile is a mine.

        OUTPUTS:
        The method has no output: the Tile objects are modified directly.
        """
        for tile in self:
            n_mines = 0
            for neighbour in self.adjacent(tile.row, tile.col):
                if neighbour.is_mine:
                    n_mines += 1

            tile.number = n_mines

    # toggles flag on specified tile
    def flag(self, row, col):
        """
        DESCRIPTION:
        Places or removes flag on specified tile.

        PARAMETERS:
        row (int):      The row coordinate of the tile that is to be flagged.
        col (int):      The column coordinate of the tile that is to be flagged.

        STRUCTURES:
        If-statement:   Used to check if the tile is revealed.

        OUTPUTS:
        The method has no output: the Tile object is modified directly.
        """
        tile = self.board[row][col]

        # inverts flagged status of an unrevealed tile
        if not tile.revealed:
            tile.flagged = not tile.flagged

    # checks if the game is over and triggers corresponding event handlers
    def game_over(self):
        """
        DESCRIPTION:
        Checks if the game is over and whether the player has won or lost.

        PARAMETERS:
        No additional parameters aside from the MineSweeper attributes itself.

        STRUCTURES:
        For-loop:       Used to go through all tiles.
        If-statement:   Used to check if a tile is revealed.
        If-statement:   Used to check if the revealed tile is a mine.
        If-statement:   Used to check if the player has lost. Loss is checked
                        before victory, because it can occur that both win and
                        loss are true. This happens when only one revealed tile
                        remains after a mine is revealed.
                        In such a scenario, the player has lost, so loss should
                        be checked first.
        Elif-statement: Used to check if the player has won.
        For-loop:       Used to trigger event handlers.

        OUTPUTS:
        The proper event handlers are triggered when this method determines that
        the game is over.
        """
        loss = False
        n_hidden = self.n_rows * self.n_cols

        # goes through each tile
        for tile in self:

            # checks if the tile is revealed
            if tile.revealed:
                n_hidden -= 1

                # player loses if revealed tile is a mine
                if tile.is_mine:
                    loss = True

        # player wins if the amount of hidden tiles equals the amount of mines
        win = self.n_mines == n_hidden

        if loss:
            for eventhandler in self.on_loss:
                eventhandler()

        elif win:
            for eventhandler in self.on_win:
                eventhandler()

    # resets n for iteration start
    def __iter__(self):
        '''
        DESCRIPTION:
        This method makes it possible to iterate over the MineSweeper object.
        Looping over the MineSweeper goes through each tile on the board.

        PARAMETERS:
        No additional parameters aside from the MineSweeper attributes itself.

        OUTPUTS:
        The MineSweeper object with attribute n set to 0.
        '''
        self.n = 0
        return self

    # iterates over all tiles
    def __next__(self):
        '''
        DESCRIPTION:
        This method returns the tile at the current point of iteration.

        PARAMETERS:
        No additional parameters aside from the MineSweeper attributes itself.

        STRUCTURES:
        If-statement:   Used to check if the current point of iteration is
                        within the limits of the board.
        StopIteration:  Raised when all tiles have been looped over.

        OUTPUTS:
        1.  The current tile in the iteration
        2.  The MineSweeper object's n attribute is increased by one.
        '''
        if self.n < self.n_rows * self.n_cols:

            # calculates row and column indices
            row = self.n // self.n_cols
            col = self.n % self.n_cols

            tile = self.board[row][col]

            # returns tile and increases n by one for the next iteration
            self.n += 1
            return tile

        # stops iteration when the board size is reached
        else:
            raise StopIteration

    # prints minesweeper board
    def __str__(self):
        '''
        DESCRIPTION:
        Returns string representation of the MineSweeper board.

        PARAMETERS:
        No additional parameters aside from the MineSweeper attributes itself.

        STRUCTURES:
        For-loop:   Used to go through all rows of the board.

        OUTPUTS:
        Each row of the MineSweeper board, separated by newlines.
        '''
        text = []
        for row in self.board:
            text += [str(row)]

        # prints one row per line
        return '\n'.join(text)


###########################################
################### Tile ##################
###########################################
class Tile:
    """
    DESCRIPTION of the class "Tile":
    The Tile class contains information of a tile on the Mine Sweeper board.

    PARAMETERS:
    row (int):      Vertical position of the tile.
    col (int):      Horizontal position of the tile.

    LIMITATIONS:
    1.  There is no way to tell the flagged status of a revealed tile from the string
        representation.
    2.

    METHODS:
    self.__repr__():    Determines and returns the string representation for the
                        different tile states.

    OUTPUTS:
    The Tile object.
    """

    def __init__(self, row, col):
        self.number = 0
        self.row = row
        self.col = col

        self.is_mine = False
        self.revealed = False
        self.flagged = False

    # string representation of tile
    def __repr__(self):
        """
        DESCRIPTION:
        Determines the string representation of the tile.

        PARAMETERS:
        No additional parameters aside from the Tile attributes itself.

        STRUCTURES:
        If-statement:   Used to check if the tile is revealed.
        If-statement:   Used to check if the tile is flagged.
        Elif-statement: Used to check if the tile is a mine.
        Elif-statement: Used to check if the tile's number more than 0.

        OUTPUTS:
        The single-character string representation of the tile.
        """
        if not self.revealed:

            # symbol for flagged tile
            if self.flagged:
                text = '🚩'

            # symbol for unrevealed tile
            else:
                text = ' '

        # symbol for mine
        elif self.is_mine:
            text = '💥'

        # symbol for number tile
        elif self.number > 0:
            text = str(self.number)

        # symbol for empty tile
        else:
            text = '$'

        return text
