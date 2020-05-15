import sys
import curses
import asyncio
from signal import signal, SIGINT
from typing import List, Any
from .widget import Widget, Event, Target


class Application(Widget):
    def __init__(self) -> None:
        super().__init__(None)
        self.active = True
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
            self.attach()

    def _capture(self, event: Event) -> Widget:
        target: Widget = self
        path: List[Target] = [self]

        while target.children:  # pragma: no cover
            target = next(item for item in target.children
                          if item.hit(event))
            path.append(target)

        event.path = list(reversed(path))
        return target

    def _start_screen(self) -> None:
        self.window = curses.initscr()
        self.window.timeout(0)
        self.window.keypad(True)
        self.window.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

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
        curses.endwin()

    def _interrupt(self, signal: int, frame: Any) -> None:
        self._stop_screen()
        sys.exit(0)
