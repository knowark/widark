from widark.widget import Event


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
