from widark.widget import Event, Target


def test_event_instantiation_defaults():
    event = Event('Mouse', 'click')
    assert event.category == 'Mouse'
    assert event.type == 'click'
    assert event.y == 0
    assert event.x == 0
    assert event.details == {}


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
    assert target.listeners == {'capture': [], 'bubble': []}


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

    assert click_handler in target.listeners['bubble']

    target.listen('click', click_handler, True)

    assert click_handler in target.listeners['capture']
