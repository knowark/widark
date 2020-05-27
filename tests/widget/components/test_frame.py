import curses
from widark.widget import Frame


def test_frame_instantiation_defaults(root):
    frame = Frame(root)
    assert frame.title == ''
    assert frame.title_styling.align == 'C'
    assert frame.title_styling.template == ' {} '


def test_frame_amend(root):
    frame = Frame(root, title='Details').render().update()
    curses.doupdate()

    title_text = frame.window.instr(0, 42, 7)

    assert title_text == b'Details'


def test_frame_title_style(root):
    frame = Frame(root, title='Details').title_style('SUCCESS', align='L')

    assert frame.title_styling.color == 'SUCCESS'
    assert frame.title_styling.align == 'L'


def test_frame_amend_right_align(root):
    frame = Frame(
        root, title='Details').title_style(align='R').render().update()
    curses.doupdate()

    title_text = frame.window.instr(0, 83, 9)

    assert title_text == b'Details'


def test_frame_amend_left_align(root):
    frame = Frame(
        root, title='Details').title_style(align='L').render().update()
    curses.doupdate()

    title_text = frame.window.instr(0, 2, 7)

    assert title_text == b'Details'
