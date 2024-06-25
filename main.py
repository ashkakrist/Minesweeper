"""
Run this file to start the game.
"""
import os

from src.config import StartScreen


def main():
    app = StartScreen()
    app.mainloop()


if __name__ == '__main__':
    print(os.getcwd())
    main()
