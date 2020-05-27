from pytest import mark
from widark.widget import Button, Event


pytestmark = mark.asyncio


def test_button_instantiation_defaults(root):
    button = Button(root)
    assert button.styling.template == '< {} >'
    assert button.content == ''


async def test_button_command(root):
    command_called = False

    async def custom_command(event: Event):
        nonlocal command_called
        command_called = True

    button = Button(root, content='Accept', command=custom_command)

    event = Event('Custom', 'click')

    await button.dispatch(event)

    assert button.content == 'Accept'
    assert command_called is True
