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
