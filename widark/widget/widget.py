from math import ceil
from types import SimpleNamespace
from typing import List, Dict, Optional, Tuple, Any, TypeVar
from curses import setsyx
from _curses import error as CursesError
from .event import Target
from .style import Style


T = TypeVar('T', bound='Widget')


class Widget(Target):
    def __init__(self, parent: Optional['Widget'],
                 content: str = '', style: Style = None,
                 position: str = 'relative') -> None:
        super().__init__()
        self.parent: Optional['Widget'] = parent
        self.content = content
        self.children: List['Widget'] = []
        self.window: Any = None
        self.position = position
        self.styling = style or Style()
        self.focused = False
        self.y = 0
        self.x = 0
        self.width = 0
        self.height = 0
        self.row = SimpleNamespace(
            pos=0, span=1, weight=1)
        self.col = SimpleNamespace(
            pos=0, span=1, weight=1)

        if self.parent:
            self.parent.children.append(self)

        self.setup()

    def setup(self) -> None:
        """Custom setup"""

    def attach(self: T, y=0, x=0, height=0, width=0) -> T:
        if self.parent:
            try:
                factory = self.parent.window.derwin
                self.window = factory(height, width, y, x)
                h, w = self.window.getmaxyx()
                self.pin(y, x, h, w)
                self._y_min, self._x_min = self.window.getbegyx()
                self._y_max, self._x_max = self._y_min + h, self._x_min + w
            except CursesError:
                return self

        relative_children, fixed_children = self.subtree()

        for child, dimensions in self.layout(relative_children):
            child.attach(**dimensions)

        for child in fixed_children:
            if child.height and child.width:
                child.attach(child.y, child.x, child.height, child.width)

        return self.update()

    def subtree(self) -> Tuple[List['Widget'], List['Widget']]:
        fixed_children = []
        relative_children = []
        for child in self.children:
            if child.position == 'fixed':
                fixed_children.append(child)
            else:
                relative_children.append(child)

        return relative_children, fixed_children

    def add(self: T, child: 'Widget', index: int = None) -> T:
        if child.parent:
            child.parent.children.remove(child)
        child.parent = self
        index = len(self.children) if index is None else index
        self.children.insert(index, child)
        return self

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
        return self

    def update(self: T, content: str = None) -> T:
        if not self.window:
            return self

        if content is not None:
            self.content = content

        try:
            self.settle()

            self.window.clear()

            self.window.bkgd(' ', self.styling.background_color)

            if self.styling.border:
                self.window.bkgdset(' ', self.styling.border_color)
                self.window.border(*self.styling.border)

            y, x = self.place()
            formatted_content = self.styling.template.format(self.content)

            self.window.bkgdset(' ', self.styling.color)
            self.window.addstr(y, x, formatted_content, self.styling.color)

            relative_children, fixed_children = self.subtree()

            for child in relative_children:
                child.update()

            for child in fixed_children:
                child.update()

            self.amend()

            self.window.noutrefresh()
        except CursesError:
            pass

        return self

    def settle(self) -> None:
        """Custom settlement"""

    def amend(self) -> None:
        """Custom amendment"""

    def style(self: T, *args, **kwargs) -> T:
        self.styling.configure(*args, **kwargs)
        return self

    def pin(self: T, y=0, x=0, height=0, width=0) -> T:
        self.y, self.x = y, x
        self.height, self.width = height, width
        return self

    def grid(self: T, row=0, col=0) -> T:
        self.row.pos, self.col.pos = row, col
        return self

    def span(self: T, row=1, col=1) -> T:
        self.row.span, self.col.span = row, col
        return self

    def weight(self: T, row=1, col=1) -> T:
        self.row.weight, self.col.weight = row, col
        return self

    def focus(self: T) -> T:
        if not self.window:
            return self
        origin = 1 if self.styling.border else 0
        y, x = self.window.getbegyx()
        setsyx(y + origin, x + origin)
        self.focused = True
        return self

    def blur(self: T) -> T:
        self.focused = False
        return self

    def place(self) -> Tuple[int, int]:
        y, x = 0, 0
        h, w = self.height, self.width
        origin, loss = (1, 2) if self.styling.border else (0, 0)
        height, width = max(h - loss, 1), max(w - loss, 1)
        fill = len(self.styling.template.format(self.content))
        vertical, horizontal = (
            (3 - len(self.styling.align)) * self.styling.align)

        if vertical == 'C':
            y = int(max(height - ceil(fill / width), 0) / 2)
        elif vertical == 'R':
            y = max(height - ceil(fill / width), 0)

        if horizontal == 'C':
            x = int(max(width - fill, 0) / 2)
        elif horizontal == 'R':
            x = max(width - fill, 0)

        return y + origin, x + origin

    def layout(self, children: List['Widget']
               ) -> List[Tuple['Widget', Dict[str, int]]]:
        if not self.window or not children:
            return []

        row_origin, col_origin = 0, 0
        total_height, total_width = self.window.getmaxyx()
        if self.styling.border:
            row_origin, col_origin = 1, 1
            total_height, total_width = total_height - 2, total_width - 2

        cols: Dict[int, int] = {}
        rows: Dict[int, int] = {}
        for child in children:
            col_weight = cols.setdefault(child.col.pos, 1)
            cols[child.col.pos] = max([col_weight, child.col.weight])

            row_weight = rows.setdefault(child.row.pos, 1)
            rows[child.row.pos] = max([row_weight, child.row.weight])

        width_split = total_width / sum(cols.values())
        height_split = total_height / sum(rows.values())

        row_indexes, row_weights = {}, {}
        for j, (y, row_weight) in enumerate(rows.items()):
            row_indexes[y] = j
            row_weights[j] = row_weight

        col_indexes, col_weights = {}, {}
        for i, (x, col_weight) in enumerate(cols.items()):
            col_indexes[x] = i
            col_weights[i] = col_weight

        layout = []
        for child in children:
            row_index = row_indexes[child.row.pos]
            row_span = row_index + child.row.span
            col_index = col_indexes[child.col.pos]
            col_span = col_index + child.col.span

            y = sum(ceil(row_weights[j] * height_split) for j in
                    range(row_index)) + row_origin
            x = sum(ceil(col_weights[i] * width_split) for i in
                    range(col_index)) + col_origin

            height = ceil(
                sum(row_weights.get(j, 0) for j in
                    range(row_index, row_span)) * height_split)
            height = height - max(0, height + y - total_height - row_origin)

            width = ceil(
                sum(col_weights.get(i, 0) for i in
                    range(col_index, col_span)) * width_split)
            width = width - max(0, width + x - total_width - col_origin)

            layout.append((child, {'y': y, 'x': x,
                                   'height': height, 'width': width}))

        return layout
