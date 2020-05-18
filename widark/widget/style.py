import curses
from enum import IntEnum
from typing import List


class Style:
    def __init__(self, color: str = 'DEFAULT',
                 background_color: str = 'DEFAULT',
                 border_color: str = 'DEFAULT',
                 border: List[int] = None) -> None:
        self._color = Color[color]
        self._background_color = Color[background_color]
        self._border_color = Color[border_color]
        self.border: List[int] = border or []

    @property
    def color(self):
        return curses.color_pair(self._color)

    @property
    def background_color(self):
        return curses.color_pair(self._background_color)

    @property
    def border_color(self):
        return curses.color_pair(self._border_color)


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
