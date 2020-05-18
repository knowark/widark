import curses
from enum import IntEnum
from widark.widget import Color, Style


def test_color_definition():
    assert issubclass(Color, IntEnum)


def test_style_instantiation_defaults(monkeypatch):
    style = Style()

    def mock_color_pair(value):
        return value

    monkeypatch.setattr(curses, "color_pair", mock_color_pair)

    assert style.color == Color.DEFAULT
    assert style.background_color == Color.DEFAULT
    assert style.align == 'LL'


def test_style_place(monkeypatch):
    height, width = 4, 12

    assert Style().place(height, width) == (0, 0)
    assert Style(align='C').place(height, width, 3) == (1, 4)
    assert Style(align='R').place(height, width, 3) == (3, 9)
    assert Style(align='CR').place(height, width, 3) == (1, 9)
    assert Style(align='LC').place(height, width, 3) == (0, 4)
    assert Style(align='CC').place(height, width, 24) == (1, 0)
