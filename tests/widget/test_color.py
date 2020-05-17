from enum import IntEnum
from widark.widget import Color


def test_color_definition():
    assert issubclass(Color, IntEnum)
