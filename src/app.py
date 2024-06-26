"""
README:
This code generates the graphical user interface of the minesweeper
playing field.

ADDITIONAL PACKAGES:
tkinter:    A python library used to create the GUI
winsound:   A build in module on Windows that can be used to play sounds.
            (Imported in win OR loss function of the App class, only
            when OS is Windows, not for MacOS.)
config:     A module made to create a GUI that allows the user to choose
            game options
engine:     A module made to run the minesweeper game
"""

import tkinter as tk
import src.engine as engine
import src.config as cfg


###########################################
################### App ###################
###########################################
class App(tk.Tk):
    """
    DESCRIPTION:
    The App creates a GUI

    PARAMETERS:
    The parameters that are needed in the __init__ are:
        rows:           The number of rows of the minesweeper board. Is
                        decided by the user in the config GUI.
        cols:           The number of columns of the minesweeper board. Is
                        decided by the user in the config GUI.
        mines:          The number of mines of the minesweeper board as
                        chosen in the config GUI as well. This number is based
                        on the difficulty and the size that the user selects,
                        the mines are set.
        safe_radius:    The square radius around the first click where no
                        mines are placed.
        right_click:    Default is 3 (Windows). If the user selects that he/she
                        has an apple OS, the value is set to 2.

    METHODS:
    __init__(self):     Initialises the class.
    update_clock(self): Makes sure that the clock at the top of the GUI keeps
                        working until the user wins, loses or ends the game.
    win(self):          Calls function show_popup with a winning message.
    loss(self):         Calls function show_popup with a losing message.
    show_popup(self, message): Creates a pop-up with a label showing the
                        message: "you won" or "you lost", and two buttons:
                        "restart" (calling the function restart) and "quit"
                        (calling the function quit).
    restart(self, popup): Destroys the config screen and starts a new game.
    quit (self, popup): Destroys the config screen.
    create_button_grid(self, rows, cols): Creates a grid of buttons based on
                        the number of rows and columns that are selected in
                        the config GUI.
    on_left_click(self, row, col): Reveals the tile on the board with the same
                        coordinates (row/column) as the button and calls the
                        function update_button_grid.
    on_right_click(self, row, col): Flags the tile on the board with the same
                        coordinates (row/column) as the button.
    update_button_grid(self): Iterates over the board and changes text on the
                        buttons to match the state of the minesweeper board.
                        This is done after every mouse click.

    LIMITATIONS:
    1.  The GUI is slow. This can in part be attributed to Python (it being a
        slow language compared to compiled languages). Another reason can be
        that there are multiple nested for loops in multiple methods which are
        called within each other adding complexity.

    2.  Buttons can change size during the game. This happens when the text
        within a button is changed. The buttons are always changed to the size
        of the largest text within a column.

    3.  The sound effects are only working on Windows computers.

    STRUCTURES:
    The structures used are elaborated on in the docstring of the methods
    themselves where applicable.

    OUTPUT:
    GUI on which the minesweeper game can be played.
    """

    def __init__(self, rows, cols, mines, safe_radius, right_click=3):
        """
        This method initialises the attributes of the class:
        self.title:     Gives the GUI a title.
        self.resizable: To make sure that the user cannot change the size of
                        the GUI.
        self.board:     Minesweeper object.
        self.rows:      Number of rows.
        self.cols:      Number of columns.
        self.buttons:   List of lists with Nones. Has self.rows number of rows
                        and self.columns number of columns.
        self.OS:        Operating system (Windows or Apple). Value is equal to
                        the right_click variable and determined in the
                        Config GUI.
        self.timer:     A label that shows how long the user has been playing
                        the game.
        self.now:       Variable that ensures the timer restarts every new game.
        self.ticking:   Boolean variable, default = True. This variable is
                        changed when a game is won, lost or quit. This variable
                        was added to make sure the timer stops when a game is
                        finished.
        """

        tk.Tk.__init__(self)
        self.title('Minesweeper')
        self.resizable(False, False)
        self.board = engine.MineSweeper(rows, cols, mines, safe_radius)
        self.rows = rows
        self.cols = cols
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.OS = right_click

        # label for timer
        self.timer = tk.Label(self, text=" ", font=('Arial', 40))
        self.timer.grid(row=0, column=2, columnspan=self.cols)
        self.now = 0
        self.ticking = True
        self.update_clock()

        # label for picture of flag
        self.flag_lbl = tk.Label(self,
                                 text='🚩',
                                 font=('Arial', 40))
        self.flag_lbl.grid(row=0, column=0)

        # label that shows number of flags
        self.n_flags_lbl = tk.Label(self,
                                    text=self.board.n_mines,
                                    font=('Arial', 30))
        self.n_flags_lbl.grid(row=0, column=1)

        self.create_button_grid(rows, cols)
        self.board.on_win += [self.win]
        self.board.on_loss += [self.loss]

    def update_n_flags(self):
        """
        DESCRIPTION:
        Function that updates the label on the GUI to show the number of flags
        that still need to be placed by the user to win the game.

        PARAMETERS:
        No additional parameters aside from the App attributes itself.

        STRUCTURES:
        A for-loop that iterates over all the tiles on the minesweeper board to
        count the number of tiles that are flagged. An if-statement that
        reduces the count (= number of mines on board) when a tile is flagged.

        OUTPUT:
        A label that shows the number of flags that still need to be placed by
        the user to win the game.
        """

        count = self.board.n_mines
        for tile in self.board:
            if tile.flagged:
                count -= 1
        self.n_flags_lbl['text'] = count

    def update_clock(self):
        """
        DESCRIPTION:
        Function that ensures that the clock in the GUI is constantly updated.

        PARAMETERS:
        No additional parameters aside from the App attributes itself.

        STRUCTURES:
        If-statement that checks if ticking is still True. If the game is won,
        lost or quit, ticking is set to False and the clock will stop.

        OUTPUT:
        Label that shows how long the user has been playing the game.
        """

        if self.ticking:
            self.now += 1
            now = '%02d : %02d' % (self.now // 60, self.now % 60)
            self.timer.configure(text=now)
            self.timer.after(1000, self.update_clock)

    def win(self):
        """
        DESCRIPTION:
        Function that sets ticking to False and calls the show_popup function
        with the message: "You won!"

        PARAMETERS:
        No additional parameters aside from the App attributes itself.

        OUTPUT:
        A pop-up GUI that tells the uses that he/she has won the game. The
        popup also contains two buttons; the user can choose to quit or
        restart the game. The function also plays a winning sound on Windows.
        """

        self.ticking = False
        self.show_popup("You won!")
        if self.OS == 3:
            import winsound
            winsound.PlaySound('assets\\winning.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)

    def loss(self):
        """
        DESCRIPTION:
        Function that sets ticking to False and calls the show_popup function
        with the message: "You lost!"

        PARAMETERS:
        No additional parameters aside from the App attributes itself.

        OUTPUT:
        A pop-up GUI that tells the uses that he/she has lost the game. The
        popup also contains two buttons; the user can choose to quit or restart
        the game. The function also plays an explosion sound on Windows.
        """

        self.ticking = False
        self.show_popup("You lost!")
        if self.OS == 3:
            import winsound
            winsound.PlaySound('assets\\explosion.wav',
                               winsound.SND_FILENAME | winsound.SND_ASYNC)

    def show_popup(self, message):
        """
        DESCRIPTION:
        A function that creates a pop up GUI in which the user receives a
        message that he/she has lost or won the game. The pop-up also has two
        buttons; exit and restart. The exit button calls the function quit.
        The restart button calls the function restart.

        PARAMETERS:
        message:    a string variable that is defined in the function win or
                    lost.

        OUTPUT:
        A pop-up GUI that tells the user that he/she has won or lost the game.
        The user can click on one of two buttons; exit or restart.
        """

        popup = tk.Toplevel(self)
        popup.title("Game Over")
        popup.geometry("300x100")

        label = tk.Label(popup, text=message)
        label.pack(pady=10)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        exit_button = tk.Button(button_frame,
                                text="Exit",
                                command=lambda: self.quit(popup))
        exit_button.pack(side=tk.LEFT, padx=10)

        restart_button = tk.Button(button_frame,
                                   text="Restart",
                                   command=lambda: self.restart(popup))
        restart_button.pack(side=tk.RIGHT, padx=10)

    def restart(self, popup):
        """
        DESCRIPTION:
        A function that destroys the current config screen and restarts the
        game.

        PARAMETERS:
        popup:  the pop-up that is shown to the user. It is needed by the \
                function so it is able to destroy it.

        OUTPUT:
        A new minesweeper game.
        """

        popup.destroy()
        self.destroy()
        app = cfg.StartScreen()
        app.mainloop()

    def quit(self, popup):
        """
        DESCRIPTION:
        A function that destroys the current config screen.

        PARAMETERS:
        popup:  the pop-up that is shown to the user. It is needed by the
                function so it is able to destroy it.

        OUTPUT:
        None.
        """

        popup.destroy()
        self.destroy()

    def create_button_grid(self, rows, cols):
        """
        DESCRIPTION:
        A function that creates the grid of buttons based on the number of
        rows and columns that are selected in the config GUI.

        PARAMETERS:
        rows:       the number of rows for which buttons should be created.
        cols:       the number of columns for which buttons should be created.

        STRUCTURES:
        An embedded for-loop is used to go through all row/column coordinates
        that have to be on the button grid. On every row/column coordinate a
        button is created.

        OUTPUT:
        A grid of buttons with rows number of rows and cols number of columns.
        """

        for r in range(rows):
            for c in range(cols):
                button = tk.Button(self,
                                   text=self.board.board[r][c].__repr__(),
                                   width=4, height=2)
                button.bind('<Button-1>',
                            lambda event, row=r,
                                   col=c: self.on_left_click(row, col))
                button.bind('<Button-%d>' % self.OS,
                            lambda event, row=r,
                                   col=c: self.on_right_click(row, col))
                button.grid(row=r + 1, column=c, padx=1, pady=1, sticky=tk.NSEW)
                self.buttons[r][c] = button

    def on_left_click(self, row, col):
        """
        DESCRIPTION:
        A function that is called when the user uses a left mouse click on the
        button. It reveals the tile and calls the function update_button_grid.

        PARAMETERS:
        row(int):   The row coordinate of the button.
        col(int):   The column coordinate of the button.

        OUTPUT:
        An updated app with at least one extra revealed button.
        """

        self.board.reveal(row, col)
        self.update_button_grid()

    def on_right_click(self, row, col):
        """
        DESCRIPTION:
        A function that is called when the user uses a right mouse click on the
        button. It flags the tile, calls the function update_button_grid and
        update_n_flags.

        PARAMETERS:
        row(int):   The row coordinate of the button
        col(int):   The column coordinate of the button

        OUTPUT:
        An updated App GUI with that shows a flag on the button that was
        right-clicked and an updated label that shows how many flags the user
        still needs to place to win the game.
        """

        self.board.flag(row, col)
        self.update_button_grid()
        self.update_n_flags()

    def update_button_grid(self):
        """
        DESCRIPTION:
        Updates the button grid after the player performs an action. If it is
        an empty tile, the button is removed, and if it is a numbered tile,
        the button is transformed into a label, so that the player can't
        interact with an already revealed tile.

        PARAMETERS:
        No additional parameters aside from the App attributes itself.

        STRUCTURES:
        2 for loops:        To go through each tile in the playing field.
        2 if statements:    To check whether the tile is empty or numbered
                            (a safe tile that shouldn't be interacted with
                            anymore).

        OUTPUT:
        None.
        """

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(
                    text=self.board.board[r][c].__repr__())
                if self.board.board[r][c].__repr__() == '$':
                    self.buttons[r][c].grid_remove()
                if self.board.board[r][c].__repr__().isdigit():
                    label = tk.Label(self,
                                     text=self.board.board[r][c].__repr__(),
                                     width=4, height=2, borderwidth=1)
                    label.grid(row=r + 1, column=c, padx=5, pady=5)
                    self.buttons[r][c].grid_remove()
                    self.buttons[r][c] = label
