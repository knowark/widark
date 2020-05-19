from ..widget import Widget
from ..style import Style
from ..event import Handler


class Button(Widget):
    def __init__(self, parent: 'Widget', content: str = '',
                 command: Handler=None) -> None:
        style = Style('PRIMARY', align='C', template='< {} >')
        super().__init__(parent, content, style)
        if command:
            self.listen('click', command)
