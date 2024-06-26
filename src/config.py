"""
README:
This script creates a graphical user interface for the game setup starting
screen:

It contains ONE class which generates a pop-up at the start of the game, that
allows the player to adjust the OS version, the size of the playing field,
and the difficulty of the game. The settings are used for the final creation
of the board.

ADDITIONAL PACKAGES:
tkinter:    A python library used to create the GUI.
winsound:   A built in module on Windows that can be used to play sounds.
app:        A module made to create the GUI for the minesweeper game.
"""

import tkinter as tk
from src.app import App


###########################################
############### StartScreen ###############
###########################################
class StartScreen(tk.Tk):
    """
    DESCRIPTION:
    The StartScreen creates the popup at the start of the game in which
    the player can adjust the OS version, the size of the playing field, and
    the difficulty of the game.

    PARAMETERS:
    The class does not have parameters.

    METHODS:
    __init__ (self);
    choose_OS (function);
    set_playing field (function);
    set_row_col (function);
    new_difficulty_level_window (function);
    easy (function);
    normal (function);
    hard (function);

    LIMITATIONS:
    1.  Other OS are not represented. We do not know how the GUI looks in other
        OS than MacOS and Windows.
    2.  The selection of the OS has to be done manually and is not automatically
        detected.
    3.  The selection of the difficulty has to be done after every game. The
        settings are not saved.

    STRUCTURES:
    The structures used are elaborated on in the docstring of the methods
    themselves where applicable.

    OUTPUT:
    A window in which the user can choose the preferred OS version, the size of
    the playing field, and the difficulty of the game. The window is closed when
    the player has made her/his selection.
    """

    def __init__(self):
        """
        DESCRIPTION:
        This method initialises the class attributes.
        self.title, self.geometry, and self.resizable are tkinter options that
        are set to our liking.

        self.ROWS and self.COLUMNS are the attributes that contains the size of
        the board.

        self.OS contains the value for the OS version. This value is added to
        account for the fact that macOS and windows have different right mouse
        buttons.

        STRUCTURES:
        If-statement:   Used to import the package "winsound" if the Windows OS
                        is selected by the user.
        """

        tk.Tk.__init__(self)
        self.title('Minesweeper')
        self.geometry("300x225")
        self.resizable(False, False)
        self.ROWS = tk.IntVar()
        self.COLUMNS = tk.IntVar()

        self.OS = tk.IntVar(value=3)
        self.choose_OS()
        if self.OS == 3:
            import winsound

        self.playfield = tk.IntVar(value=13)
        self.set_playfield()
        self.set_row_col()

        self.new_difficulty_level_window()

    def choose_OS(self):
        """
        DESCRIPTION:
        Makes radio buttons which allow the player to choose between a macOS or
        Windows version. The function changes the self.OS attribute of the class.

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

        OS_frame = tk.Frame(self)
        OS_frame.pack(pady=20)

        label = tk.Label(OS_frame,
                         text="Select operating system:")
        label.pack()

        rad_wind = tk.Radiobutton(OS_frame,
                                  text="Windows", variable=self.OS, value=3)
        rad_wind.pack(padx=20, side=tk.LEFT)

        rad_mac = tk.Radiobutton(OS_frame,
                                 text="MacOS", variable=self.OS, value=2)
        rad_mac.pack(padx=20, side=tk.RIGHT)

    def set_playfield(self):
        """
        DESCRIPTION:
        Makes radio buttons which allow the player to choose the size of the
        playing field (small(10x10)/medium(13x13)/large(16x16)). The selection
        changes the attributes of the class.

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

        play_frame = tk.Frame(self)
        play_frame.pack()

        label = tk.Label(play_frame, text="Select playingfield:")
        label.grid(row=0, column=0, columnspan=3)

        rad_wind = tk.Radiobutton(play_frame,
                                  text="Small",
                                  variable=self.playfield,
                                  value=10)
        rad_wind.grid(row=1, column=0)

        rad_mac = tk.Radiobutton(play_frame,
                                 text="Medium",
                                 variable=self.playfield,
                                 value=13)
        rad_mac.grid(row=1, column=1)

        rad_mac = tk.Radiobutton(play_frame,
                                 text="Large",
                                 variable=self.playfield,
                                 value=16)
        rad_mac.grid(row=1, column=2)

    def set_row_col(self):
        """
        DESCRIPTION:
        Changes the ROWS and COLUMNS attribute of the class, based on the
        selection the player made for the size of the playing field with the
        radio buttons generated by the set_playing field function.

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

        self.ROWS = self.playfield
        self.COLUMNS = self.playfield

    def new_difficulty_level_window(self):
        """
        DESCRIPTION:
        Creates the buttons with which the player can set the difficulty for
        the game (easy/normal/hard). Clicking the button initialises the
        creation of the board based on the settings the player selected. Either
        the function easy, normal or hard is called.

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

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
        DESCRIPTION:
        Initialised when the player presses the easy button generated in the
        new_difficulty_level_window function. The starting screen is killed and
        a new minesweeper GUI is generated on easy settings (low mine count,
        large safe radius).

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

        app = App(int(self.ROWS.get()),
                  int(self.COLUMNS.get()),
                  int(self.ROWS.get()) * int(self.COLUMNS.get()) // 6,
                  2,
                  self.OS.get())
        self.destroy()
        app.mainloop()

    def normal(self):
        """
        DESCRIPTION:
        Initialised when the player presses the normal button generated in the
        new_difficulty_level_window function. The starting screen is killed and
        a new minesweeper GUI is generated on normal settings (medium mine
        count, large safe radius).

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

        app = App(int(self.ROWS.get()),
                  int(self.COLUMNS.get()),
                  int(self.ROWS.get()) * int(self.COLUMNS.get()) // 4,
                  2,
                  self.OS.get())
        self.destroy()
        app.mainloop()

    def hard(self):
        """
        DESCRIPTION:
        Initialised when the player presses the hard button generated in the
        new_difficulty_level_window function. The starting screen is killed and
        a new minesweeper GUI is generated on hard settings (high mine count,
        small safe radius).

        PARAMETERS:
        No additional parameters aside from the StartScreen attributes itself.
        """

        app = App(int(self.ROWS.get()),
                  int(self.COLUMNS.get()),
                  int(self.ROWS.get()) * int(self.COLUMNS.get()) // 2,
                  1, self.OS.get())
        self.destroy()
        app.mainloop()
