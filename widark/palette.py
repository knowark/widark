import curses
from typing import List, Tuple
from .widget import Color


class Palette:
    REVERSE = curses.A_REVERSE

    def generate(self) -> List[Tuple[int, int, int]]:
        raise NotImplementedError('Please provide your own palette.')


class DefaultPalette(Palette):
    # https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    def generate(self) -> List[Tuple[int, int, int]]:
        return [
            (Color.PRIMARY, 12, -1),
            (Color.SECONDARY, 8, -1),
            (Color.SUCCESS, 10, -1),
            (Color.DANGER, 9, -1),
            (Color.WARNING, 11, -1),
            (Color.INFO, 14, -1),
            (Color.LIGHT, 15, -1),
            (Color.DARK, 8, -1)
        ]
