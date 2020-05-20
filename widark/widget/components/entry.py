import curses
from math import ceil, floor
from ..widget import Widget
from ..event import Event


class Entry(Widget):
    def __init__(self, parent: 'Widget', content: str = '') -> None:
        super().__init__(parent, content)
        self.listen('click', self.on_click)
        self.listen('keydown', self.on_keydown)

    async def on_click(self, event: Event) -> None:
        event.stop = True
        self.focus()
        origin, approx = (1, ceil) if self._style.border else (0, floor)
        _, width = self.size()
        self.move(approx((len(self.content) + origin) / width),
                  (len(self.content) + origin) % width)

    async def on_keydown(self, event: Event) -> None:
        self.clear()
        content = self.content
        if ord(event.key) == curses.KEY_BACKSPACE:
            content = content[:-1]
        else:
            content += event.key
        self.update(content)
