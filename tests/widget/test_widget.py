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
    # of 18 rows and 90 columns
    stdscr.resize(18, 90)
    root.window = stdscr
    return root


def test_widget_instantiation_defaults():
    widget = Widget(None)
    assert isinstance(widget, Widget)
    assert widget.parent is None
    assert widget.children == []
    assert widget.content == ''
    assert widget.row == 0
    assert widget.column == 0
    assert widget.width_weight == 1
    assert widget.height_weight == 1


def test_widget_attach(root):
    widget = Widget(root).attach(1, 2)

    relative_coordinates = widget.window.getparyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (1, 2)


def test_widget_attach_dimensions(root):
    widget = Widget(root).attach(height=3, width=2)

    relative_coordinates = widget.window.getparyx()
    dimensions = widget.window.getmaxyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (0, 0)
    assert dimensions == (3, 2)


def test_widget_position(root):
    widget = Widget(root).sequence(row=1, column=2)

    assert isinstance(widget, Widget)
    assert widget.row == 1
    assert widget.column == 2


def test_widget_weight(root):
    widget = Widget(root).weight(height=3, width=2)

    assert isinstance(widget, Widget)
    assert widget.height_weight == 3
    assert widget.width_weight == 2


def test_widget_update(root):
    widget = Widget(root)
    widget.content = 'Hello World'

    widget = widget.attach().update()

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 11)

    assert window_text == b'Hello World'


def test_widget_attach_children(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent)
    child_c = Widget(parent)

    parent.attach()

    curses.doupdate()

    assert parent.window is not None
    assert child_a.window is not None
    assert child_b.window is not None
    assert child_c.window is not None


def test_widget_layout_sequences(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent).sequence(1, 2)
    child_c = Widget(parent).sequence(3, 4)

    parent.attach()

    layout = parent.layout()

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'row': 0, 'column': 0, 'height': 6, 'width': 30}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'row': 6, 'column': 30, 'height': 6, 'width': 30}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'row': 12, 'column': 60, 'height': 6, 'width': 30}
