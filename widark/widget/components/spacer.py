from typing import Optional
from ..widget import Widget
from ..style import Style


class Spacer(Widget):
    def __init__(self, parent: Optional['Widget']) -> None:
        super().__init__(parent)
