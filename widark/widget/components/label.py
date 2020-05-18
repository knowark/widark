from typing import Optional
from ..widget import Widget
from ..style import Style
from ..event import Handler


class Label(Widget):
    def __init__(self, parent: Optional['Widget'], content: str = '') -> None:
        style = Style('INFO', align='C')
        super().__init__(parent, content, style)
