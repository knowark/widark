import inspect
import curses
import asyncio
from types import MethodType
from pytest import mark, fixture, raises
from widark.application import Application
from widark.widget import Widget, Event


pytestmark = mark.asyncio


@fixture
def application():
    class CustomApplication(Application):
        def build(self) -> None:
            self.first = Widget(self, content='First Child').grid(0, 0)
            self.second = Widget(self, content='Second Child').grid(0, 1)
            self.third = Widget(self.first, content='Third Child').grid(0)
            self.fourth = Widget(self.first, content='Fourth Child').grid(1)

        def _start_screen(self) -> None:
            super()._start_screen()
            # Run all tests with a resolution
            # of 24 rows and 120 cols
            self.window.resize(24, 120)

        def _stop_screen(self) -> None:
            try:
                super()._stop_screen()
            except curses.error:
                pass

    return CustomApplication()


def test_application_definition():
    methods = inspect.getmembers(Application, predicate=inspect.isfunction)
    methods = [item[0] for item in methods]
    assert 'run' in methods


def test_application_instantiation(application):
    assert isinstance(application, Widget)
    assert isinstance(application, Application)
    assert application.window is None
    assert application._rate == 1 / 20
    assert application.active is True


def test_application_build(application):
    application.build()

    assert application.window is None
    assert len(application.children) == 2


async def test_application_run(application, monkeypatch):
    start_screen_called = False
    connect_called = False
    doupdate_called = False
    stop_screen_called = False

    def mock_start_screen(self) -> None:
        class MockWindow:
            def getch(self):
                return -1
        self.window = MockWindow()
        nonlocal start_screen_called
        start_screen_called = True

    def mock_connect(self) -> None:
        nonlocal connect_called
        connect_called = True

    def mock_doupdate() -> None:
        nonlocal doupdate_called
        doupdate_called = True

    def mock_stop_screen(self) -> None:
        nonlocal stop_screen_called
        stop_screen_called = True

    application._start_screen = MethodType(mock_start_screen, application)
    application.connect = MethodType(mock_connect, application)
    monkeypatch.setattr(curses, "doupdate", mock_doupdate)
    application._stop_screen = MethodType(mock_stop_screen, application)

    await asyncio.wait([application.run()], timeout=1/10)

    assert start_screen_called is True
    assert connect_called is True
    assert doupdate_called is True
    assert stop_screen_called is True


def test_application_read(application):
    class MockWindow:
        def __init__(self) -> None:
            self.index = -1
            self.values = [ord('A'), ord('B'), -1]

        def getch(self):
            self.index += 1
            return self.values[self.index]

    application.window = MockWindow()

    key, buffer = application._read()

    assert key == ord('A')
    assert buffer == [ord('A'), ord('B')]


async def test_application_not_active(application):
    application.active = False

    await application.run()
    await asyncio.sleep(1 / 15)

    assert application.window is None


async def test_application_run_exception(application, monkeypatch):
    async def mock_sleep(seconds):
        raise ValueError('Test error.')

    def mock_connect(self):
        pass

    monkeypatch.setattr(asyncio, "sleep", mock_sleep)
    application.connect = MethodType(mock_connect, application)

    with raises(ValueError):
        await application.run()

    assert application.window is None


async def test_application_process(application):
    render_called = False
    clear_screen_called = False

    def mock_render(self) -> None:
        nonlocal render_called
        render_called = True

    def mock_clear_screen(self) -> None:
        nonlocal clear_screen_called
        clear_screen_called = True

    application.render = MethodType(mock_render, application)
    application._clear_screen = MethodType(mock_clear_screen, application)

    await application._process(curses.KEY_RESIZE, [curses.KEY_RESIZE])

    assert render_called is True
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


async def test_application_capture(application):
    application.active = False
    original_stop_screen = application._stop_screen

    def mock_stop_screen(self) -> None:
        pass

    application._stop_screen = MethodType(mock_stop_screen, application)

    await application._run()
    curses.doupdate()
    await asyncio.sleep(1 / 15)

    event = Event('Mouse', 'click', y=15, x=35)
    widget = application._capture(event)

    application._stop_screen = original_stop_screen
    application._stop_screen()

    assert widget is not None
    assert widget is application.fourth
    assert event.path == [application.fourth, application.first, application]


async def test_application_process_mouse_events(application, monkeypatch):
    getmouse_called = False
    capture_event = None
    dispatch_event = None

    def mock_getmouse():
        nonlocal getmouse_called
        getmouse_called = True
        return (1, 5, 10, 0, 4)

    def mock_capture(self, event: Event):
        nonlocal capture_event
        capture_event = event
        return application

    async def mock_dispatch(self, event: Event):
        nonlocal dispatch_event
        dispatch_event = event

    monkeypatch.setattr(curses, "getmouse", mock_getmouse)
    application._capture = MethodType(mock_capture, application)
    application.dispatch = MethodType(mock_dispatch, application)

    await application._process(curses.KEY_MOUSE, [curses.KEY_MOUSE])

    assert getmouse_called is True
    assert getattr(capture_event, 'y') == 10
    assert getattr(capture_event, 'x') == 5
    assert capture_event is dispatch_event


async def test_application_process_keyboard_events(application, monkeypatch):
    getmouse_called = False
    capture_event = None
    dispatch_event = None

    def mock_getsyx():
        nonlocal getmouse_called
        getmouse_called = True
        return (8, 4)

    def mock_capture(self, event: Event):
        nonlocal capture_event
        capture_event = event
        return application

    async def mock_dispatch(self, event: Event):
        nonlocal dispatch_event
        dispatch_event = event

    monkeypatch.setattr(curses, "getsyx", mock_getsyx)
    application._capture = MethodType(mock_capture, application)
    application.dispatch = MethodType(mock_dispatch, application)

    await application._process(ord('W'), [ord('W')])

    assert getmouse_called is True
    assert getattr(capture_event, 'category') == 'Keyboard'
    assert getattr(capture_event, 'type') == 'keydown'
    assert getattr(capture_event, 'y') == 8
    assert getattr(capture_event, 'x') == 4
    assert capture_event is dispatch_event
