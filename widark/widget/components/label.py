from ..widget import Widget
from ..style import Style


class Label(Widget):
    def __init__(self, parent: 'Widget', content: str = '') -> None:
        style = Style('INFO', align='C')
        super().__init__(parent, content, style)
