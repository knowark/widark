from typing import List, Dict, Optional, Tuple


class Widget:
    def __init__(self, parent: Optional['Widget']) -> None:
        self.parent: Optional['Widget'] = parent
        self.children: List['Widget'] = []
        self.window = None
        self.content = ''
        self.row = 0
        self.column = 0
        self.height_weight = 1
        self.width_weight = 1

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

    def weight(self, width=1, height=1) -> 'Widget':
        self.width_weight = width
        self.height_weight = height
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
            columns[child.column] = max([column_weight, child.width_weight])

            row_weight = rows.setdefault(child.row, 1)
            rows[child.row] = max([row_weight, child.height_weight])

        width_split = int(width / sum(columns.values()))
        height_split = int(height / sum(rows.values()))

        layout = []
        for i, column in enumerate(sorted(columns.keys())):
            for j, row in enumerate(sorted(rows.keys())):
                column_width = width_split * columns[column]
                row_height = height_split * rows[row]
                cell_children = children.get((row, column), [])

                for cell_child in cell_children:
                    layout.append((cell_child, {
                        'row': j * row_height,
                        'column': i * column_width,
                        'width': column_width,
                        'height': row_height
                    }))

        return layout
