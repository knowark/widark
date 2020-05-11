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


def test_widget_instantiation_defaults():
    widget = Widget(None)
    assert isinstance(widget, Widget)
    assert widget.parent is None
    assert widget.children == []
    assert widget.border == []
    assert widget.content == ''
    assert widget.row == 0
    assert widget.col == 0
    assert widget.row_span == 1
    assert widget.col_span == 1
    assert widget.col_weight == 1
    assert widget.row_weight == 1


def test_widget_instantiation_arguments():
    widget = Widget(None, 'Custom Content', [0])
    assert isinstance(widget, Widget)
    assert widget.border == [0]
    assert widget.content == 'Custom Content'


def test_widget_attach(root):
    widget = Widget(root).attach(1, 2)

    relative_coordinates = widget.window.getparyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (1, 2)


def test_widget_attach_with_window(stdscr):
    widget = Widget(None)
    widget.window = stdscr
    widget.content = 'Hello World'
    widget.attach(1, 2)

    window_text = widget.window.instr(0, 0, 11)

    assert isinstance(widget, Widget)
    assert widget.window is not None

    assert window_text == b'Hello World'


def test_widget_attach_dimensions(root):
    widget = Widget(root).attach(height=3, width=2)

    relative_coordinates = widget.window.getparyx()
    dimensions = widget.window.getmaxyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (0, 0)
    assert dimensions == (3, 2)


def test_widget_position(root):
    widget = Widget(root).grid(row=1, col=2)

    assert isinstance(widget, Widget)
    assert widget.row == 1
    assert widget.col == 2


def test_widget_weight(root):
    widget = Widget(root).weight(row=3, col=2)

    assert isinstance(widget, Widget)
    assert widget.row_weight == 3
    assert widget.col_weight == 2


def test_widget_update(root):
    widget = Widget(root)
    widget.content = 'Hello World'

    widget = widget.attach().update()

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 11)

    assert window_text == b'Hello World'


def test_widget_update_without_window(root):
    widget = Widget(root)
    widget.content = 'Hello World'

    widget = widget.update()

    curses.doupdate()

    assert isinstance(widget, Widget)
    assert widget.window is None


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
    child_b = Widget(parent).grid(1, 2)
    child_c = Widget(parent).grid(3, 4)

    parent.attach()

    layout = parent.layout()

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'row': 0, 'col': 0, 'height': 6, 'width': 30}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'row': 6, 'col': 30, 'height': 6, 'width': 30}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'row': 12, 'col': 60, 'height': 6, 'width': 30}


def test_widget_layout_without_window_or_children(root):
    parent = Widget(None)

    layout = parent.layout()

    assert layout == []
    assert parent.window is None

    widget = Widget(root)

    layout = widget.layout()

    assert layout == []
    assert widget.children == []


def test_widget_layout_span(root):
    parent = Widget(root)

    child_a = Widget(parent).span(2, 2)
    child_b = Widget(parent).grid(1, 2).span(2)
    child_c = Widget(parent).grid(3, 4).span(col=2)

    parent.attach()

    layout = parent.layout()

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'row': 0, 'col': 0, 'height': 12, 'width': 60}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'row': 6, 'col': 30, 'height': 12, 'width': 30}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'row': 12, 'col': 60, 'height': 6, 'width': 30}


def test_widget_layout_weight(root):
    parent = Widget(root)

    child_a = Widget(parent).span(2, 2)
    child_b = Widget(parent).grid(1, 2).span(2).weight(col=2)
    child_c = Widget(parent).grid(3, 4).span(col=2).weight(2)

    parent.attach()

    layout = parent.layout()

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'row': 0, 'col': 0, 'height': 9, 'width': 68}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'row': 5, 'col': 23, 'height': 13, 'width': 45}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'row': 9, 'col': 68, 'height': 9, 'width': 22}


def test_widget_layout_with_border(root):
    parent = Widget(root)
    parent.border = [0]

    child_a = Widget(parent).span(2, 2)
    child_b = Widget(parent).grid(1, 2).span(2).weight(col=2)
    child_c = Widget(parent).grid(3, 4).span(col=2).weight(2)

    parent.attach()

    layout = parent.layout()

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'row': 1, 'col': 1, 'height': 8, 'width': 66}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'row': 5, 'col': 23, 'height': 12, 'width': 44}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'row': 9, 'col': 67, 'height': 8, 'width': 22}
