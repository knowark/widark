import curses
import asyncio
from pytest import mark
from widark.widget import Widget, Target, Style


pytestmark = mark.asyncio


def test_widget_instantiation_defaults():
    widget = Widget(None)
    assert isinstance(widget, Widget)
    assert isinstance(widget, Target)
    assert widget.parent is None
    assert widget.window is None
    assert widget.children == []
    assert widget.content == ''
    assert widget.position == 'relative'
    assert isinstance(widget.styling, Style)
    assert widget.focused is False
    assert widget.name == ''
    assert widget.group == ''
    assert widget.row.pos == 0
    assert widget.col.pos == 0
    assert widget.row.span == 1
    assert widget.col.span == 1
    assert widget.col.weight == 1
    assert widget.row.weight == 1


def test_widget_instantiation_arguments():
    widget = Widget(None, 'Custom Content', Style(border=[1]), 'fixed')
    assert isinstance(widget, Widget)
    assert widget.styling.border == [1]
    assert widget.content == 'Custom Content'
    assert widget.position == 'fixed'


def test_widget_root(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(child_a)
    child_c = Widget(child_b)

    assert root.root is root
    assert parent.root is root
    assert child_a.root is root
    assert child_b.root is root
    assert child_c.root is root


def test_widget_instantiation_arguments():
    widget = Widget(None, 'Custom Content', Style(border=[1]), 'fixed')
    assert isinstance(widget, Widget)
    assert widget.styling.border == [1]
    assert widget.content == 'Custom Content'
    assert widget.position == 'fixed'


def test_widget_attach(root):
    widget = Widget(root).attach(1, 2)

    relative_coordinates = widget.window.getparyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (1, 2)
    assert widget._y_min == 1
    assert widget._x_min == 2
    assert widget._y_max == 18
    assert widget._x_max == 90


def test_widget_move(root):
    widget = Widget(root).move().attach()

    widget = widget.move(5, 7)

    assert isinstance(widget, Widget)
    assert widget.window.getyx() == (5, 7)


def test_widget_clear(root):
    widget = Widget(root, 'SUPER').attach()

    window_text = widget.window.instr(0, 0, 5)
    assert window_text == b'SUPER'

    widget = widget.clear()
    curses.doupdate()

    window_text = widget.window.instr(0, 0, 5)
    assert isinstance(widget, Widget)
    assert window_text == b'     '


def test_widget_attach_error(root):
    root.window.resize(1, 1)

    widget = Widget(root)

    result = widget.attach(height=2, width=2)

    assert result is widget
    assert widget.window is None


def test_widget_attach_with_window(root):
    widget = Widget(None)
    widget.window = root.window
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


def test_widget_attach_fixed(root):
    sibling = Widget(root).grid(0, 0)
    parent = Widget(root).grid(0, 1)

    root.attach()

    assert sibling.window.getbegyx() == (0, 0)
    assert parent.window.getbegyx() == (0, 45)

    fixed_widget = Widget(parent, position='fixed')

    fixed_widget.attach(5, 5, 5, 30)

    assert fixed_widget.window is not None

    assert fixed_widget.parent is parent

    coordinates = fixed_widget.window.getbegyx()
    dimensions = fixed_widget.window.getmaxyx()

    assert fixed_widget in parent.children
    assert fixed_widget.window is not None
    assert coordinates == (5, 50)
    assert dimensions == (5, 30)


def test_widget_add(root):
    parent = Widget(root).grid(row=1, col=2)
    child = Widget(None)

    parent.add(child)
    parent.add(child)

    assert len(parent.children) == 1
    assert child in parent.children
    assert child.parent is parent


def test_widget_remove(root):
    parent = Widget(root).grid(row=1, col=2)
    parent.remove(root)

    child = Widget(parent)
    assert child in parent.children
    assert child.parent is parent

    parent.remove(child)

    assert len(parent.children) == 0
    assert child.parent is None


def test_widget_mark(root):
    widget = Widget(root).mark('first', 'combo')

    assert isinstance(widget, Widget)
    assert widget.name == 'first'
    assert widget.group == 'combo'


def test_widget_grid(root):
    widget = Widget(root).grid(row=1, col=2)

    assert isinstance(widget, Widget)
    assert widget.row.pos == 1
    assert widget.col.pos == 2


def test_widget_weight(root):
    widget = Widget(root).weight(row=3, col=2)

    assert isinstance(widget, Widget)
    assert widget.row.weight == 3
    assert widget.col.weight == 2


def test_widget_style(root):
    widget = Widget(root).style('SECONDARY', align='C')

    assert isinstance(widget, Widget)
    assert widget.styling.align == 'C'
    assert widget.styling.color == 'SECONDARY'


def test_widget_update(root):
    widget = Widget(root)
    assert widget.content == ''

    content = 'Hello World'
    widget = widget.attach().update(content)

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 11)

    assert widget.content == content
    assert window_text == b'Hello World'


def test_widget_update_error(root):
    root.window.resize(1, 1)

    widget = Widget(root)
    widget.content = 'Hello World'

    widget = widget.attach().update()

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 1)

    assert window_text == b'H'


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


def test_widget_attach_fixed_children(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent, position='fixed')
    child_c = Widget(parent)

    parent.attach()

    curses.doupdate()

    assert parent.window is not None
    assert child_a.window is not None
    assert child_b.window is None
    assert child_c.window is not None

    child_b.attach(5, 5, 10, 10)

    parent.attach()

    curses.doupdate()

    assert child_b.window is not None


async def test_widget_load(root):
    load_called = False

    class CustomWidget(Widget):
        async def load(self) -> None:
            nonlocal load_called
            load_called = True

    widget = CustomWidget(root)

    await widget.load()

    assert load_called is True


async def test_widget_connect(root):
    load_called = False

    class CustomWidget(Widget):
        async def load(self) -> None:
            nonlocal load_called
            load_called = True

    widget = CustomWidget(root)

    widget.connect()

    await asyncio.sleep(1/10)

    assert widget.window is not None
    assert load_called is True


def test_widget_place(root):
    # height, width = 18, 90
    assert Widget(root).attach().place() == (0, 0)
    assert Widget(root, 'ABC',  Style(align='C')).attach().place() == (8, 43)
    assert Widget(root, 'ABC', Style(align='R')).attach().place() == (17, 87)
    assert Widget(root, 'ABC', Style(align='CR')).attach().place() == (8, 87)
    assert Widget(
        root, 'ABC' * 40, Style(align='CC')).attach().place() == (8, 0)


def test_widget_layout_sequences(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent).grid(1, 2)
    child_c = Widget(parent).grid(3, 4)

    parent.attach()

    layout = parent.layout(parent.children)

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'y': 0, 'x': 0, 'height': 6, 'width': 30}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'y': 6, 'x': 30, 'height': 6, 'width': 30}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'y': 12, 'x': 60, 'height': 6, 'width': 30}


def test_widget_layout_without_window_or_children(root):
    parent = Widget(None)

    layout = parent.layout(parent.children)

    assert layout == []
    assert parent.window is None

    widget = Widget(root)

    layout = widget.layout(widget.children)

    assert layout == []
    assert widget.children == []


def test_widget_layout_span(root):
    parent = Widget(root)

    child_a = Widget(parent).span(2, 2)
    child_b = Widget(parent).grid(1, 2).span(2)
    child_c = Widget(parent).grid(3, 4).span(col=2)

    parent.attach()

    layout = parent.layout(parent.children)

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'y': 0, 'x': 0, 'height': 12, 'width': 60}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'y': 6, 'x': 30, 'height': 12, 'width': 30}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'y': 12, 'x': 60, 'height': 6, 'width': 30}


def test_widget_layout_weight(root):
    parent = Widget(root)

    child_a = Widget(parent).span(2, 2)
    child_b = Widget(parent).grid(1, 2).span(2).weight(col=2)
    child_c = Widget(parent).grid(3, 4).span(col=2).weight(2)

    parent.attach()

    layout = parent.layout(parent.children)

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'y': 0, 'x': 0, 'height': 9, 'width': 68}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'y': 5, 'x': 23, 'height': 13, 'width': 45}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'y': 10, 'x': 68, 'height': 8, 'width': 22}


def test_widget_layout_with_border(root):
    parent = Widget(root)
    parent.styling.border = [0]

    child_a = Widget(parent).span(2, 2)
    child_b = Widget(parent).grid(1, 2).span(2).weight(col=2)
    child_c = Widget(parent).grid(3, 4).span(col=2).weight(2)

    parent.attach()

    layout = parent.layout(parent.children)

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'y': 1, 'x': 1, 'height': 8, 'width': 66}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'y': 5, 'x': 23, 'height': 12, 'width': 44}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'y': 9, 'x': 67, 'height': 8, 'width': 22}


def test_widget_focus(root):
    parent = Widget(root).focus()
    assert isinstance(parent, Widget)

    child_a = Widget(parent).grid(0, 0)
    child_b = Widget(parent).grid(0, 1)
    assert isinstance(child_a, Widget)
    assert isinstance(child_b, Widget)

    parent.attach()

    child_a.focus()
    curses.doupdate()
    cursor_y, cursor_x = curses.getsyx()
    assert child_a.focused is True
    assert (cursor_y, cursor_x) == (0, 0)

    child_b.focus()
    curses.doupdate()
    cursor_y, cursor_x = curses.getsyx()
    assert child_b.focused is True
    assert (cursor_y, cursor_x) == (0, 45)


def test_widget_blur(root):
    widget = Widget(root).blur()

    assert isinstance(widget, Widget)
    assert widget.focused is False
