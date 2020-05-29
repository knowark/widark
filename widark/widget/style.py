import curses
from enum import IntEnum
from typing import List, Union


class Style:
    def __init__(self, *args, **kwargs) -> None:
        self.configure(*args, **kwargs)

    def configure(self,
                  color: int = None,
                  background_color: int = None,
                  border_color: int = None,
                  border: List[int] = None,
                  align: str = '',
                  template: str = '') -> None:
        self.border: List[int] = (
            getattr(self, 'border', []) if border is None else border)
        self.color = getattr(self, 'color', 0) if color is None else color
        self.background_color = (
            getattr(self, 'background_color', 0)
            if background_color is None else background_color)
        self.border_color = (
            getattr(self, 'border_color', 0)
            if border_color is None else border_color)
        self.align = str.upper(align or getattr(self, 'align', 'LL'))
        self.template = template or getattr(self, 'template', '{}')


class Attribute:
    def __init__(self, attributes: Union[List[str], str] = None) -> None:
        if isinstance(attributes, str):
            attributes = [attributes]
        self.attributes = attributes or []

    def join(self, attributes: Union[List[str], str] = None) -> int:
        attributes = attributes or []
        if isinstance(attributes, str):
            attributes = [attributes]
        attributes = self.attributes + attributes

        result = 0
        for value in [getattr(curses, f'A_{item}') for item in attributes]:
            result |= value

        return result


class ColorEnum(IntEnum):
    def __call__(self) -> int:
        return curses.color_pair(self.value)

    def reverse(self) -> int:
        return curses.color_pair(self.value) | curses.A_REVERSE

    def bold(self) -> int:
        return curses.color_pair(self.value) | curses.A_BOLD

    def blink(self) -> int:
        return curses.color_pair(self.value) | curses.A_BLINK


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
    BACK_PRIMARY = 9
    BACK_SECONDARY = 10
    BACK_SUCCESS = 11
    BACK_DANGER = 12
    BACK_WARNING = 13
    BACK_INFO = 14
    BACK_LIGHT = 15
    BACK_DARK = 16
