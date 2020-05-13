import inspect
import curses
import asyncio
from types import MethodType
from pytest import mark, fixture, raises
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
    assert application.window is None
    assert application._rate == 1 / 20
    assert application.active is True


async def test_application_build(application):
    await application.build()

    assert application.window is None
    assert len(application.children) == 2


async def test_application_run(application, monkeypatch):
    start_screen_called = False
    build_called = False
    attach_called = False
    doupdate_called = False
    stop_screen_called = False

    def mock_start_screen(self) -> None:
        class MockWindow:
            def getch(self):
                return -1
        self.window = MockWindow()
        nonlocal start_screen_called
        start_screen_called = True

    async def mock_build(self) -> None:
        nonlocal build_called
        build_called = True

    def mock_attach(self) -> None:
        nonlocal attach_called
        attach_called = True

    def mock_doupdate() -> None:
        nonlocal doupdate_called
        doupdate_called = True

    def mock_stop_screen(self) -> None:
        nonlocal stop_screen_called
        stop_screen_called = True

    application._start_screen = MethodType(mock_start_screen, application)
    application.build = MethodType(mock_build, application)
    application.attach = MethodType(mock_attach, application)
    monkeypatch.setattr(curses, "doupdate", mock_doupdate)
    application._stop_screen = MethodType(mock_stop_screen, application)

    await asyncio.wait([application.run()], timeout=1/10)

    assert start_screen_called is True
    assert build_called is True
    assert attach_called is True
    assert doupdate_called is True
    assert stop_screen_called is True


async def test_application_not_active(application):
    application.active = False

    await application.run()

    assert application.window is None


async def test_application_run_exception(application, monkeypatch):
    async def mock_sleep(seconds):
        raise ValueError('Test error.')

    monkeypatch.setattr(asyncio, "sleep", mock_sleep)

    with raises(ValueError):
        await application.run()

    assert application.window is None


async def test_application_process(application):
    attach_called = False
    clear_screen_called = False

    def mock_attach(self) -> None:
        nonlocal attach_called
        attach_called = True

    def mock_clear_screen(self) -> None:
        nonlocal clear_screen_called
        clear_screen_called = True

    application.attach = MethodType(mock_attach, application)
    application._clear_screen = MethodType(mock_clear_screen, application)

    await application._process(curses.KEY_RESIZE)

    assert attach_called is True
    assert clear_screen_called is True


async def test_application_interrupt(application):
    stop_screen_called = False

    def mock_stop_screen(self) -> None:
        nonlocal stop_screen_called
        stop_screen_called = True

    application._stop_screen = MethodType(mock_stop_screen, application)

    with raises(SystemExit):
        application._interrupt(0, None)

    assert stop_screen_called is True
