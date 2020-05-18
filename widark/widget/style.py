import curses
from math import ceil
from enum import IntEnum
from typing import List, Tuple


class Style:
    def __init__(self, color: str = 'DEFAULT',
                 background_color: str = 'DEFAULT',
                 border_color: str = 'DEFAULT',
                 border: List[int] = None,
                 align: str = 'LL') -> None:
        self.border: List[int] = border or []
        self.align = (align if all(char in 'LCR' for char in list(align))
                      and len(align) <= 2 else 'LL')
        self._color = Color[color]
        self._background_color = Color[background_color]
        self._border_color = Color[border_color]

    @property
    def color(self):
        return curses.color_pair(self._color)

    @property
    def background_color(self):
        return curses.color_pair(self._background_color)

    @property
    def border_color(self):
        return curses.color_pair(self._border_color)

    def place(self, height: int, width: int, fill: int = 0) -> Tuple[int, int]:
        y, x = 0, 0
        vertical, horizontal = (3 - len(self.align)) * self.align
        if vertical == 'C':
            y = int(max(height - ceil(fill / width), 0) / 2)
        elif vertical == 'R':
            y = max(height - ceil(fill / width), 0)

        if horizontal == 'C':
            x = int(max(width - fill, 0) / 2)
        elif horizontal == 'R':
            x = max(width - fill, 0)

        return y, x


class Color(IntEnum):
    DEFAULT = 0
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    WARNING = 5
    INFO = 6
    LIGHT = 7
    DARK = 8
