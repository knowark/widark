import curses
from pytest import fixture
from widark.widget import Widget


@fixture
def stdscr():
    stdscr = curses.initscr()

    yield stdscr

    try:
        curses.endwin()
    except curses.error:
        pass


@fixture
def root(stdscr):
    root = Widget(None)
    # Run all tests with a resolution
    # of 18 rows and 90 cols
    stdscr.resize(18, 90)
    root.window = stdscr
    return root
