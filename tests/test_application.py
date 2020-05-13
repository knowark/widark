import inspect
from types import MethodType
from pytest import mark, fixture
from widark.application import Application
from widark.widget import Widget


pytestmark = mark.asyncio


@fixture
def application():
    class CustomApplication(Application):
        async def build(self) -> None:
            Widget(self, 'First Child')
            Widget(self, 'Second Child')

    return CustomApplication()


def test_application_definition():
    methods = inspect.getmembers(Application, predicate=inspect.isfunction)
    methods = [item[0] for item in methods]
    assert 'run' in methods
    assert 'build' in methods


def test_application_instantiation(application):
    assert isinstance(application, Widget)
    assert isinstance(application, Application)
    assert application.window is not None
    assert application.rate == 1 / 20


async def test_application_build(application):
    await application.build()

    assert application.window is not None
    assert len(application.children) == 2


async def test_application_run(application):
    called = False

    async def mock_build(self) -> None:
        nonlocal called
        called = True

    application.build = MethodType(mock_build, application)

    await application.run()

    assert called is True
