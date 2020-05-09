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
    root.window = stdscr
    return root


def test_widget_instantiation_defaults():
    widget = Widget(None)
    assert isinstance(widget, Widget)
    assert widget.parent is None
    assert widget.children == []
    assert widget.content == ''
    assert widget.row_sequence == 0
    assert widget.column_sequence == 0
    assert widget.row_weight == 1
    assert widget.column_weight == 1


def test_widget_attach(root):
    widget = Widget(root).attach(1, 2)

    relative_coordinates = widget.window.getparyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (1, 2)


def test_widget_attach_dimensions(root):
    widget = Widget(root).attach(width=2, height=3)

    relative_coordinates = widget.window.getparyx()
    dimensions = widget.window.getmaxyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (0, 0)
    assert dimensions == (2, 3)


def test_widget_position(root):
    widget = Widget(root).sequence(row=1, column=2)

    assert isinstance(widget, Widget)
    assert widget.row_sequence == 1
    assert widget.column_sequence == 2


def test_widget_weight(root):
    widget = Widget(root).weight(row=2, column=3)

    assert isinstance(widget, Widget)
    assert widget.row_weight == 2
    assert widget.column_weight == 3


def test_widget_update(root):
    widget = Widget(root)
    widget.content = 'Hello World'

    widget = widget.attach().update()

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 11)

    assert window_text == b'Hello World'
