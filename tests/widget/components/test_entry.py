import curses
from pytest import mark
from types import MethodType
from widark.widget import Entry, Event


pytestmark = mark.asyncio


def test_entry_instantiation_defaults(root):
    entry = Entry(root)
    assert entry.content == ''
    assert len(entry._bubble_listeners['click']) == 1
    assert len(entry._bubble_listeners['keydown']) == 1


async def test_entry_on_click(root):
    focus_called = False

    def mock_focus(self):
        nonlocal focus_called
        focus_called = True
        return self

    entry = Entry(root, content='QWERTY')
    entry.focus = MethodType(mock_focus, entry)

    root.render()

    event = Event('Custom', 'click')

    await entry.dispatch(event)

    assert focus_called is True


async def test_entry_on_keydown_backspace(root):
    given_content = None

    def mock_render(self):
        nonlocal given_content
        given_content = self.content
        return self

    entry = Entry(root, content='QWERTY')
    entry.render = MethodType(mock_render, entry)

    event = Event('Custom', 'keydown', key=chr(curses.KEY_BACKSPACE))

    await entry.dispatch(event)

    assert given_content == 'QWERT'


async def test_entry_on_keydown_all(root):
    given_content = None

    def mock_render(self):
        nonlocal given_content
        given_content = self.content
        return self

    entry = Entry(root, content='QWERTY')
    entry.render = MethodType(mock_render, entry)

    event_1 = Event('Custom', 'keydown', key='U')
    await entry.dispatch(event_1)
    event_2 = Event('Custom', 'keydown', key='I')
    await entry.dispatch(event_2)

    assert given_content == 'QWERTYUI'


async def test_entry_on_keydown_arrows(root):
    entry = Entry(root, content='QWERTY')

    root.render()

    entry.focus()

    assert entry.window.getyx() == (1, 7)

    await entry.dispatch(Event('Custom', 'keydown', key=chr(curses.KEY_LEFT)))

    assert entry.window.getyx() == (1, 6)
