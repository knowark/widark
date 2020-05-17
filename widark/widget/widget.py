from typing import List, Dict, Optional, Tuple, Any
from _curses import error as CursesError
from curses import color_pair
from math import ceil
from .color import Color
from .event import Target


class Widget(Target):
    def __init__(self, parent: Optional['Widget'],
                 content: str = '', border: List[int] = None,
                 color: Color = Color.DEFAULT) -> None:
        super().__init__()
        self.parent: Optional['Widget'] = parent
        self.content = content
        self.border: List[int] = border or []
        self.color = color
        self.window: Any = None
        self.children: List['Widget'] = []
        self.row = 0
        self.col = 0
        self.row_span = 1
        self.col_span = 1
        self.row_weight = 1
        self.col_weight = 1

        if self.parent:
            self.parent.children.append(self)

        self.setup()

    def setup(self) -> None:
        """Custom setup"""

    def attach(self, row=0, col=0, height=0, width=0) -> 'Widget':
        if self.parent:
            factory = self.parent.window.derwin  # type: ignore
            try:
                self.window = factory(height, width, row, col)
                h, w = self.window.getmaxyx()
                self.y_min, self.x_min = self.window.getbegyx()
                self.y_max, self.x_max = self.y_min + h, self.x_min + w
            except CursesError:
                return self

        if self.window and self.border:
            self.window.border(*self.border)

        for child, dimensions in self.layout():
            child.attach(**dimensions).update()

        return self.update()

    def update(self) -> 'Widget':
        if not self.window:
            return self

        try:
            origin = 1 if self.border else 0
            self.window.addstr(
                origin, origin, self.content, color_pair(self.color))
            self.window.noutrefresh()
        except CursesError:
            pass

        return self

    def grid(self, row=0, col=0) -> 'Widget':
        self.row = row
        self.col = col
        return self

    def span(self, row=1, col=1) -> 'Widget':
        self.row_span = row
        self.col_span = col
        return self

    def weight(self, row=1, col=1) -> 'Widget':
        self.row_weight = row
        self.col_weight = col
        return self

    def layout(self) -> List[Tuple['Widget', Dict[str, int]]]:
        if not self.window or not self.children:
            return []

        row_origin, col_origin = 0, 0
        total_height, total_width = self.window.getmaxyx()
        if self.border:
            row_origin, col_origin = 1, 1
            total_height, total_width = total_height - 2, total_width - 2

        cols: Dict[int, int] = {}
        rows: Dict[int, int] = {}
        for child in self.children:
            col_weight = cols.setdefault(child.col, 1)
            cols[child.col] = max([col_weight, child.col_weight])

            row_weight = rows.setdefault(child.row, 1)
            rows[child.row] = max([row_weight, child.row_weight])

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
            row_index = row_indexes[child.row]
            row_span = row_index + child.row_span
            col_index = col_indexes[child.col]
            col_span = col_index + child.col_span

            row = ceil(
                row_origin +
                sum(row_weights[y] for y in
                    range(row_index)) * height_split)
            col = ceil(
                col_origin +
                sum(col_weights[x] for x in
                    range(col_index)) * width_split)

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
