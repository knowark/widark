from typing import Optional
from ..widget import Widget, Style


class Modal(Widget):
    def __init__(self, parent: 'Widget') -> None:
        super().__init__(parent)
        self.style(border=[ord('+') for i in range(8)])
        self.position = 'fixed'
        self.body: Optional[Widget] = None

    def amend(self) -> None:
        self.panel.top()
