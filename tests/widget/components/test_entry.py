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


async def test_button_on_click(root):
    focus_called = False

    def mock_focus(self):
        nonlocal focus_called
        focus_called = True
        return self

    entry = Entry(root, 'QWERTY')
    entry.focus = MethodType(mock_focus, entry)

    event = Event('Custom', 'click')

    await entry.dispatch(event)

    assert focus_called is True


async def test_button_on_keydown_backspace(root):
    given_content = None

    def mock_update(self, content):
        nonlocal given_content
        given_content = content
        return self

    entry = Entry(root, 'QWERTY')
    entry.update = MethodType(mock_update, entry)

    event = Event('Custom', 'keydown', key=chr(curses.KEY_BACKSPACE))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert given_content == 'QWERT'


async def test_button_on_keydown_all(root):
    given_content = None

    def mock_update(self, content):
        nonlocal given_content
        self.content = content
        given_content = content
        return self

    entry = Entry(root, 'QWERTY')
    entry.update = MethodType(mock_update, entry)

    event_1 = Event('Custom', 'keydown', key='U')
    await entry.dispatch(event_1)
    event_2 = Event('Custom', 'keydown', key='I')
    await entry.dispatch(event_2)

    assert given_content == 'QWERTYUI'
