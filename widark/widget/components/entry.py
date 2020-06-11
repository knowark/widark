import curses
from typing import List, Tuple
from ..widget import Widget
from ..event import Event
from ..style import Style


class Entry(Widget):
    def setup(self, **context) -> 'Entry':
        self.canvas_content = context.pop('content', '')

        style: Style = context.pop('style', Style(border=[0]))
        return super().setup(**context, style=style) and self

    def build(self) -> None:
        self.canvas = Canvas(self, content=self.canvas_content)

    @property
    def text(self) -> str:
        return '\n'.join(self.canvas.buffer)


class Canvas(Widget):
    def setup(self, **context) -> 'Canvas':
        content = context.pop('content', '')

        self.buffer: List[str] = content.splitlines() or ['']
        self.base_y: int = 0
        self.base_x: int = 0

        self.listen('click', self.on_click)
        self.listen('keydown', self.on_keydown)
        return super().setup(**context) and self

    async def on_click(self, event: Event) -> None:
        origin_y, origin_x = self.window.getbegyx()
        y, x = event.y - origin_y,  event.x - origin_x
        line = self.base_y + y + 1
        self.move(min(y, len(self.buffer[:line]) - 1),
                  min(x, len(self.buffer[:line][-1])))

    def settle(self) -> None:
        origin = 1 if self.styling.border else 0
        height, width = self.size()
        height -= 2 * origin
        width -= 2 * origin

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
            self._character(event.data)

    def _right(self) -> None:
        _, width = self.size()
        y, x = self.cursor()
        sentence = self.buffer[self.base_y + y]
        pillar = x + 1
        if x >= width - 3 and len(sentence) - self.base_x - width >= 0:
            pillar = x
            max_shift = max(len(sentence) - width + 1, 0)
            self.base_x = min(self.base_x + 1, max_shift)
            self.render()
        self.move(y, min(pillar, max(len(sentence) - self.base_x, 0)))

    def _left(self) -> None:
        y, x = self.cursor()
        pillar = x - 1
        if x <= 1 and self.base_x != 0:
            pillar = x
            self.base_x = max(self.base_x - 1, 0)
            self.render()
        self.move(y,  max(pillar, 0))

    def _up(self) -> None:
        _, width = self.size()
        y, x = self.cursor()
        line = y - 1
        if y <= 1 and self.base_y != 0:
            line = y
            self.base_y = max(self.base_y - 1, 0)
        sentence = self.buffer[line + self.base_y]
        if x > len(sentence) - self.base_x:
            self.base_x = int(len(sentence) / width) * width
        pillar = min(x, max(len(sentence) - self.base_x, 0))
        self.render().move(line, pillar)

    def _down(self) -> None:
        height, width = self.size()
        y, x = self.cursor()
        line = y + 1
        if y >= height - 2 and len(self.buffer) - self.base_y - height >= 1:
            line = y
            max_shift = max(len(self.buffer) - height, 0)
            self.base_y = min(self.base_y + 1, max_shift)
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
        character = self.base_x + x
        if x == 1 and self.base_x != 0:
            pillar = x
            self.base_x = max(self.base_x - 1, 0)
        elif x == 0 and y > 0:
            row = self.buffer.pop(self.base_y + y)
            line = max(line - 1, 0)
            sentence = self.buffer[self.base_y + y - 1]
            self.base_x = int(len(sentence) / width) * width
            pillar = max(len(sentence) - self.base_x, 0)
            self.buffer[self.base_y + y - 1] += row

        self.buffer[self.base_y + line] = (
            self.buffer[self.base_y + line][:max(character - 1, 0)] +
            self.buffer[self.base_y + line][character:])

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
        self.base_x = 0
        self.buffer[self.base_y + y] = head
        self.buffer.insert(self.base_y + y + 1, tail)
        self.render().move(y + 1)

    def _character(self, data: str) -> None:
        y, x = self.cursor()
        _, width = self.size()

        insertion = data.splitlines()
        first = insertion and insertion.pop(0) or ''
        head = self.buffer[self.base_y + y][:self.base_x + x] + first
        tail = self.buffer[self.base_y + y][self.base_x + x:]

        line = min(self.base_y + y, len(self.buffer) - 1)
        self.buffer[self.base_y + y] = head + tail
        self.buffer[line + 1:line + 1] = insertion

        x += 1
        if x >= width - 2:
            self.base_x += 1
            x -= 1

        self.render().move(y, x)
