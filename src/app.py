"""GUI - maybe rename?
README MINESWEEPER GUI TKINTER
SUMMARY
    This code generates the graphical user interface of the minesweeper playfield.
DESCRIPTION
    App (class)
        __init__ (function) - Initialises the class. 
        win (function) - 
        loss (function) - 
        show_popup (function) - 
        restart (function) - 
        create_button_grid (function) - 
        on_left_click (function) - 
        on_right_click (function) - 
        update_button_grid (function) - 
PARAMETERS
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
LIMITATIONS
    1. Due to differences between windows and macOS, the code needs to be altered for a
    mac. In this code the following differences are:
        - Code for the event when clicking the buttons.
        - Graphical layout, screenwidth etc.
    2. 
    ...
STRUCTURES
    for loop (create_button_grid) - 
    for loop (update_button_grid) - 
OUTPUT
    button grid?     
"""
import tkinter as tk
import engine
import config as cfg


class App(tk.Tk):
    def __init__(self, width, height, rows, cols, mines, safe_radius, right_click=2):
        tk.Tk.__init__(self)
        self.title('Minesweeper')
        #self.geometry(f'{width}x{height}')
        self.resizable(False, False)  # Doesn't work with Mac? Some of the columns are outside the window.
        self.board = engine.MineSweeper(rows, cols, mines, safe_radius)
        self.rows = rows
        self.cols = cols
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.OS = right_click

        self.create_button_grid(rows, cols)
        self.board.on_win += [self.win]
        self.board.on_loss += [self.loss]

    def win(self):
        self.show_popup("You won!")

    def loss(self):
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
        grid_menu = tk.Frame(self)
        grid_menu.pack(padx=10, pady=10)

        res_but = tk.Button(grid_menu, text="Restart")
        res_but.pack()

        grid_frame = tk.Frame(self)
        grid_frame.pack(padx=10, pady=10)

        for r in range(rows):
            for c in range(cols):
                button = tk.Button(grid_frame, text=self.board.board[r][c].__repr__(), width=4, height=2)
                button.bind('<Button-1>', lambda event, row=r, col=c: self.on_left_click(row, col))
                button.bind('<Button-%d>' % self.OS, lambda event, row=r, col=c: self.on_right_click(row, col))
                button.grid(row=r, column=c, padx=1, pady=1, sticky=tk.NSEW)
                self.buttons[r][c] = button

    def on_left_click(self, row, col):
        self.board.reveal(row, col)
        self.update_button_grid()

    def on_right_click(self, row, col):
        self.board.flag(row, col)
        self.update_button_grid()

    def update_button_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text=self.board.board[r][c].__repr__())
                if self.board.board[r][c].__repr__() == '$':
                    self.buttons[r][c].grid_remove()
                if self.board.board[r][c].__repr__() in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    label = tk.Label(self, text=self.board.board[r][c].__repr__(), width=4, height=2, borderwidth=1)
                    label.grid(row=r, column=c, padx=5, pady=5)
                    self.buttons[r][c].grid_remove()
                    self.buttons[r][c] = label
