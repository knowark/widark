from pytest import fixture
from widark.widget import Widget


@fixture
def widget():
    return Widget()


def test_widget_instantiation(widget):
    assert isinstance(widget, Widget)
