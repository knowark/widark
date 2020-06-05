import curses
from math import ceil, floor
from typing import List
from ..widget import Widget
from ..event import Event
from ..style import Style


class Entry(Widget):
    def setup(self, **context) -> 'Entry':
        content = context.pop('content', '')

        self.buffer: List[str] = content.splitlines()
        self.base_y: int = 0
        self.base_x: int = 0

        self.listen('click', self.on_click)
        self.listen('keydown', self.on_keydown)
        return super().setup(**context) and self

    @property
    def text(self) -> str:
        return '\n'.join(self.buffer)

    async def on_click(self, event: Event) -> None:
        event.stop = True
        self.focus()

    def focus(self) -> 'Entry':
        super().focus()
        return self

    def settle(self) -> None:
        height, width = self.size()

        content = ''
        for line in self.buffer[self.base_y: height + self.base_y]:
            sentence = line[self.base_x: width - 1 + self.base_x]
            content += f'{sentence}\n'

        self.content = content

    async def on_keydown(self, event: Event) -> None:
        height, width = self.size()
        y, x = self.cursor()

        if ord(event.key) == curses.KEY_LEFT:
            self._left(y, x, height, width)
        elif ord(event.key) == curses.KEY_RIGHT:
            self._right(y, x, height, width)
        elif ord(event.key) == curses.KEY_UP:
            self._up(y, x, height, width)
        elif ord(event.key) == curses.KEY_DOWN:
            self._down(y, x, height, width)
        elif ord(event.key) == curses.KEY_BACKSPACE:
            line = y
            pillar = max(x - 1, 0)
            if x == 0:
                row = self.buffer.pop(self.base_y + y)
                line = max(line - 1, 0)
                pillar = len(self.buffer[max(self.base_y + y - 1, 0)])
                self.buffer[max(self.base_y + y - 1, 0)] += row

            self.buffer[self.base_y + y] = (
                self.buffer[self.base_y + y][:max(self.base_x + x - 1, 0)] +
                self.buffer[self.base_y + y][self.base_x + x:])

            self.render().move(line, pillar)
        elif ord(event.key) == curses.KEY_DC:
            if (x == len(self.buffer[self.base_y + y]) and
                    self.base_y + y < len(self.buffer) - 1):
                row = self.buffer.pop(self.base_y + y + 1)
                self.buffer[self.base_y + y] += row
            else:
                self.buffer[self.base_y + y] = (
                    self.buffer[self.base_y + y][:self.base_x + x] +
                    self.buffer[self.base_y + y][self.base_x + x + 1:])
            self.render().move(y, x)
        elif event.key == '\n':
            head, tail = (
                self.buffer[self.base_y + y][:self.base_x + x],
                self.buffer[self.base_y + y][self.base_x + x:])
            self.buffer[self.base_y + y] = head
            self.buffer.insert(self.base_y + y + 1, tail)
            self.render().move(y + 1)
        else:
            self.buffer[self.base_y + y] = (
                self.buffer[self.base_y + y][:x] +
                event.key +
                self.buffer[self.base_y + y][x:])
            self.render().move(y, x + 1)

    def _right(self, y: int, x: int, height: int, width: int) -> None:
        sentence = self.buffer[self.base_y + y]
        if x == width - 1:
            max_shift = max(len(sentence) - width + 1, 0)
            self.base_x = min(self.base_x + 1, max_shift)
            self.render()
        self.move(y, min(x + 1, max(len(sentence) - self.base_x, 0)))

    def _left(self, y: int, x: int, height: int, width: int) -> None:
        if x == 0:
            self.base_x = max(self.base_x - 1, 0)
            self.render()
        self.move(y,  max(x - 1, 0))

    def _up(self, y: int, x: int, height: int, width: int) -> None:
        if y == 0:
            self.base_y = max(self.base_y - 1, 0)
        line = max(y - 1, 0)
        sentence = self.buffer[line + self.base_y]
        if x > len(sentence) - self.base_x:
            self.base_x = int(len(sentence) / width) * width
        pillar = min(x, max(len(sentence) - self.base_x, 0))
        self.render().move(line, pillar)

    def _down(self, y: int, x: int, height: int, width: int) -> None:
        if y == height - 1:
            max_shift = max(len(self.buffer) - height, 0)
            self.base_y = min(self.base_y + 1, max_shift)
        line = min(y + 1, height - 1)
        sentence = self.buffer[line + self.base_y]
        if x > len(sentence) - self.base_x:
            self.base_x = int(len(sentence) / width) * width
        pillar = min(x, max(len(sentence) - self.base_x, 0))
        self.render().move(line, pillar)
