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

    def settle(self) -> None:
        height, width = self.size()

        content = ''
        for line in self.buffer[self.base_y: height + self.base_y]:
            sentence = line[self.base_x: width - 1 + self.base_x]
            content += f'{sentence}\n'

        self.content = content

    async def on_keydown(self, event: Event) -> None:
        if ord(event.key) == curses.KEY_LEFT:
            self._left()
        elif ord(event.key) == curses.KEY_RIGHT:
            self._right()
        elif ord(event.key) == curses.KEY_UP:
            self._up()
        elif ord(event.key) == curses.KEY_DOWN:
            self._down()
        elif ord(event.key) == curses.KEY_BACKSPACE:
            self._backspace()
        elif ord(event.key) == curses.KEY_DC:
            self._delete()
        elif event.key == '\n':
            self._enter()
        else:
            self._character(event.key)

    def _right(self) -> None:
        _, width = self.size()
        y, x = self.cursor()
        sentence = self.buffer[self.base_y + y]
        if x == width - 1:
            max_shift = max(len(sentence) - width + 1, 0)
            self.base_x = min(self.base_x + 1, max_shift)
            self.render()
        self.move(y, min(x + 1, max(len(sentence) - self.base_x, 0)))

    def _left(self) -> None:
        y, x = self.cursor()
        if x == 0:
            self.base_x = max(self.base_x - 1, 0)
            self.render()
        self.move(y,  max(x - 1, 0))

    def _up(self) -> None:
        _, width = self.size()
        y, x = self.cursor()
        if y == 0:
            self.base_y = max(self.base_y - 1, 0)
        line = max(y - 1, 0)
        sentence = self.buffer[line + self.base_y]
        if x > len(sentence) - self.base_x:
            self.base_x = int(len(sentence) / width) * width
        pillar = min(x, max(len(sentence) - self.base_x, 0))
        self.render().move(line, pillar)

    def _down(self) -> None:
        height, width = self.size()
        y, x = self.cursor()
        if y == height - 1:
            max_shift = max(len(self.buffer) - height, 0)
            self.base_y = min(self.base_y + 1, max_shift)
        line = min(y + 1, height - 1)
        if line + self.base_y >= len(self.buffer):
            return
        sentence = self.buffer[line + self.base_y]
        if x > len(sentence) - self.base_x:
            self.base_x = int(len(sentence) / width) * width
        pillar = min(x, max(len(sentence) - self.base_x, 0))
        self.render().move(line, pillar)

    def _backspace(self) -> None:
        _, width = self.size()
        y, x = self.cursor()
        line = y
        pillar = max(x - 1, 0)
        if x == 0 and y > 0:
            row = self.buffer.pop(self.base_y + y)
            line = max(line - 1, 0)
            sentence = self.buffer[self.base_y + y - 1]
            self.base_x = int(len(sentence) / width) * width
            pillar = max(len(sentence) - self.base_x, 0)
            self.buffer[self.base_y + y - 1] += row

        self.buffer[self.base_y + y] = (
            self.buffer[self.base_y + y][:max(self.base_x + x - 1, 0)] +
            self.buffer[self.base_y + y][self.base_x + x:])

        self.render().move(line, pillar)

    def _delete(self) -> None:
        y, x = self.cursor()
        sentence = self.buffer[self.base_y + y]
        if (self.base_x + x == len(sentence) and
                (self.base_y + y) < len(self.buffer) - 1):
            row = self.buffer.pop(self.base_y + y + 1)
            self.buffer[self.base_y + y] += row
        else:
            self.buffer[self.base_y + y] = (
                sentence[:self.base_x + x] +
                sentence[self.base_x + x + 1:])
        self.render().move(y, x)

    def _enter(self) -> None:
        y, x = self.cursor()
        head, tail = (
            self.buffer[self.base_y + y][:self.base_x + x],
            self.buffer[self.base_y + y][self.base_x + x:])
        self.buffer[self.base_y + y] = head
        self.buffer.insert(self.base_y + y + 1, tail)
        self.render().move(y + 1)

    def _character(self, character: str) -> None:
        y, x = self.cursor()
        self.buffer[self.base_y + y] = (
            self.buffer[self.base_y + y][:self.base_x + x] +
            character +
            self.buffer[self.base_y + y][self.base_x + x:])
        self.render().move(y, x + 1)
