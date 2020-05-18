from typing import Optional
from ..widget import Widget
from ..style import Style
from ..event import Handler


class Button(Widget):
    def __init__(self, parent: Optional['Widget'], content: str = '',
                 command: Handler=None, style: Style = None) -> None:
        style = style or Style('PRIMARY', align='C', template='< {} >')
        super().__init__(parent, content, style)
        if command:
            self.listen('click', command)
