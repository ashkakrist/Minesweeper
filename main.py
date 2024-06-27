"""
README:
Run this file to start the game.

ADDITIONAL PACKAGES:
config:     A module made to create a GUI that allows the user to choose
            game options
"""
from src.config import StartScreen


def main():
    app = StartScreen()
    app.mainloop()


if __name__ == '__main__':
    main()
