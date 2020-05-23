import curses
from enum import IntEnum
from typing import List


class Style:
    def __init__(self, *args, **kwargs) -> None:
        self.configure(*args, **kwargs)

    def configure(self,
                  color: int = 0,
                  background_color: int = 0,
                  border_color: int = 0,
                  border: List[int] = [],
                  align: str = '',
                  template: str = '') -> None:
        self.border: List[int] = border or getattr(self, 'border', [])
        self.color = color or getattr(self, 'color', 0)
        self.background_color = background_color or (
            getattr(self, 'background_color', 0))
        self.border_color = border_color or (
            getattr(self, 'border_color', 0))
        self.align = str.upper(align or getattr(self, 'align', 'LL'))
        self.template = template or getattr(self, 'template', '{}')


class ColorEnum(IntEnum):
    def __call__(self) -> int:
        return curses.color_pair(self.value)

    def reverse(self) -> int:
        return curses.color_pair(self.value) | curses.A_REVERSE


class Color(ColorEnum):
    DEFAULT = 0
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    WARNING = 5
    INFO = 6
    LIGHT = 7
    DARK = 8
