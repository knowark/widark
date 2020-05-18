from pytest import mark, raises, fixture
from widark.widget import Event, Target


pytestmark = mark.asyncio


def test_event_instantiation_defaults():
    event = Event('Mouse', 'click')
    assert event.category == 'Mouse'
    assert event.type == 'click'
    assert event.y == 0
    assert event.x == 0
    assert event.details == {}
    assert event.phase == ''
    assert event.path == []
    assert event.current is None
    assert event.target is None


def test_event_instantiation_arguments():
    event = Event('Custom', 'alert', y=5, x=3, details={'hello': 'world'})
    assert event.category == 'Custom'
    assert event.type == 'alert'
    assert event.y == 5
    assert event.x == 3
    assert event.details == {'hello': 'world'}


def test_target_instantiation_defaults():
    target = Target()
    assert target.parent is None
    assert target.y_min == 0
    assert target.x_min == 0
    assert target.y_max == 1
    assert target.x_max == 1
    assert target.capture_listeners == {}
    assert target.bubble_listeners == {}


def test_target_hit():
    event = Event('Mouse', 'click', y=3, x=7)
    target = Target()
    target.y_min = 1
    target.x_min = 6
    target.y_max = 5
    target.x_max = 10

    hit = target.hit(event)

    assert hit is True


def test_target_not_hit():
    event = Event('Mouse', 'click', y=3, x=15)
    target = Target()
    target.y_min = 1
    target.x_min = 6
    target.y_max = 5
    target.x_max = 10

    hit = target.hit(event)

    assert hit is False


def test_target_listen():
    target = Target()

    async def click_handler(event: Event) -> None:
        pass

    target.listen('click', click_handler)

    assert click_handler in target.bubble_listeners['click']

    target.listen('click', click_handler, True)

    assert click_handler in target.capture_listeners['click']


def test_target_ignore():
    target = Target()

    async def click_handler(event: Event) -> None:
        pass

    target.capture_listeners['click'].append(click_handler)
    target.bubble_listeners['click'].append(click_handler)

    target.ignore('click', click_handler)

    assert target.bubble_listeners['click'] == []

    target.ignore('click', click_handler, True)

    assert target.capture_listeners['click'] == []


@fixture
def targets():
    first = Target()
    first.y_min = 0
    first.x_min = 0
    first.y_max = 12
    first.x_max = 12

    second = Target()
    second.parent = first
    second.y_min = 3
    second.x_min = 3
    second.y_max = 6
    second.x_max = 9

    third = Target()
    third.parent = first
    third.y_min = 7
    third.x_min = 3
    third.y_max = 11
    third.x_max = 11

    fourth = Target()
    fourth.parent = third
    fourth.y_min = 8
    fourth.x_min = 6
    fourth.y_max = 10
    fourth.x_max = 8

    return first, second, third, fourth


async def test_target_dispatch(targets):
    first, _, _, fourth = targets

    calls = []

    async def capture_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('capture')

    async def bubble_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('bubble')

    first.listen('click', capture_click_handler, True)
    assert capture_click_handler in first.capture_listeners['click']

    fourth.listen('click', bubble_click_handler)
    assert bubble_click_handler in fourth.bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7)
    await fourth.dispatch(event)  # Dispatch

    assert len(first.capture_listeners['click']) == 1
    assert len(fourth.bubble_listeners['click']) == 1
    assert calls == ['capture', 'bubble']


async def test_target_dispatch_with_given_event_path(targets):
    first, _, third, fourth = targets

    calls = []

    async def capture_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('capture')

    async def bubble_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('bubble')

    first.listen('click', capture_click_handler, True)
    assert capture_click_handler in first.capture_listeners['click']

    fourth.listen('click', bubble_click_handler)
    assert bubble_click_handler in fourth.bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7)
    event.path = [
        fourth,
        third
    ]
    await fourth.dispatch(event)  # Dispatch

    assert len(first.capture_listeners['click']) == 1
    assert len(fourth.bubble_listeners['click']) == 1
    assert calls == ['bubble']