from typing import List, Dict, Optional, Tuple


class Widget:
    def __init__(self, parent: Optional['Widget']) -> None:
        self.parent: Optional['Widget'] = parent
        self.children: List['Widget'] = []
        self.window = None
        self.content = ''
        self.row = 0
        self.column = 0
        self.row_span = 1
        self.column_span = 1
        self.row_weight = 1
        self.column_weight = 1

        if self.parent:
            self.parent.children.append(self)

    def attach(self, y=0, x=0, height=0, width=0) -> 'Widget':
        if not self.parent:
            return self
        factory = self.parent.window.derwin  # type: ignore
        self.window = factory(height, width, y, x)

        for child in self.children:
            child.attach().update()

        return self

    def update(self) -> 'Widget':
        if self.window:
            self.window.addstr(self.content)
            self.window.noutrefresh()
        return self

    def sequence(self, row=0, column=0) -> 'Widget':
        self.row = row
        self.column = column
        return self

    def span(self, row=1, column=1) -> 'Widget':
        self.row_span = row
        self.column_span = column
        return self

    def weight(self, row=1, column=1) -> 'Widget':
        self.row_weight = row
        self.column_weight = column
        return self

    def layout(self) -> List[Tuple['Widget', Dict[str, int]]]:
        if not self.window or not self.children:
            return []

        height, width = self.window.getmaxyx()

        children, columns, rows = {}, {}, {}
        for child in self.children:
            children.setdefault((child.row, child.column), [])
            children[(child.row, child.column)].append(child)

            column_weight = columns.setdefault(child.column, 1)
            columns[child.column] = max([column_weight, child.column_weight])

            row_weight = rows.setdefault(child.row, 1)
            rows[child.row] = max([row_weight, child.row_weight])

        width_split = width / sum(columns.values())
        height_split = height / sum(rows.values())

        row_indexes, row_weights = {}, {}
        for y, (row, row_weight) in enumerate(rows.items()):
            row_indexes[row] = y
            row_weights[y] = row_weight

        column_indexes, column_weights = {}, {}
        for x, (column, column_weight) in enumerate(columns.items()):
            column_indexes[column] = x
            column_weights[x] = column_weight

        layout = []
        for child in self.children:
            row_index = row_indexes[child.row]
            row_span = row_index + child.row_span
            column_index = column_indexes[child.column]
            column_span = column_index + child.column_span

            dimensions = {
                'row': int(
                    sum(row_weights[y] for y in
                        range(row_index)) * height_split),
                'column': int(
                    sum(column_weights[x] for x in
                        range(column_index)) * width_split),
                'height': int(
                    sum(row_weights.get(y, 0) for y in
                        range(row_index, row_span)) * height_split),
                'width': int(
                    sum(column_weights.get(x, 0) for x in
                        range(column_index, column_span)) * width_split)
            }

            layout.append((child, dimensions))

        return layout
