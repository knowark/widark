from math import ceil
from typing import List, Dict, Optional, Tuple, Any, TypeVar
from _curses import error as CursesError
from curses import color_pair, setsyx
from .event import Target
from .style import Style, Color


T = TypeVar('T', bound='Widget')


class Widget(Target):
    def __init__(self, parent: Optional['Widget'],
                 content: str = '', style: Style = None) -> None:
        super().__init__()
        self.parent: Optional['Widget'] = parent
        self.content = content
        self.children: List['Widget'] = []
        self.window: Any = None
        self._style = style or Style()
        self._focused = False
        self._row = 0
        self._col = 0
        self._row_span = 1
        self._col_span = 1
        self._row_weight = 1
        self._col_weight = 1

        if self.parent:
            self.parent.children.append(self)

        self.setup()

    def setup(self) -> None:
        """Custom setup"""

    def attach(self: T, row=0, col=0, height=0, width=0) -> T:
        if self.parent:
            factory = self.parent.window.derwin  # type: ignore
            try:
                self.window = factory(height, width, row, col)
                h, w = self.size()
                self._y_min, self._x_min = self.window.getbegyx()
                self._y_max, self._x_max = self._y_min + h, self._x_min + w
            except CursesError:
                return self

        for child, dimensions in self.layout():
            child.attach(**dimensions).update()

        return self.update()

    def add(self: T, child: 'Widget', index: int = None) -> T:
        if child not in self.children:
            child.parent = self
            index = index or len(self.children)
            self.children.insert(index, child)
            self.clear()
            origin = 1 if self._style.border else 0
            self.attach(origin, origin, *self.size())
        return self

    def settle(self) -> None:
        """Custom settlement"""

    def move(self: T, row=0, col=0) -> T:
        if self.window:
            height, width = self.window.getmaxyx()
            self.window.move(min(row, height - 1), min(col, width - 1))
            self.window.noutrefresh()
        return self

    def clear(self: T) -> T:
        if self.window:
            self.window.clear()
            self.window.noutrefresh()
        return self

    def remove(self: T, child: 'Widget') -> T:
        if child in self.children:
            child.parent, child.window = None, None
            self.children.remove(child)
            self.clear()
            origin = 1 if self._style.border else 0
            self.attach(origin, origin, *self.size())
        return self

    def update(self: T, content: str = None) -> T:
        if not self.window:
            return self
        if content is not None:
            self.content = content

        try:
            self.settle()

            if self._style.border:
                self.window.attrset(color_pair(
                    Color[self._style.border_color]))
                self.window.border(*self._style.border)

            y, x = self.place()
            formatted_content = self._style.template.format(self.content)
            color = color_pair(Color[self._style.color])
            self.window.addstr(y, x, formatted_content, color)

            self.amend()
            self.window.noutrefresh()
        except CursesError:
            pass

        return self

    def amend(self) -> None:
        """Custom amendment"""

    def size(self) -> Tuple[int, int]:
        return self.window.getmaxyx() if self.window else (0, 0)

    def style(self: T, *args, **kwargs) -> T:
        self._style.configure(*args, **kwargs)
        return self

    def grid(self: T, row=0, col=0) -> T:
        self._row, self._col = row, col
        return self

    def span(self: T, row=1, col=1) -> T:
        self._row_span, self._col_span = row, col
        return self

    def weight(self: T, row=1, col=1) -> T:
        self._row_weight, self._col_weight = row, col
        return self

    def focus(self: T) -> T:
        if not self.window:
            return self
        origin = 1 if self._style.border else 0
        y, x = self.window.getbegyx()
        setsyx(y + origin, x + origin)
        self._focused = True
        return self

    def blur(self: T) -> T:
        self._focused = False
        return self

    def place(self) -> Tuple[int, int]:
        y, x = 0, 0
        h, w = self.size()
        origin, loss = (1, 2) if self._style.border else (0, 0)
        height, width = max(h - loss, 1), max(w - loss, 1)
        fill = len(self._style.template.format(self.content))
        vertical, horizontal = (
            (3 - len(self._style.align)) * self._style.align)

        if vertical == 'C':
            y = int(max(height - ceil(fill / width), 0) / 2)
        elif vertical == 'R':
            y = max(height - ceil(fill / width), 0)

        if horizontal == 'C':
            x = int(max(width - fill, 0) / 2)
        elif horizontal == 'R':
            x = max(width - fill, 0)

        return y + origin, x + origin

    def layout(self) -> List[Tuple['Widget', Dict[str, int]]]:
        if not self.window or not self.children:
            return []

        row_origin, col_origin = 0, 0
        total_height, total_width = self.window.getmaxyx()
        if self._style.border:
            row_origin, col_origin = 1, 1
            total_height, total_width = total_height - 2, total_width - 2

        cols: Dict[int, int] = {}
        rows: Dict[int, int] = {}
        for child in self.children:
            col_weight = cols.setdefault(child._col, 1)
            cols[child._col] = max([col_weight, child._col_weight])

            row_weight = rows.setdefault(child._row, 1)
            rows[child._row] = max([row_weight, child._row_weight])

        width_split = total_width / sum(cols.values())
        height_split = total_height / sum(rows.values())

        row_indexes, row_weights = {}, {}
        for y, (row, row_weight) in enumerate(rows.items()):
            row_indexes[row] = y
            row_weights[y] = row_weight

        col_indexes, col_weights = {}, {}
        for x, (col, col_weight) in enumerate(cols.items()):
            col_indexes[col] = x
            col_weights[x] = col_weight

        layout = []
        for child in self.children:
            row_index = row_indexes[child._row]
            row_span = row_index + child._row_span
            col_index = col_indexes[child._col]
            col_span = col_index + child._col_span

            row = sum(ceil(row_weights[y] * height_split) for y in
                      range(row_index)) + row_origin
            col = sum(ceil(col_weights[x] * width_split) for x in
                      range(col_index)) + col_origin

            height = ceil(
                sum(row_weights.get(y, 0) for y in
                    range(row_index, row_span)) * height_split)
            height = height - max(0, height + row - total_height - row_origin)

            width = ceil(
                sum(col_weights.get(x, 0) for x in
                    range(col_index, col_span)) * width_split)
            width = width - max(0, width + col - total_width - col_origin)

            layout.append((child, {'row': row, 'col': col,
                                   'height': height, 'width': width}))

        return layout
