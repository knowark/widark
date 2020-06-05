import curses
from pytest import mark, fixture
from types import MethodType
from widark.widget import Event
from widark.widget.components.entry import Entry


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

    event = Event('Mouse', 'click')

    await entry.dispatch(event)

    assert focus_called is True


def test_entry_text(root):
    content = 'Hello\nWorld'
    entry = Entry(root, content=content)
    assert entry.buffer == [
        'Hello',
        'World'
    ]
    assert entry.text == content


# async def test_entry_on_keydown_backspace(root):
#     given_content = None

#     def mock_render(self):
#         nonlocal given_content
#         given_content = self.content
#         return self

#     entry = Entry(root, content='QWERTY')
#     entry.render = MethodType(mock_render, entry)

#     event = Event('Custom', 'keydown', key=chr(curses.KEY_BACKSPACE))

#     await entry.dispatch(event)

#     assert given_content == 'QWERT'


# async def test_entry_on_keydown_all(root):
#     given_content = None

#     def mock_render(self):
#         nonlocal given_content
#         given_content = self.content
#         return self

#     entry = Entry(root, content='QWERTY')
#     entry.render = MethodType(mock_render, entry)

#     event_1 = Event('Custom', 'keydown', key='U')
#     await entry.dispatch(event_1)
#     event_2 = Event('Custom', 'keydown', key='I')
#     await entry.dispatch(event_2)

#     assert given_content == 'QWERTYUI'


# async def test_entry_on_keydown_arrows(root):
#     entry = Entry(root, content='QWERTY')

#     root.render()

#     entry.focus()

#     assert entry.window.getyx() == (1, 7)

#     await entry.dispatch(Event('Custom', 'keydown',
#       key=chr(curses.KEY_LEFT)))

#     assert entry.window.getyx() == (1, 6)


@fixture
def entry(root):
    content = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas\n"
        "ac felis enim. Praesent facilisis lacus vitae nunc posuere volutpat\n"
        "et quis elit. Quisque nec molestie lorem. Nunc sem est, vulputate\n"
        "ut interdum vitae, hendrerit sodales augue. In vel iaculis lacus,\n"
        "eu auctor enim. Etiam a pharetra velit. Cras scelerisque erat magna\n"
        "at aliquam metus rhoncus in. Nulla vitae sodales mauris, sit amet\n"
        "mollis orci. Cras quis mattis ex. Pellentesque habitant morbi\n"
        "tristique senectus et netus et malesuada fames ac turpis egestas.\n"
        "Donec scelerisque nec tellus sed laoreet. Mauris eleifend et justo\n"
        "ut tincidunt. Morbi et libero volutpat, efficitur odio eu,\n"
        "iaculis dui."
    )

    # Entry of hight: 10 and width: 30
    entry = Entry(root, content=content, position='fixed').pin(0, 0, 10, 30)
    root.render()
    return entry


async def test_entry_right(entry):
    entry.move(0, 0)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_RIGHT))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (0, 2)


async def test_entry_left(entry):
    entry.move(2, 4)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_LEFT))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (2, 2)


async def test_entry_up(entry):
    entry.move(4, 4)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_UP))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (2, 4)


async def test_entry_down(entry):
    entry.move(4, 4)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_DOWN))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (6, 4)


async def test_entry_on_keydown_backspace(entry):
    entry.move(4, 2)

    assert len(entry.buffer[4]) == 67

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_BACKSPACE))
    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (4, 0)
    assert len(entry.buffer[4]) == 65
