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

    yield stdscr

    curses.endwin()


@fixture
def root(stdscr):
    root = Widget(None)
    # Run all tests with a resolution
    # of 18 rows and 90 cols
    stdscr.resize(18, 90)
    root.window = stdscr
    return root
