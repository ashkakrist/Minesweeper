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
        tk.TK -
        self -
        width -
        height -
        rows -
        cols -
        mines -
        safe_radius -
        message -
        popup -
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
        self.updateClock()

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
        count = self.board.n_mines
        for tile in self.board:
            if tile.flagged:
                count -= 1
        self.n_flags_lbl['text'] = count

    def update_clock(self):
        if self.ticking:
            self.now += 1
            now = '%02d : %02d' % (self.now//60, self.now%60)
            self.timer.configure(text=now)
            self.timer.after(1000, self.update_clock)

    def win(self):
        self.ticking = False
        self.show_popup("You won!")

    def loss(self):
        self.ticking = False
        self.show_popup("You lost!")

    def show_popup(self, message):
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
        popup.destroy()
        self.destroy()
        app = cfg.StartScreen()
        app.mainloop()

    def quit(self, popup):
        popup.destroy()
        self.destroy()

    def create_button_grid(self, rows, cols):
        # grid_menu = tk.Frame(self)
        # grid_menu.pack(padx=10, pady=10)
        #
        # res_but = tk.Button(grid_menu, text="Restart")
        # res_but.pack()
        #
        # grid_frame = tk.Frame(self)
        # grid_frame.pack(padx=10, pady=10)

        for r in range(rows):
            for c in range(cols):
                button = tk.Button(self, text=self.board.board[r][c].__repr__(), width=4, height=2)
                button.bind('<Button-1>', lambda event, row=r, col=c: self.on_left_click(row, col))
                button.bind('<Button-%d>' % self.OS, lambda event, row=r, col=c: self.on_right_click(row, col))
                button.grid(row=r + 1, column=c, padx=1, pady=1, sticky=tk.NSEW)
                self.buttons[r][c] = button

    def on_left_click(self, row, col):
        self.board.reveal(row, col)
        self.update_button_grid()

    def on_right_click(self, row, col):
        self.board.flag(row, col)
        self.update_button_grid()
        self.update_n_flags()

    def update_button_grid(self):
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
