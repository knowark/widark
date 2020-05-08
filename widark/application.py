import curses
from .widget import Widget


class Application(Widget):
    def __init__(self) -> None:
        super().__init__(None)
        curses.wrapper(self._setup_screen)

    def _setup_screen(self, stdscr) -> None:
        self.window = stdscr
