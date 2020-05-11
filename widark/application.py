import curses
from .widget import Widget


class Application(Widget):
    def __init__(self) -> None:
        super().__init__(None)
        self._start_screen()

    async def run(self) -> None:
        pass

    def _start_screen(self) -> None:
        self.window = curses.initscr()
        self.window.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

    def _stop_screen(self) -> None:
        self.window.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def __del__(self) -> None:
        self._stop_screen()
