from widark.widget import Widget


def test_widget_instantiation_defaults():
    widget = Widget()
    assert isinstance(widget, Widget)
    assert widget.parent is None
    assert widget.children == []
