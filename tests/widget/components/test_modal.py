from pytest import mark
from widark.widget import Modal, Event


pytestmark = mark.asyncio


def test_modal_instantiation_defaults(root):
    modal = Modal(root)
    assert modal.position == 'fixed'


def test_modal_attach(root):
    modal = Modal(root)

    modal.attach()

    assert modal.window is not None


def test_modal_launch(root):
    modal = Modal(root)

    modal.launch()

    assert modal.window is not None
    assert modal.close.window is not None


async def test_modal_close(root):
    close_modal_called = False

    async def close_modal(event: Event):
        nonlocal close_modal_called
        close_modal_called = True

    modal = Modal(root, close_modal)

    modal.attach()

    await modal.close.dispatch(Event('Mouse', 'click'))

    assert close_modal_called is True
