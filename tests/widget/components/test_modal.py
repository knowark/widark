import asyncio
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

    modal = Modal(root, done_command=close_modal)

    modal.build()

    await modal.close.dispatch(Event('Mouse', 'click'))

    assert close_modal_called is True


async def test_modal_done_modal(root):
    async def done_modal(event: Event):
        pass

    modal = Modal(root, done_command=done_modal).render()

    assert done_modal is modal.done_command

    event_details = None

    async def new_done_modal(event: Event):
        nonlocal event_details
        event_details = event.details

    modal.setup(done_command=new_done_modal).connect()

    await asyncio.sleep(1 / 15)

    await modal.close.dispatch(Event('Mouse', 'click'))

    assert event_details == {'result': 'closed'}


async def test_modal_done_external(root):
    modal = Modal(root).render()

    external_event_details = None

    async def external_handler(event: Event):
        nonlocal external_event_details
        external_event_details = event.details

    modal.setup(done_command=None).listen('done', external_handler).connect()

    await modal.close.dispatch(Event('Mouse', 'click'))

    await asyncio.sleep(1 / 15)

    assert external_event_details == {'result': 'closed'}
    assert len(modal.close._bubble_listeners) == 1
