from typing import List, Tuple
from .widget import Color


class Palette:
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
            (Color.DARK, 0, -1),
            (Color.BACK_PRIMARY, 15, 12),
            (Color.BACK_SECONDARY, 15, 8),
            (Color.BACK_SUCCESS, 15, 10),
            (Color.BACK_DANGER, 15, 9),
            (Color.BACK_WARNING, 15, 11),
            (Color.BACK_INFO, 15, 14),
            (Color.BACK_LIGHT, 15, 15),
            (Color.BACK_DARK, 15, 0)
        ]
