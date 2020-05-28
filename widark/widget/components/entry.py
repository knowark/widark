import curses
from math import ceil, floor
from ..widget import Widget
from ..event import Event


class Entry(Widget):
    def setup(self, **context) -> 'Entry':
        self.listen('click', self.on_click)
        self.listen('keydown', self.on_keydown)
        return super().setup(**context) and self

    async def on_click(self, event: Event) -> None:
        event.stop = True
        self.focus()
        origin, approx = (1, ceil) if self.styling.border else (0, floor)
        self.move(approx((len(self.content) + origin) / self.width),
                  (len(self.content) + origin) % self.width)

    async def on_keydown(self, event: Event) -> None:
        self.clear()
        content = self.content
        if ord(event.key) == curses.KEY_BACKSPACE:
            content = content[:-1]
        else:
            content += event.key
        self.content = content
        self.render()
