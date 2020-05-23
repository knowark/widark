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

    assert style.color == 0
    assert style.background_color == 0
    assert style.align == 'LL'
    assert style.template == '{}'


def test_color_enum_call(monkeypatch):
    color_pair_called = False

    def mock_color_pair(value) -> None:
        nonlocal color_pair_called
        color_pair_called = True
        return value

    monkeypatch.setattr(curses, "color_pair", mock_color_pair)

    result = Color.DEFAULT()

    assert color_pair_called is True
    assert result == Color.DEFAULT

    result = Color.DEFAULT.reverse()

    assert result == curses.A_REVERSE
