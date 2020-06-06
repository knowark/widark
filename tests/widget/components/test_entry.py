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

    assert entry.content == (
        "Lorem ipsum dolor sit amet, c\n"
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
    )

    entry.move(0, 27)

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.content == (
        "rem ipsum dolor sit amet, con\n"
        " felis enim. Praesent facilis\n"
        " quis elit. Quisque nec moles\n"
        " interdum vitae, hendrerit so\n"
        " auctor enim. Etiam a pharetr\n"
        " aliquam metus rhoncus in. Nu\n"
        "llis orci. Cras quis mattis e\n"
        "istique senectus et netus et \n"
        "nec scelerisque nec tellus se\n"
        " tincidunt. Morbi et libero v\n"
    )


async def test_entry_left(entry):
    entry.move(2, 4)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_LEFT))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (2, 2)

    entry.base_x = 2
    entry.render()

    assert entry.content == (
        "rem ipsum dolor sit amet, con\n"
        " felis enim. Praesent facilis\n"
        " quis elit. Quisque nec moles\n"
        " interdum vitae, hendrerit so\n"
        " auctor enim. Etiam a pharetr\n"
        " aliquam metus rhoncus in. Nu\n"
        "llis orci. Cras quis mattis e\n"
        "istique senectus et netus et \n"
        "nec scelerisque nec tellus se\n"
        " tincidunt. Morbi et libero v\n"
    )

    entry.move(0, 0)

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.content == (
        "Lorem ipsum dolor sit amet, c\n"
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
    )


async def test_entry_up(entry):
    entry.move(4, 4)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_UP))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (2, 4)

    entry.base_y = 1
    entry.render()

    assert entry.content == (
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
        "iaculis dui.\n"
    )

    entry.move(0, 0)
    await entry.dispatch(event)

    assert entry.content == (
        "Lorem ipsum dolor sit amet, c\n"
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
    )

    entry.base_x = 40
    entry.render()
    entry.move(7, 25)

    assert entry.cursor() == (7, 25)
    assert entry.content == (
        "adipiscing elit. Maecenas\n"
        "vitae nunc posuere volutpat\n"
        ". Nunc sem est, vulputate\n"
        "ue. In vel iaculis lacus,\n"
        "Cras scelerisque erat magna\n"
        " sodales mauris, sit amet\n"
        "tesque habitant morbi\n"
        " fames ac turpis egestas.\n"
        ". Mauris eleifend et justo\n"
        "efficitur odio eu,\n"
    )

    await entry.dispatch(event)
    assert entry.cursor() == (6, 1)


async def test_entry_down(entry):
    entry.move(4, 4)

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_DOWN))

    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (6, 4)

    assert entry.content == (
        "Lorem ipsum dolor sit amet, c\n"
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
    )

    entry.move(8, 0)
    entry.base_y = 0
    entry.base_x = 0
    await entry.dispatch(event)

    assert entry.content == (
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
        "iaculis dui.\n"
    )

    entry.base_y = 0
    entry.base_x = 40
    entry.render()
    entry.move(8, 26)

    assert entry.cursor() == (8, 26)
    assert entry.content == (
        "adipiscing elit. Maecenas\n"
        "vitae nunc posuere volutpat\n"
        ". Nunc sem est, vulputate\n"
        "ue. In vel iaculis lacus,\n"
        "Cras scelerisque erat magna\n"
        " sodales mauris, sit amet\n"
        "tesque habitant morbi\n"
        " fames ac turpis egestas.\n"
        ". Mauris eleifend et justo\n"
        "efficitur odio eu,\n"
    )

    await entry.dispatch(event)
    assert entry.cursor() == (8, 26)

    entry.move(5, 0)
    entry.buffer = entry.buffer[:5]

    await entry.dispatch(event)
    assert entry.cursor() == (5, 0)


async def test_entry_backspace(entry):
    entry.move(4, 2)

    assert len(entry.buffer[4]) == 67

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_BACKSPACE))
    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (4, 0)
    assert len(entry.buffer[4]) == 65
    assert len(entry.buffer) == 11

    assert entry.content == (
        "Lorem ipsum dolor sit amet, c\n"
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        " auctor enim. Etiam a pharetr\n"
        "at aliquam metus rhoncus in. \n"
        "mollis orci. Cras quis mattis\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
    )

    entry.move(1, 0)
    await entry.dispatch(event)
    assert len(entry.buffer) == 10
    assert entry.cursor() == (0, 5)

    assert entry.content == (
        "cenasac felis enim. Praesent \n"
        "utate\n"
        "acus,\n"
        "magna\n"
        " amet\n"
        "i\n"
        "stas.\n"
        " justo\n"
        "\n"
        "\n"
    )

    entry.base_y = 0
    entry.base_x = 40
    entry.render()

    entry.move(1, 1)

    await entry.dispatch(event)
    assert entry.base_x == 39

    assert entry.content == (
        ' adipiscing elit. Maecenasac \n'
        'm Nunc sem est, vulputate\n'
        'gue. In vel iaculis lacus,\n'
        'ras scelerisque erat magna\n'
        'e sodales mauris, sit amet\n'
        'ntesque habitant morbi\n'
        'a fames ac turpis egestas.\n'
        't. Mauris eleifend et justo\n'
        ' efficitur odio eu,\n'
        '\n'
    )


async def test_entry_delete(entry):
    entry.move(8, 2)

    assert len(entry.buffer[8]) == 66

    event = Event('Keyboard', 'keydown', key=chr(curses.KEY_DC))
    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (8, 2)
    assert len(entry.buffer[8]) == 64

    entry.base_y = 0
    entry.base_x = 50
    entry.render()

    assert len(entry.buffer) == 11
    assert entry.content == (
        " elit. Maecenas\n"
        " posuere volutpat\n"
        " est, vulputate\n"
        " iaculis lacus,\n"
        "risque erat magna\n"
        "auris, sit amet\n"
        "itant morbi\n"
        "turpis egestas.\n"
        "ifend et justo\n"
        "odio eu,\n"
    )

    entry.move(3, 15)
    await entry.dispatch(event)

    assert len(entry.buffer) == 10
    assert entry.cursor() == (3, 15)
    assert entry.content == (
        " elit. Maecenas\n"
        " posuere volutpat\n"
        " est, vulputate\n"
        " iaculis lacus,eu auctor enim\n"
        "auris, sit amet\n"
        "itant morbi\n"
        "turpis egestas.\n"
        "ifend et justo\n"
        "odio eu,\n"
        "\n"
    )


async def test_entry_enter(entry):
    entry.move(3, 0)

    assert len(entry.buffer[3]) == 65
    assert len(entry.buffer[4]) == 67
    assert len(entry.buffer) == 11

    event = Event('Keyboard', 'keydown', key='\n')
    await entry.dispatch(event)
    await entry.dispatch(event)

    assert len(entry.buffer[3]) == 0
    assert len(entry.buffer[4]) == 0
    assert entry.cursor() == (5, 0)
    assert len(entry.buffer) == 13


async def test_entry_character(entry):
    entry.move(6, 0)

    assert len(entry.buffer[6]) == 61

    event = Event('Keyboard', 'keydown', key='A')
    await entry.dispatch(event)
    await entry.dispatch(event)

    assert entry.cursor() == (6, 2)
    assert len(entry.buffer[6]) == 63

    assert entry.content == (
        "Lorem ipsum dolor sit amet, c\n"
        "ac felis enim. Praesent facil\n"
        "et quis elit. Quisque nec mol\n"
        "ut interdum vitae, hendrerit \n"
        "eu auctor enim. Etiam a phare\n"
        "at aliquam metus rhoncus in. \n"
        "AAmollis orci. Cras quis matt\n"
        "tristique senectus et netus e\n"
        "Donec scelerisque nec tellus \n"
        "ut tincidunt. Morbi et libero\n"
    )

    entry.move(0, 27)

    event = Event('Keyboard', 'keydown', key='W')
    await entry.dispatch(event)

    assert entry.content == (
        "orem ipsum dolor sit amet, Wc\n"
        "c felis enim. Praesent facili\n"
        "t quis elit. Quisque nec mole\n"
        "t interdum vitae, hendrerit s\n"
        "u auctor enim. Etiam a pharet\n"
        "t aliquam metus rhoncus in. N\n"
        "Amollis orci. Cras quis matti\n"
        "ristique senectus et netus et\n"
        "onec scelerisque nec tellus s\n"
        "t tincidunt. Morbi et libero \n"
    )
