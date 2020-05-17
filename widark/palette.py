import curses
from typing import List, Tuple
from .widget import Color


class Palette:
    def generate(self) -> List[Tuple[int, int, int]]:
        raise NotImplementedError('Please provide your own palette.')


class DefaultPalette(Palette):
    def generate(self) -> List[Tuple[int, int, int]]:
        return [
            (Color.PRIMARY, curses.COLOR_BLUE, curses.COLOR_BLACK),
            (Color.SECONDARY, curses.COLOR_MAGENTA, curses.COLOR_BLACK),
            (Color.SUCCESS, curses.COLOR_GREEN, curses.COLOR_BLACK),
            (Color.DANGER, curses.COLOR_RED, curses.COLOR_BLACK),
            (Color.WARNING, curses.COLOR_YELLOW, curses.COLOR_BLACK),
            (Color.INFO, curses.COLOR_CYAN, curses.COLOR_BLACK),
            (Color.LIGHT, curses.COLOR_WHITE, curses.COLOR_BLACK),
            (Color.DARK, curses.COLOR_BLACK, curses.COLOR_BLACK)
        ]
