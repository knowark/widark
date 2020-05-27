from pytest import mark
from widark.widget import Modal, Event


pytestmark = mark.asyncio


def test_modal_instantiation_defaults(root):
    modal = Modal(root)
    assert modal.position == 'fixed'


def test_modal_render(root):
    modal = Modal(root)

    modal.render()

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

    modal = Modal(root, close_command=close_modal)

    modal.render()

    await modal.close.dispatch(Event('Mouse', 'click'))

    assert close_modal_called is True


async def test_modal_setup(root):
    async def close_modal(event: Event):
        pass

    modal = Modal(root, close_command=close_modal)

    assert close_modal in modal.close._bubble_listeners['click']
    assert len(modal.close._bubble_listeners) == 1

    original_close = modal.close

    async def new_close_modal(event: Event):
        pass

    modal.setup(close_command=new_close_modal)

    assert new_close_modal in modal.close._bubble_listeners['click']
    assert len(modal.close._bubble_listeners) == 1
    assert modal.close is not original_close
