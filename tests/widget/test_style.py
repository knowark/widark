import curses
from enum import IntEnum
from widark.widget import Color, Style, Attribute


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
    result = Color.DEFAULT.bold()
    assert result == curses.A_BOLD
    result = Color.DEFAULT.blink()
    assert result == curses.A_BLINK


def test_attribute_call():
    assert Attribute().join('REVERSE') == curses.A_REVERSE
    assert Attribute('BOLD').join() == curses.A_BOLD
    assert Attribute('BOLD').join('REVERSE') == (
        curses.A_BOLD | curses.A_REVERSE)
    assert Attribute(['BOLD', 'BLINK']).join('REVERSE') == (
        curses.A_BOLD | curses.A_BLINK | curses.A_REVERSE)
    assert Attribute(['BOLD', 'BLINK']).join(['REVERSE', 'DIM']) == (
        curses.A_BOLD | curses.A_BLINK | curses.A_REVERSE | curses.A_DIM)
