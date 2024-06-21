"""GUI difficulty selection screen"""

import tkinter as tk
from src.app import App


class StartScreen(tk.Tk):
    """
    Initialise the start screen.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Minesweeper')
        self.geometry("300x200")
        self.resizable(False, False)
        self.WIDTH = 700
        self.HEIGHT = 700
        self.ROWS = tk.IntVar(value=15)
        self.COLUMNS = tk.IntVar(value=15)
        self.set_row_col()
        self.NUMBER_OF_MINES = int(self.ROWS.get()) * int(self.COLUMNS.get()) // 4
        self.SAFE_RADIUS = 2
        self.new_difficulty_level_window()
        self.OS = tk.IntVar()
        self.OS.set(3)
        self.choose_OS()


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
        app = App(self.WIDTH, self.HEIGHT, int(self.ROWS.get()), int(self.COLUMNS.get()), int(self.ROWS.get()) * int(self.COLUMNS.get()) // 6, 2, self.OS.get())
        self.destroy()
        app.mainloop()

    def normal(self):
        """
        Kill starting screen and create new minesweeper gui with settings that are medium difficult.
        (medium mine count, large safe radius).
        """
        app = App(self.WIDTH, self.HEIGHT, int(self.ROWS.get()), int(self.COLUMNS.get()), int(self.ROWS.get()) * int(self.COLUMNS.get()) // 4, 2, self.OS.get())
        self.destroy()
        app.mainloop()

    def hard(self):
        """
        Hardest mode
        (High mine count, small safe radius).
        """
        app = App(self.WIDTH, self.HEIGHT, int(self.ROWS.get()), int(self.COLUMNS.get()), int(self.ROWS.get()) * int(self.COLUMNS.get()) // 3, 1, self.OS.get())
        self.destroy()
        app.mainloop()

    def set_row_col(self):
        entry_frame = tk.Frame(self)
        entry_frame.pack()
        lab_col = tk.Label(entry_frame, text="Number of columns:")
        lab_col.grid(row=0, column=1)
        var_col = tk.Entry(entry_frame, width=5)
        var_col['textvariable'] = self.COLUMNS
        self.COLUMNS = var_col
        var_col.grid(row=0, column=2)

        lab_row = tk.Label(entry_frame, text="Number of rows:")
        lab_row.grid(row=1, column=1)
        var_row = tk.Entry(entry_frame, width=5)
        var_row['textvariable'] = self.ROWS
        var_row.grid(row=1, column=2)

    def get_value(self, entry):
        ent_val = int(entry.get())

    def choose_OS(self):
        """
        Selecting operator, standard on windows.
        """
        label = tk.Label(self, text="Select operating system:")
        label.pack()

        rad_wind = tk.Radiobutton(self, text="Windows", variable=self.OS, value=3)
        rad_wind.pack(padx=20, side=tk.LEFT)

        rad_mac = tk.Radiobutton(self, text="MacOS", variable=self.OS, value=2)
        rad_mac.pack(padx=20, side=tk.RIGHT)
