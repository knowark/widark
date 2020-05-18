import curses
from widark.widget import Frame


def test_frame_instantiation_defaults(root):
    frame = Frame(root)
    assert frame.title == ''
    assert frame.title_align == 'C'
    assert frame.title_template == ' {} '


def test_frame_settle(root):
    frame = Frame(root, 'Details').attach().update()
    curses.doupdate()

    title_text = frame.window.instr(0, 42, 7)

    assert title_text == b'Details'


def test_frame_settle_right_align(root):
    frame = Frame(root, 'Details', 'R').attach().update()
    curses.doupdate()

    title_text = frame.window.instr(0, 83, 9)

    assert title_text == b'Details'


def test_frame_settle_left_align(root):
    frame = Frame(root, 'Details', 'L').attach().update()
    curses.doupdate()

    title_text = frame.window.instr(0, 2, 7)

    assert title_text == b'Details'
