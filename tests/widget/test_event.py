from pytest import mark, raises, fixture
from widark.widget import Event, Target


pytestmark = mark.asyncio


def test_event_instantiation_defaults():
    event = Event('Mouse', 'click')
    assert event.category == 'Mouse'
    assert event.type == 'click'
    assert event.y == 0
    assert event.x == 0
    assert event.key == ''
    assert event.button == 0
    assert event.bubbles is True
    assert event.stop is False
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
    assert target._y_min == 0
    assert target._x_min == 0
    assert target._y_max == 0
    assert target._x_max == 0
    assert target._capture_listeners == {}
    assert target._bubble_listeners == {}


def test_target_hit():
    event = Event('Mouse', 'click', y=3, x=7)
    target = Target()
    target._y_min = 1
    target._x_min = 6
    target._y_max = 5
    target._x_max = 10

    hit = target.hit(event)

    assert hit is True


def test_target_not_hit():
    event = Event('Mouse', 'click', y=3, x=15)
    target = Target()
    target._y_min = 1
    target._x_min = 6
    target._y_max = 5
    target._x_max = 10

    hit = target.hit(event)

    assert hit is False


def test_target_listen():
    target = Target()

    async def click_handler(event: Event) -> None:
        pass

    target.listen('click', click_handler)

    assert click_handler in target._bubble_listeners['click']

    target.listen('click', click_handler, True)

    assert click_handler in target._capture_listeners['click']


def test_target_ignore():
    target = Target()

    async def click_handler(event: Event) -> None:
        pass

    target._capture_listeners['click'].append(click_handler)
    target._bubble_listeners['click'].append(click_handler)

    target.ignore('click', click_handler)

    assert target._bubble_listeners['click'] == []

    target.ignore('click', click_handler, True)

    assert target._capture_listeners['click'] == []


def test_target_ignore_all():
    target = Target()

    async def click_handler(event: Event) -> None:
        pass

    target._capture_listeners['click'].append(click_handler)
    target._bubble_listeners['click'].append(click_handler)

    target.ignore('click')

    assert target._bubble_listeners['click'] == []

    target.ignore('click', capture=True)

    assert target._capture_listeners['click'] == []


@fixture
def targets():
    first = Target()
    first._y_min = 0
    first._x_min = 0
    first._y_max = 12
    first._x_max = 12

    second = Target()
    second.parent = first
    second._y_min = 3
    second._x_min = 3
    second._y_max = 6
    second._x_max = 9

    third = Target()
    third.parent = first
    third._y_min = 7
    third._x_min = 3
    third._y_max = 11
    third._x_max = 11

    fourth = Target()
    fourth.parent = third
    fourth._y_min = 8
    fourth._x_min = 6
    fourth._y_max = 10
    fourth._x_max = 8

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
    assert capture_click_handler in first._capture_listeners['click']

    fourth.listen('click', bubble_click_handler)
    assert bubble_click_handler in fourth._bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7)
    await fourth.dispatch(event)  # Dispatch

    assert len(first._capture_listeners['click']) == 1
    assert len(fourth._bubble_listeners['click']) == 1
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
    assert capture_click_handler in first._capture_listeners['click']

    fourth.listen('click', bubble_click_handler)
    assert bubble_click_handler in fourth._bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7)
    event.path = [
        fourth,
        third
    ]
    await fourth.dispatch(event)  # Dispatch

    assert len(first._capture_listeners['click']) == 1
    assert len(fourth._bubble_listeners['click']) == 1
    assert calls == ['bubble']


async def test_target_dispatch_bubbles_false(targets):
    first, _, _, fourth = targets

    calls = []

    async def capture_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('capture')

    async def bubble_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('bubble')

    first.listen('click', capture_click_handler, True)
    assert capture_click_handler in first._capture_listeners['click']

    fourth.listen('click', capture_click_handler, True)
    fourth.listen('click', bubble_click_handler)
    assert capture_click_handler in fourth._capture_listeners['click']
    assert bubble_click_handler in fourth._bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7, bubbles=False)

    await fourth.dispatch(event)  # Dispatch

    assert len(first._capture_listeners['click']) == 1
    assert len(fourth._capture_listeners['click']) == 1
    assert len(fourth._bubble_listeners['click']) == 1
    assert calls == ['capture', 'capture']


async def test_target_dispatch_event_stop_bubbling(targets):
    first, _, third, fourth = targets

    calls = []

    async def capture_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('capture')

    async def bubble_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('bubble')

    async def stop_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('bubble:stopped')
        event.stop = True

    first.listen('click', capture_click_handler, True)
    assert capture_click_handler in first._capture_listeners['click']

    third.listen('click', bubble_click_handler)
    assert bubble_click_handler in third._bubble_listeners['click']
    assert third.parent == first

    fourth.listen('click', capture_click_handler, True)
    fourth.listen('click', stop_click_handler)
    assert capture_click_handler in fourth._capture_listeners['click']
    assert stop_click_handler in fourth._bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7)

    await fourth.dispatch(event)  # Dispatch

    assert len(first._capture_listeners['click']) == 1
    assert len(third._bubble_listeners['click']) == 1
    assert len(fourth._capture_listeners['click']) == 1
    assert len(fourth._bubble_listeners['click']) == 1
    assert calls == ['capture', 'capture', 'bubble:stopped']


async def test_target_dispatch_event_stop_capturing(targets):
    first, _, third, fourth = targets

    calls = []

    async def capture_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('capture')

    async def bubble_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('bubble')

    async def stop_click_handler(event: Event) -> None:
        nonlocal calls
        calls.append('capture:stopped')
        event.stop = True

    first.listen('click', capture_click_handler, True)
    assert capture_click_handler in first._capture_listeners['click']

    third.listen('click', stop_click_handler, True)
    assert stop_click_handler in third._capture_listeners['click']
    assert third.parent == first

    fourth.listen('click', capture_click_handler, True)
    fourth.listen('click', bubble_click_handler)
    assert capture_click_handler in fourth._capture_listeners['click']
    assert bubble_click_handler in fourth._bubble_listeners['click']
    assert fourth.parent.parent == first

    event = Event('Mouse', 'click', y=9, x=7)

    await fourth.dispatch(event)  # Dispatch

    assert len(first._capture_listeners['click']) == 1
    assert len(third._bubble_listeners['click']) == 0
    assert len(third._capture_listeners['click']) == 1
    assert len(fourth._capture_listeners['click']) == 1
    assert len(fourth._bubble_listeners['click']) == 1
    assert calls == ['capture', 'capture:stopped']
