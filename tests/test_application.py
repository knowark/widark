import pytest
from widark.application import Application
from widark.widget import Widget


pytestmark = pytest.mark.asyncio


def test_application_instantiation():
    application = Application()

    assert isinstance(application, Widget)
    assert application.window is None


async def test_application_run():
    application = Application()
    await application.run()

    assert application.window is not None
