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
        self.geometry("300x225")
        self.resizable(False, False)
        self.WIDTH = 700
        self.HEIGHT = 700
        self.ROWS = tk.IntVar()
        self.COLUMNS = tk.IntVar()

        self.OS = tk.IntVar(value=3)
        self.OS.set(3)
        self.choose_OS()

        self.playfield = tk.IntVar(value=13)
        self.set_playfield()
        self.set_row_col()

        self.NUMBER_OF_MINES = int(self.ROWS.get()) * int(self.COLUMNS.get()) // 4
        self.SAFE_RADIUS = 2
        self.new_difficulty_level_window()


    def choose_OS(self):
        """
        Selecting operator, standard on windows.
        """
        OS_frame = tk.Frame(self)
        OS_frame.pack(pady=20)

        label = tk.Label(OS_frame, text="Select operating system:")
        label.pack()

        rad_wind = tk.Radiobutton(OS_frame, text="Windows", variable=self.OS, value=3)
        rad_wind.pack(padx=20, side=tk.LEFT)

        rad_mac = tk.Radiobutton(OS_frame, text="MacOS", variable=self.OS, value=2)
        rad_mac.pack(padx=20, side=tk.RIGHT)


    def set_playfield(self):
        """
        Selecting small(10x10), medium(15x15) or large(20x20) playingfield.
        """
        play_frame = tk.Frame(self)
        play_frame.pack()

        label = tk.Label(play_frame, text="Select playingfield:")
        label.grid(row=0, column=0, columnspan=3)

        rad_wind = tk.Radiobutton(play_frame, text="Small", variable=self.playfield, value=10)
        rad_wind.grid(row=1, column=0)

        rad_mac = tk.Radiobutton(play_frame, text="Medium", variable=self.playfield, value=13)
        rad_mac.grid(row=1, column=1)

        rad_mac = tk.Radiobutton(play_frame, text="Large", variable=self.playfield, value=16)
        rad_mac.grid(row=1, column=2)


    def set_row_col(self):
        self.ROWS = self.playfield
        self.COLUMNS = self.playfield

    def new_difficulty_level_window(self):
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        label = tk.Label(button_frame, text="Select difficulty level:")
        label.grid(row=0, column=0, columnspan=3)

        easy_button = tk.Button(button_frame, text="Easy", command=self.easy)
        easy_button.grid(row=1, column=0)

        normal_button = tk.Button(button_frame, text="Normal", command=self.normal)
        normal_button.grid(row=1, column=1)

        hard_button = tk.Button(button_frame, text="Hard", command=self.hard)
        hard_button.grid(row=1, column=2)


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
