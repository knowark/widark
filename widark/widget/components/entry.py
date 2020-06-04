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
            if x == 0:
                self.base_x = max(self.base_x - 1, 0)
                self.render()
            pillar = max(x - 1, 0)
            self.move(y, pillar)
            return
        elif ord(event.key) == curses.KEY_RIGHT:
            if x == width - 1:
                max_shift = max(len(self.buffer[self.base_y + y]) - width, 0)
                self.base_x = min(self.base_x + 1, max_shift)
                self.render()
            pillar = min(x + 1, len(self.buffer[self.base_y + y]))
            self.move(y, pillar)
            return
        elif ord(event.key) == curses.KEY_UP:
            if y == 0:
                self.base_y = max(self.base_y - 1, 0)
                self.render()
            line = max(y - 1, 0)
            self.move(line, min(x, len(self.buffer[line + self.base_y])))
            return
        elif ord(event.key) == curses.KEY_DOWN:
            if y == height - 1:
                max_shift = max(len(self.buffer) - height, 0)
                self.base_y = min(self.base_y + 1, max_shift)
                self.render()
            line = min(y + 1, height - 1)
            self.move(line, min(x, len(self.buffer[line + self.base_y])))
            return
        elif ord(event.key) == curses.KEY_BACKSPACE:
            if x == 0:
                row = self.buffer.pop(y)
                y = max(y - 1, 0)
                x = len(self.buffer[y]) + 1
                self.buffer[y] += row
            self.buffer[y] = (
                self.buffer[y][:max(x - 1, 0)] + self.buffer[y][x:])
            self.content = "\n".join(self.buffer)
            self.render().move(y, x - 1)
        elif ord(event.key) == curses.KEY_DC:
            if x == len(self.buffer[y]) and y < len(self.buffer) - 1:
                row = self.buffer.pop(y + 1)
                self.buffer[y] += row
            self.buffer[y] = (
                self.buffer[y][:max(x, 0)] + self.buffer[y][x + 1:])
            self.content = "\n".join(self.buffer)
            self.render().move(y, x)
        else:
            self.buffer[self.base_y + y] = (
                self.buffer[self.base_y + y][:x] + event.key +
                self.buffer[self.base_y + y][x:])
            x += 1
            if event.key == '\n':
                y, x = y + 1, 0
                if y == len(self.buffer):
                    self.buffer.append('')
            self.content = "\n".join(self.buffer)
            self.render().move(y, x)
