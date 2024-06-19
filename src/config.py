"""GUI difficulty selection screen"""

import tkinter as tk
from app import App


class StartScreen(tk.Tk):
    """
    Initialise the start screen.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Minesweeper')
        self.geometry("300x100")
        self.resizable(False, False)
        self.WIDTH = 700
        self.HEIGHT = 700
        self.ROWS = 15
        self.COLUMNS = 15
        self.NUMBER_OF_MINES = self.ROWS * self.COLUMNS // 4
        self.SAFE_RADIUS = 2
        self.new_difficulty_level_window()

    def new_difficulty_level_window(self):
        label = tk.Label(self, text="Select difficulty level:")
        label.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        easy_button = tk.Button(button_frame, text="Easy", command=self.easy)
        easy_button.pack(side=tk.LEFT, padx=10)

        normal_button = tk.Button(button_frame, text="Normal", command=self.normal)
        normal_button.pack(side=tk.LEFT, padx=10)

        hard_button = tk.Button(button_frame, text="Hard", command=self.hard)
        hard_button.pack(side=tk.RIGHT, padx=10)

    def easy(self):
        """
        Kill starting screen and create new minesweeper gui with settings that are easy
        (low mine count, large safe radius).
        """
        app = App(self.WIDTH, self.HEIGHT, self.ROWS, self.COLUMNS, self.ROWS * self.COLUMNS // 6, 2)
        self.destroy()
        app.mainloop()

    def normal(self):
        """
        Kill starting screen and create new minesweeper gui with settings that are medium difficult.
        (medium mine count, large safe radius).
        """
        app = App(self.WIDTH, self.HEIGHT, self.ROWS, self.COLUMNS, self.ROWS * self.COLUMNS // 4, 2)
        self.destroy()
        app.mainloop()

    def hard(self):
        """
        Hardest mode
        (High mine count, small safe radius).
        """
        app = App(self.WIDTH, self.HEIGHT, self.ROWS, self.COLUMNS, self.ROWS * self.COLUMNS // 3, 1)
        self.destroy()
        app.mainloop()
