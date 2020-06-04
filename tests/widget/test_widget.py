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
    assert widget.autoload is True
    assert widget.autobuild is True
    assert isinstance(widget.styling, Style)
    assert widget.name == ''
    assert widget.group == ''
    assert widget.row.pos == 0
    assert widget.col.pos == 0
    assert widget.row.span == 1
    assert widget.col.span == 1
    assert widget.col.weight == 1
    assert widget.row.weight == 1
    assert widget.mode == 'loose'
    assert widget.proportion == {'height': 0, 'width': 0}
    assert widget.align == ''
    assert widget.margin == {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}


def test_widget_instantiation_arguments():
    widget = Widget(None, content='Custom Content',
                    style=Style(border=[1]), position='fixed')
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


def test_widget_render(root):
    widget = Widget(root).pin(1, 2).render()

    relative_coordinates = widget.window.getparyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (1, 2)
    assert widget._y_min == 1
    assert widget._x_min == 2
    assert widget._y_max == 18
    assert widget._x_max == 90


def test_widget_render(root):

    class CustomWidget(Widget):
        def build(self) -> None:
            Widget(self)
            Widget(self)

    widget = CustomWidget(root)
    assert len(widget.children) == 2

    widget = CustomWidget(root, autobuild=False)
    assert len(widget.children) == 0


async def test_widget_gather(root):
    parent_called = False
    child_called = False

    class ChildWidget(Widget):
        async def load(self) -> None:
            nonlocal child_called
            child_called = True

    class ParentWidget(Widget):
        def build(self) -> None:
            ChildWidget(self)

        async def load(self) -> None:
            nonlocal parent_called
            parent_called = True

    widget = ParentWidget(root)
    widget.gather()

    await asyncio.sleep(1/15)

    assert len(widget.children) == 1
    assert parent_called is True
    assert child_called is True


async def test_widget_gather_autoload_false(root):
    parent_called = False
    child_called = False

    class ChildWidget(Widget):
        async def load(self) -> None:
            nonlocal child_called
            child_called = True

    class ParentWidget(Widget):
        def build(self) -> None:
            ChildWidget(self)

        async def load(self) -> None:
            nonlocal parent_called
            parent_called = True

    widget = ParentWidget(root, autoload=False)
    widget.gather()

    await asyncio.sleep(1/15)

    assert len(widget.children) == 1
    assert parent_called is False
    assert child_called is False


def test_widget_move(root):
    widget = Widget(root).move().render()

    widget = widget.move(5, 7)

    assert isinstance(widget, Widget)
    assert widget.window.getyx() == (5, 7)


def test_widget_size(root):
    widget = Widget(root)
    assert widget.size() == (0, 0)
    widget.render()
    assert widget.size() == (18, 90)


def test_widget_clear(root):
    widget = Widget(root, content='SUPER').render()

    window_text = widget.window.instr(0, 0, 5)
    assert window_text == b'SUPER'

    widget = widget.clear()
    curses.doupdate()

    window_text = widget.window.instr(0, 0, 5)
    assert isinstance(widget, Widget)
    assert window_text == b'     '


def test_widget_render_resize_error(root):
    root.window.resize(1, 1)

    widget = Widget(root)

    result = widget.pin(height=2, width=2).render()

    assert result is widget
    assert widget.window is None


def test_widget_render_with_window(root):
    widget = Widget(None)
    widget.window = root.window
    widget.content = 'Hello World'
    widget.pin(1, 2).render()

    window_text = widget.window.instr(0, 0, 11)

    assert isinstance(widget, Widget)
    assert widget.window is not None

    assert window_text == b'Hello World'


def test_widget_render_dimensions(root):
    widget = Widget(root).pin(height=3, width=2).render()

    relative_coordinates = widget.window.getparyx()
    dimensions = widget.window.getmaxyx()

    assert widget in root.children
    assert widget.window is not None
    assert relative_coordinates == (0, 0)
    assert dimensions == (3, 2)


def test_widget_render_fixed(root):
    sibling = Widget(root).grid(0, 0)
    parent = Widget(root).grid(0, 1)

    root.render()

    assert sibling.window.getbegyx() == (0, 0)
    assert parent.window.getbegyx() == (0, 45)

    fixed_widget = Widget(parent, position='fixed')

    fixed_widget.pin(5, 5, 5, 30).render()

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

    result = parent.add(None)
    assert result is parent


def test_widget_remove(root):
    parent = Widget(root).grid(row=1, col=2)
    parent.remove(root)

    child = Widget(parent)
    assert child in parent.children
    assert child.parent is parent

    parent.remove(child)

    assert len(parent.children) == 0
    assert child.parent is None

    result = parent.remove(None)
    assert result is parent


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


def test_widget_render_content(root):
    widget = Widget(root)
    assert widget.content == ''

    content = 'Hello World'
    widget.content = content
    widget = widget.render()

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 11)

    assert widget.content == content
    assert window_text == b'Hello World'


def test_widget_render_error(root):
    root.window.resize(1, 1)

    widget = Widget(root)
    widget.content = 'Hello World'

    widget = widget.render()

    curses.doupdate()

    window_text = widget.window.instr(0, 0, 1)

    assert window_text == b'H'


def test_widget_update_without_window(root):
    root.window.resize(1, 1)
    widget = Widget(root)
    widget.content = 'Hello World'
    root.window = None

    widget = widget.render()

    curses.doupdate()

    assert isinstance(widget, Widget)
    assert widget.window is None


def test_widget_render_children(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent)
    child_c = Widget(parent)

    parent.render()

    curses.doupdate()

    assert parent.window is not None
    assert child_a.window is not None
    assert child_b.window is not None
    assert child_c.window is not None


def test_widget_render_fixed_children(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent, position='fixed')
    child_c = Widget(parent)

    parent.render()

    curses.doupdate()

    assert parent.window is not None
    assert child_a.window is not None
    assert child_b.window is None
    assert child_c.window is not None

    child_b.pin(5, 5, 10, 10).render()

    parent.render()

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

    widget = CustomWidget(root, autoload=True)

    widget.connect()

    await asyncio.sleep(1/10)

    assert widget.window is not None
    assert load_called is True


def test_widget_place(root):
    # height, width = 18, 90
    assert Widget(root).render().place() == (0, 0)
    assert Widget(root, content='ABC',  style=Style(
        align='C')).render().place() == (8, 43)
    assert Widget(root, content='ABC', style=Style(
        align='R')).render().place() == (17, 87)
    assert Widget(root, content='ABC', style=Style(
        align='CR')).render().place() == (8, 87)
    assert Widget(root, content='ABC' * 40, style=Style(
        align='CC')).render().place() == (8, 0)


def test_widget_layout_sequences(root):
    parent = Widget(root)

    child_a = Widget(parent)
    child_b = Widget(parent).grid(1, 2)
    child_c = Widget(parent).grid(3, 4)

    parent.render()

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

    parent.render()

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

    parent.render()

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

    parent.render()

    layout = parent.layout(parent.children)

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'y': 1, 'x': 1, 'height': 8, 'width': 66}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'y': 5, 'x': 23, 'height': 12, 'width': 44}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'y': 9, 'x': 67, 'height': 8, 'width': 22}


def test_widget_layout_mode(root):
    parent = Widget(root, mode='compact')

    child_a = Widget(parent)
    child_b = Widget(parent).grid(1)
    child_c = Widget(parent).grid(2)
    child_d = Widget(parent).grid(3)

    parent.render()

    layout = parent.layout(parent.children)

    assert isinstance(layout, list)
    assert layout[0][0] == child_a
    assert layout[0][1] == {'y': 0, 'x': 0, 'height': 4, 'width': 90}
    assert layout[1][0] == child_b
    assert layout[1][1] == {'y': 4, 'x': 0, 'height': 4, 'width': 90}
    assert layout[2][0] == child_c
    assert layout[2][1] == {'y': 8, 'x': 0, 'height': 4, 'width': 90}
    assert layout[3][0] == child_d
    assert layout[3][1] == {'y': 12, 'x': 0, 'height': 4, 'width': 90}


def test_widget_focus(root):
    parent = Widget(root).focus()
    assert isinstance(parent, Widget)

    child_a = Widget(parent).grid(0, 0)
    child_b = Widget(parent).grid(0, 1)
    assert isinstance(child_a, Widget)
    assert isinstance(child_b, Widget)

    parent.render()

    child_a.focus()
    curses.doupdate()
    cursor_y, cursor_x = curses.getsyx()
    assert (cursor_y, cursor_x) == (0, 0)

    child_b.focus()
    curses.doupdate()
    cursor_y, cursor_x = curses.getsyx()
    assert (cursor_y, cursor_x) == (0, 45)


def test_widget_blur(root):
    widget = Widget(root).blur()

    assert isinstance(widget, Widget)
    cursor_y, cursor_x = curses.getsyx()
    assert (cursor_y, cursor_x) == (0, 0)


def test_widget_arrange_proportion(root):
    parent = Widget(root)

    child_a = Widget(parent, position='fixed').pin(y=5, x=5, height=5, width=5)
    child_b = Widget(parent)
    child_c = Widget(
        parent, position='fixed', proportion={'height': 0.8, 'width': 0.8})

    assert parent.arrange(parent.children) == []

    parent.render()

    arrangement = parent.arrange(parent.children)

    assert len(arrangement) == 2

    _, child_a_dimensions = arrangement[0]

    assert child_a_dimensions == {'y': 5, 'x': 5, 'height': 5, 'width': 5}

    _, child_c_dimensions = arrangement[1]

    assert child_c_dimensions == {'y': 0, 'x': 0, 'height': 14, 'width': 72}


def test_widget_arrange_align(root):
    parent = Widget(root)

    Widget(parent, name='child_a',
           position='fixed', height=10, width=10, align='LL')
    Widget(parent, name='child_b',
           position='fixed', height=10, width=10, align='LC')
    Widget(parent, name='child_c',
           position='fixed', height=10, width=10, align='LR')

    Widget(parent, name='child_d',
           position='fixed', height=10, width=10, align='CL')
    Widget(parent, name='child_e',
           position='fixed', height=10, width=10, align='CC')
    Widget(parent, name='child_f',
           position='fixed', height=10, width=10, align='CR')

    Widget(parent, name='child_g',
           position='fixed', height=10, width=10, align='RL')
    Widget(parent, name='child_h',
           position='fixed', height=10, width=10, align='RC')
    Widget(parent, name='child_i',
           position='fixed', height=10, width=10, align='RR')

    parent.render()

    arrangement = parent.arrange(parent.children)

    assert len(arrangement) == 9

    _, child_a_dimensions = arrangement[0]
    assert child_a_dimensions == {'y': 0, 'x': 0, 'height': 10, 'width': 10}

    _, child_b_dimensions = arrangement[1]
    assert child_b_dimensions == {'y': 0, 'x': 40, 'height': 10, 'width': 10}

    _, child_c_dimensions = arrangement[2]
    assert child_c_dimensions == {'y': 0, 'x': 80, 'height': 10, 'width': 10}

    _, child_d_dimensions = arrangement[3]
    assert child_d_dimensions == {'y': 4, 'x': 0, 'height': 10, 'width': 10}

    _, child_e_dimensions = arrangement[4]
    assert child_e_dimensions == {'y': 4, 'x': 40, 'height': 10, 'width': 10}

    _, child_f_dimensions = arrangement[5]
    assert child_f_dimensions == {'y': 4, 'x': 80, 'height': 10, 'width': 10}

    _, child_g_dimensions = arrangement[6]
    assert child_g_dimensions == {'y': 8, 'x': 0, 'height': 10, 'width': 10}

    _, child_h_dimensions = arrangement[7]
    assert child_h_dimensions == {'y': 8, 'x': 40, 'height': 10, 'width': 10}

    _, child_i_dimensions = arrangement[8]
    assert child_i_dimensions == {'y': 8, 'x': 80, 'height': 10, 'width': 10}


def test_widget_arrange_margin(root):
    parent = Widget(root)

    Widget(parent, name='child_a', y=1, x=1,
           position='fixed', height=10, width=10, margin={'top': 5})
    Widget(parent, name='child_b', y=16, x=1,
           position='fixed', height=10, width=10, margin={'bottom': 2})
    Widget(parent, name='child_c', y=1, x=1,
           position='fixed', height=10, width=10, margin={'left': 3})
    Widget(parent, name='child_d', y=1, x=85,
           position='fixed', height=10, width=10, margin={'right': 4})

    parent.render()

    arrangement = parent.arrange(parent.children)

    assert len(arrangement) == 4

    _, child_a_dimensions = arrangement[0]
    assert child_a_dimensions == {'y': 5, 'x': 1, 'height': 10, 'width': 10}

    _, child_b_dimensions = arrangement[1]
    assert child_b_dimensions == {'y': 6, 'x': 1, 'height': 10, 'width': 10}

    _, child_c_dimensions = arrangement[2]
    assert child_c_dimensions == {'y': 1, 'x': 3, 'height': 10, 'width': 10}

    _, child_d_dimensions = arrangement[3]
    assert child_d_dimensions == {'y': 1, 'x': 76, 'height': 10, 'width': 10}
