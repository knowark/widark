from typing import List, Optional


class Widget:
    def __init__(self, parent: Optional['Widget']) -> None:
        self.parent: Optional['Widget'] = parent
        self.children: List['Widget'] = []
        self.window = None
        self.content = ''
        self.row_sequence = 0
        self.column_sequence = 0
        self.row_weight = 1
        self.column_weight = 1

    def attach(self, row=0, column=0, width=0, height=0) -> 'Widget':
        if not self.parent:
            return self
        self.parent.children.append(self)
        factory = self.parent.window.derwin  # type: ignore
        self.window = factory(width, height, row, column)

        return self

    def update(self) -> 'Widget':
        if self.window:
            self.window.addstr(self.content)
            self.window.noutrefresh()
        return self

    def sequence(self, row=0, column=0) -> 'Widget':
        self.row_sequence = row
        self.column_sequence = column
        return self

    def weight(self, row=1, column=1) -> 'Widget':
        self.row_weight = row
        self.column_weight = column
        return self
