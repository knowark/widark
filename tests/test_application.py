from widark.application import Application
from widark.widget import Widget


def test_application_instantiation():
    application = Application()
    assert isinstance(application, Widget)
    assert application.window is not None
