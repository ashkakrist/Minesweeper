"""
README:
This script contains two object class definitions for playing the Mine Sweeper game.
The two classes are MineSweeper, which is the whole game, and Tile, which make up the board of the game.
"""
import random


# class for minesweeper game
class MineSweeper:
    """
    DESCRIPTION:
    The MineSweeper class contains the logic behind the Mine Sweeper game.

    PARAMETERS:
    - n_rows (int): the vertical size of the board
    - n_cols (int): the horizontal size of the board
    - n_mines (int): the amount of mines to be distributed on the board
    - safe_radius(int): the square radius around the first revealed tile where there will be no mines

    LIMITATIONS:
    - The randomly generated games can not always be solved without guessing.
    - Tiles that are flagged are not revealed when the reveal method recurses around empty tiles.

    METHODS:
    - self.valid_pos(row, col): checks if given row/column coordinates exist on the board
    - self.adjacent(row, col, radius): returns a set of adjacent tiles in a square radius
    - self.create_board(): creates a board of tiles in a list of lists
    - self.reveal(row, col): reveals a tile on the board, recurses when it reveals an empty tile
    - self.lay_mines(start_row, start_col): places mines on the board
    - self.assign_numbers(): counts the amount of adjacent mines for each tile
    - self.flag(row, col): places or removes flag on tile
    - self.game_over(): checks if the game has been won or lost and triggers corresponding eventhandlers
    - self.__iter__(): makes MineSweeper object iterable, looping over a MineSweeper object will go through each tile on the board
    - self.__next__(): calculates row/column indices and returns tile at those coordinates
    - self.__str__(): returns basic string representation of minesweeper board

    OUTPUTS:
    - the MineSweeper object
    """

    def __init__(self, n_rows: int, n_cols: int, n_mines: int, safe_radius):
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
        return row in range(self.n_rows) and col in range(self.n_cols)

    # returns a set of adjacent tiles (including the tile itself) in a square radius
    def adjacent(self, row, col, radius=1):
        tiles = set()

        # loops all row/column indices around the tile
        for i in range(row - radius, row + radius + 1):
            for j in range(col - radius, col + radius + 1):

                # checks if the tile exists on the board, before adding it to the output set
                if self.valid_pos(i, j):
                    tiles.add(self.board[i][j])

        return tiles

    # creates a board of empty tiles
    def create_board(self):
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
        '''
        reveals specified tile;
        tile must be specified by giving the row and column coordinates (int) as input;
        the minefield is created only after the first time reveal is called;
        this is to ensure that the first tile revealed will never be a mine;
        checks that the tile is neither revealed nor flagged before revealing it;
        if the revealed tile has zero adjacent mines, the method recursively reveal each adjacent tile
        '''

        # lays mines after the first tile has been selected, so the first tile will never be a mine
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
        for tile in self:
            n_mines = 0
            for neighbour in self.adjacent(tile.row, tile.col):
                if neighbour.is_mine:
                    n_mines += 1

            tile.number = n_mines

    # toggle flag on specified tile
    def flag(self, row, col):
        '''
        toggles the flagged status of a tile;
        tile must be specified by giving the row and column coordinates (int) as input;
        only tiles that are not revealed can be flagged;
        flagged tiles cannot be revealed
        '''

        tile = self.board[row][col]

        # inverts flagged status of an unrevealed tile
        if not tile.revealed:
            tile.flagged = not tile.flagged

    # checks if the game is over and triggers corresponding event handlers
    def game_over(self):
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
        self.n = 0
        return self

    # iterates over all tiles
    def __next__(self):
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
        text = []
        for row in self.board:
            text += [str(row)]

        # prints one row per line
        return '\n'.join(text)


# class for minesweeper tile
class Tile:
    """
    DESCRIPTION:
    The Tile class contains information of a tile on the Mine Sweeper board.

    PARAMETERS:
    - row (int): vertical position of the tile
    - col (int): horizontal position of the tile

    LIMITATIONS:
    - There is no way to tell the flagged status of a revealed tile from the string representation

    METHODS:
    self.__repr__(): determines and returns the string representation for the different tile states

    OUTPUTS:
    - the Tile object
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
