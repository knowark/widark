from typing import List, Dict, Optional, Tuple, Any


class Widget:
    def __init__(self, parent: Optional['Widget']) -> None:
        self.parent: Optional['Widget'] = parent
        self.children: List['Widget'] = []
        self.window: Any = None
        self.border: List[int] = []
        self.content = ''
        self.row = 0
        self.col = 0
        self.row_span = 1
        self.col_span = 1
        self.row_weight = 1
        self.col_weight = 1

        if self.parent:
            self.parent.children.append(self)

    def attach(self, row=0, col=0, height=0, width=0) -> 'Widget':
        if not self.window:
            factory = self.parent.window.derwin  # type: ignore
            self.window = factory(height, width, row, col)

        if self.window and self.border:
            self.window.border(*[])

        for child, dimensions in self.layout():
            child.attach(**dimensions).update()

        return self.update()

    def update(self) -> 'Widget':
        if self.window:
            origin = 1 if self.border else 0
            self.window.move(origin, origin)
            self.window.addstr(self.content)
            self.window.noutrefresh()
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
        height, width = self.window.getmaxyx()
        if self.border:
            row_origin, col_origin = 1, 1
            height, width = height - 2, width - 2

        cols: Dict[int, int] = {}
        rows: Dict[int, int] = {}
        for child in self.children:
            col_weight = cols.setdefault(child.col, 1)
            cols[child.col] = max([col_weight, child.col_weight])

            row_weight = rows.setdefault(child.row, 1)
            rows[child.row] = max([row_weight, child.row_weight])

        width_split = width / sum(cols.values())
        height_split = height / sum(rows.values())

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

            dimensions = {
                'row': int(
                    row_origin +
                    sum(row_weights[y] for y in
                        range(row_index)) * height_split),
                'col': int(
                    col_origin +
                    sum(col_weights[x] for x in
                        range(col_index)) * width_split),
                'height': int(
                    sum(row_weights.get(y, 0) for y in
                        range(row_index, row_span)) * height_split),
                'width': int(
                    sum(col_weights.get(x, 0) for x in
                        range(col_index, col_span)) * width_split)
            }

            layout.append((child, dimensions))

        return layout
