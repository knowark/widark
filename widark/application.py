import sys
import curses
import asyncio
from signal import signal, SIGINT
from typing import List, Any
from .widget import Widget, Event, Target
from .palette import DefaultPalette, Palette


class Application(Widget):
    def __init__(self, palette: Palette = None) -> None:
        super().__init__(None)
        self.active = True
        self.palette = palette or DefaultPalette()
        self._rate = 1 / 20
        signal(SIGINT, self._interrupt)

    async def build(self) -> None:
        """Interface building method"""

    async def run(self) -> None:
        try:
            await self._run()
        except Exception:
            self._stop_screen()
            raise

    async def _run(self) -> None:
        self._start_screen()
        await self.build()
        self.attach()

        while self.active:
            await asyncio.sleep(self._rate)
            key = self.window.getch()

            await self._process(key)

            curses.doupdate()
            curses.flushinp()

        self._stop_screen()

    async def _process(self, key: int) -> None:
        if key == curses.KEY_RESIZE:
            self._clear_screen()
            self.attach()  # .update()
        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            event = Event('Mouse', 'click', y=y, x=x, key=chr(key))
            target = self._capture(event)
            await target.dispatch(event)
        elif key >= 0:
            y, x = curses.getsyx()
            event = Event('Keyboard', 'keydown', y=y, x=x, key=chr(key))
            target = self._capture(event)
            await target.dispatch(event)

    def _capture(self, event: Event) -> Widget:
        target: Widget = self
        path: List[Target] = [self]

        children = target.children
        while children:  # pragma: no cover
            for child in children:
                if child.hit(event):
                    children = child.children
                    target = child
                    path.append(target)
                    break
            else:
                children = []

        event.path = list(reversed(path))
        return target

    def _start_screen(self) -> None:
        self.window = curses.initscr()
        self.window.timeout(0)
        self.window.keypad(True)
        self.window.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.mousemask(
            curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.start_color()
        curses.use_default_colors()
        for pair, foreground, background in self.palette.generate():
            curses.init_pair(pair, foreground, background)

    def _clear_screen(self) -> None:
        self.window.clear()

    def _stop_screen(self) -> None:
        self._clear_screen()
        self.window.timeout(-1)
        self.window.keypad(False)
        self.window.nodelay(False)
        self.window = None
        curses.echo()
        curses.nocbreak()
        curses.mousemask(False)
        curses.endwin()

    def _interrupt(self, signal: int, frame: Any) -> None:
        self._stop_screen()
        sys.exit(0)
