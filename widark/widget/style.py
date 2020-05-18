import curses
from enum import IntEnum
from typing import List


class Style:
    def __init__(self, *args, **kwargs) -> None:
        self.configure(*args, **kwargs)

    def configure(self,
                  color: str = '',
                  background_color: str = '',
                  border_color: str = '',
                  border: List[int] = [],
                  align: str = '',
                  template: str = '') -> None:
        self.border: List[int] = border or getattr(self, 'border', [])
        self.color = color or getattr(self, 'color', 'DEFAULT')
        self.background_color = background_color or (
            getattr(self, 'background_color', 'DEFAULT'))
        self.border_color = border_color or (
            getattr(self, 'border_color', 'DEFAULT'))
        self.template = template or getattr(self, 'template', '{}')
        self.align = str.upper(align or getattr(self, 'align', 'LL'))


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
