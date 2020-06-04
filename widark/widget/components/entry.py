import curses
from math import ceil, floor
from ..widget import Widget
from ..event import Event
from ..style import Style


class Entry(Widget):
    def setup(self, **context) -> 'Entry':
        self.canvas_content: str = context.pop(
            'content', getattr(self, 'canvas_content', ''))

        style: Style = context.pop('style', Style(border=[0]))
        return super().setup(**context, style=style) and self

    def build(self) -> None:
        self.canvas = Canvas(self, content=self.canvas_content)


class Canvas(Widget):
    def setup(self, **context) -> 'Canvas':
        self.listen('click', self.on_click)
        self.listen('keydown', self.on_keydown)
        return super().setup(**context) and self

    async def on_click(self, event: Event) -> None:
        event.stop = True
        self.focus()

    def focus(self) -> 'Canvas':
        super().focus()
        matrix = (self.content or ' ').splitlines()
        self.move(len(matrix) - 1, len(matrix[-1]))
        return self

    async def on_keydown(self, event: Event) -> None:
        y, x = self.cursor()
        matrix = (self.content or ' ').splitlines()
        if ord(event.key) == curses.KEY_LEFT:
            self.move(y, x - 1)
            return
        elif ord(event.key) == curses.KEY_RIGHT:
            self.move(y, min(x + 1, len(matrix[y])))
            return
        elif ord(event.key) == curses.KEY_UP:
            line = max(y - 1, 0)
            self.move(line, min(x, len(matrix[line])))
            return
        elif ord(event.key) == curses.KEY_DOWN:
            line = min(y + 1, len(matrix) - 1)
            self.move(line, min(x, len(matrix[line])))
            return
        elif ord(event.key) == curses.KEY_BACKSPACE:
            if x == 0:
                row = matrix.pop(y)
                y = max(y - 1, 0)
                x = len(matrix[y]) + 1
                matrix[y] += row
            matrix[y] = matrix[y][:max(x - 1, 0)] + matrix[y][x:]
            self.content = "\n".join(matrix)
            self.render().move(y, x - 1)
        elif ord(event.key) == curses.KEY_DC:
            if x == len(matrix[y]) and y < len(matrix) - 1:
                row = matrix.pop(y + 1)
                matrix[y] += row
            matrix[y] = matrix[y][:max(x, 0)] + matrix[y][x + 1:]
            self.content = "\n".join(matrix)
            self.render().move(y, x)
        else:
            matrix[y] = matrix[y][:x] + event.key + matrix[y][x:]
            x += 1
            if event.key == '\n':
                y, x = y + 1, 0
                if y == len(matrix):
                    matrix.append('')
            self.content = "\n".join(matrix)
            self.render().move(y, x)
