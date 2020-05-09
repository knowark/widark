from typing import List, Optional


class Widget:
    def __init__(self, parent: Optional['Widget']) -> None:
        self.parent: Optional['Widget'] = parent
        self.children: List['Widget'] = []
        self.window = None
        self.content = ''
        self.row_sequence = 0
        self.column_sequence = 0

        if self.parent:
            self.parent.children.append(self)
            factory = parent.window.derwin  # type: ignore
            self.window = factory(1, 1, 0, 0)

    def sequence(self, row=0, column=0) -> 'Widget':
        self.row_sequence = row
        self.column_sequence = column
        return self
