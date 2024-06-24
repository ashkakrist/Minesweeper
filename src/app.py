"""
README:
    This code generates the graphical user interface of the minesweeper playfield.

ADDITIONAL PACKAGES:
    tkinter - a python library used to create the GUI
    config - a module made to create a GUI that allowes the user to choose game options
    engine - a module made to run the minesweeper game
"""

import tkinter as tk
import src.engine as engine
import src.config as cfg


class App(tk.Tk):
    """
    DESCRIPTION:
    The App creates a GUI

    PARAMETERS:
    The parameters that are needed in the __innit__ are:
        - rows: number of rows of the minesweeper board. Is decided by the user in the config GUI.
        - cols: number of columns of the minesweeper board. Is decided by the user in the config GUI.
        - mines: number of mines of the minesweeper board. Is chosen in the config GUI as well.
                 Based on the difficulty and the size that the user selects. The number of mines is set.
        - safe_radius: the square radius around the first click where no mines are placed.
        - right_click: default is 3 (Windows). If the user selects that he/she has an apple OS, the value is set to 2.

    METHODS:
    - __init__ (self): initialises the class.
    - update_clock(self): makes sure that the clock at the top of the GUI keeps working until the user wins, loses
                          or ends the game.
    - win (self): calls function show_popup with a winning message.
    - loss (self): calls function show_popup with a losing message.
    - show_popup (self, message): creates a pop up with a label showing the message: "you won" or "you lost"
                                  and two buttons: restart and quit. These buttons call the functions with the same name.
    - restart (self, popup): destroys the config screen and starts a new game.
    - quit (self, popup): destroys the config screen.
    - create_button_grid (self, rows, cols): creates a grid of buttons based on the number of rows and columns that are
                                             selected in the config GUI.
    - on_left_click (self, row, col): reveals the tile on the board with the same coordinates (row/column) as the button.
                                      and calls the function update_button_grid.
    - on_right_click (self, row, col): flags the tile on the board with the same coordinates (row/column) as the button.
    - update_button_grid (self): iterates over the board and changes text on the buttons to match the state of the
                                 minesweeper board. This is done after every mouse click.

    LIMITATIONS:
        1. ???

        2. Buttons can change size during the game. This happens when the text within a button is changed. The buttons are
           always changed to the size of the largest text within a column.

    STRUCTURES:
    The structures used are elaborated on in the methods themselves.

    OUTPUT:
        GUI on which the minesweeper game can be played.
    """

    def __init__(self, rows, cols, mines, safe_radius, right_click=3):
        """
        self.title: gives the GUI a title
        self.resizable: to make sure that the user cannot change the size of the GUI
        self.board: minesweeper object
        self.rows: number of rows
        self.cols: number of columns
        self.buttons: list of lists with Nones. Has self.rows number of rows and self.columns number of columns
        self.OS: Operation system (Windows or Apple). Value is equal to the right_click variable and determined in the Config GUI.
        self.timer: a label that shows how long the user has been playing the game
        self.now: variable that ensures the timer restarts every new game
        self.ticking: Boolean variable, default = True. This variable is changed when a game is won, lost or quit.
                      This variable was added to make sure the timer stops when a game is finished.
        """

        tk.Tk.__init__(self)
        self.title('Minesweeper')
        self.resizable(False, False)  # Doesn't work with Mac? Some of the columns are outside the window.
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

        #label for picture of flag
        self.flag_lbl = tk.Label(self, text= '🚩', font=('Arial', 40))
        self.flag_lbl.grid(row=0, column=0)

        #label that shows number of flags
        self.n_flags_lbl = tk.Label(self, text=self.board.n_mines, font=('Arial', 30))
        self.n_flags_lbl.grid(row=0, column=1)

        self.create_button_grid(rows, cols)
        self.board.on_win += [self.win]
        self.board.on_loss += [self.loss]

    def update_n_flags(self):
        """
        DESCRIPTION:
        Function that updates the label on the GUI to show the number of flags that still need to be placed by the user
        to win the game.

        PARAMETERS:
        None.

        STRUCTURES:
        A for-loop that iterates over all the tiles on the minesweeper board to count the number of tiles that are flagged.
        An if-statement that reduces the count (= number of mines on board) when a tile is flagged.

        OUTPUT:
        A label that shows the number of flags that still need to be placed by the user to win the game.
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
        None.

        STRUCTURES:
        If-statement that checks if ticking is still True. If the game is won, lost or quit, ticking is set to False and
        the clock will stop.

        OUTPUT:
        Label that shows how long the user has been playing the game.
        """

        if self.ticking:
            self.now += 1
            now = '%02d : %02d' % (self.now//60, self.now%60)
            self.timer.configure(text=now)
            self.timer.after(1000, self.update_clock)

    def win(self):
        """
        DESCRIPTION:
        Function that sets ticking to False and calls the show_popup function with the message: "You won!"

        PARAMETERS:
        None

        STRUCTURES:
        None

        OUTPUT:
        A pop up GUI that tells the uses that he/she has won the game. The popup also contains two buttons; the user
        can choose to quit or restart the game.
        """

        self.ticking = False
        self.show_popup("You won!")

    def loss(self):
        """
        DESCRIPTION:
        Function that sets ticking to False and calls the show_popup function with the message: "You lost!"

        PARAMETERS:
        None

        STRUCTURES:
        None

        OUTPUT:
        A pop up GUI that tells the uses that he/she has lost the game. The popup also contains two buttons; the user
        can choose to quit or restart the game.
        """

        self.ticking = False
        self.show_popup("You lost!")

    def show_popup(self, message):
        """
        DESCRIPTION:
        A function that creates a pop up GUI in which the user receives a message that he/she has lost or won the game.
        The pop-up also has two buttons; exit and restart.
            The exit button calls the function quit.
            The restart button calls the function restart.

        PARAMETERS:
        message: a string variable that is defined in the function win or lost.

        STRUCTURES:
        None.

        OUTPUT:
        A pop up GUI that tells the user that he/she has won or lost the game. The user can click on one of two buttons;
        exit or restart.
        """

        popup = tk.Toplevel(self)
        popup.title("Game Over")
        popup.geometry("300x100")

        label = tk.Label(popup, text=message)
        label.pack(pady=10)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        exit_button = tk.Button(button_frame, text="Exit", command=lambda: self.quit(popup))
        exit_button.pack(side=tk.LEFT, padx=10)

        restart_button = tk.Button(button_frame, text="Restart", command=lambda: self.restart(popup))
        restart_button.pack(side=tk.RIGHT, padx=10)

    def restart(self, popup):
        """
        DESCRIPTION:
        A function that destroys the current config screen and restarts the game.

        PARAMETERS:
        popup: the pop-up that is shown to the user. It is needed by the function so it is able to destroy it.

        STRUCTURES:
        None

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
        popup: the pop-up that is shown to the user. It is needed by the function so it is able to destroy it.

        STRUCTURES:
        None.

        OUTPUT:
        None.
        """
        popup.destroy()
        self.destroy()

    def create_button_grid(self, rows, cols):
        """
        DESCRIPTION:
        A function that creates the grid of buttons based on the number of rows and columns that are
                                             selected in the config GUI.
        PARAMETERS:
        STRUCTURES:
        OUTPUT:
        """
        for r in range(rows):
            for c in range(cols):
                button = tk.Button(self, text=self.board.board[r][c].__repr__(), width=4, height=2)
                button.bind('<Button-1>', lambda event, row=r, col=c: self.on_left_click(row, col))
                button.bind('<Button-%d>' % self.OS, lambda event, row=r, col=c: self.on_right_click(row, col))
                button.grid(row=r + 1, column=c, padx=1, pady=1, sticky=tk.NSEW)
                self.buttons[r][c] = button

    def on_left_click(self, row, col):
        """
        DESCRIPTION:
        PARAMETERS:
        STRUCTURES:
        OUTPUT:
        """
        self.board.reveal(row, col)
        self.update_button_grid()

    def on_right_click(self, row, col):
        """
        DESCRIPTION:
        PARAMETERS:
        STRUCTURES:
        OUTPUT:
        """
        self.board.flag(row, col)
        self.update_button_grid()
        self.update_n_flags()

    def update_button_grid(self):
        """
        DESCRIPTION:
        PARAMETERS:
        STRUCTURES:
        OUTPUT:
        """

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text=self.board.board[r][c].__repr__())
                if self.board.board[r][c].__repr__() == '$':
                    self.buttons[r][c].grid_remove()
                if self.board.board[r][c].__repr__() in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    label = tk.Label(self, text=self.board.board[r][c].__repr__(), width=4, height=2, borderwidth=1)
                    label.grid(row=r + 1, column=c, padx=5, pady=5)
                    self.buttons[r][c].grid_remove()
                    self.buttons[r][c] = label
