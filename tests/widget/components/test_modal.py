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


async def test_modal_on_backdrop(root):
    close_called = False

    async def on_modal_close(event: Event) -> None:
        nonlocal close_called
        close_called = True

    modal = Modal(root, on_modal_close).launch(5, 5, 20, 20)

    await modal.dispatch(Event('Mouse', 'click', y=15, x=15))

    assert close_called is False

    await modal.dispatch(Event('Mouse', 'click', y=3, x=3))

    assert close_called is True
