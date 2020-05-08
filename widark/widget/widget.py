from typing import List, Optional


class Widget:
    def __init__(self, parent: Optional['Widget']) -> None:
        self.parent: Optional['Widget'] = parent
        self.children: List['Widget'] = []
        self.window = None

        if self.parent:
            factory = parent.window.derwin  # type: ignore
            self.window = factory(1, 1, 0, 0)
