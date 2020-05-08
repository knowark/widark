import curses
from pytest import fixture
from widark.widget import Widget


@fixture
def stdscr():
    stdscr = None

    def _init(screen):
        nonlocal stdscr
        stdscr = screen

    curses.wrapper(_init)
    return stdscr


def test_widget_instantiation_defaults():
    widget = Widget(None)
    assert isinstance(widget, Widget)
    assert widget.parent is None
    assert widget.children == []


def test_widget_window(stdscr):
    root = Widget(None)
    root.window = stdscr

    widget = Widget(root)

    relative_coordinates = widget.window.getparyx()
    dimensions = widget.window.getmaxyx()

    assert widget.window is not None
    assert relative_coordinates == (0, 0)
    assert dimensions == (1, 1)
