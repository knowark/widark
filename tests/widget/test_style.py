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
    assert style.template == '{}'
