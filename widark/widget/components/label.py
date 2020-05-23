from ..widget import Widget
from ..style import Style, Color


class Label(Widget):
    def __init__(self, parent: 'Widget', content: str = '') -> None:
        style = Style(Color.INFO(), align='C')
        super().__init__(parent, content, style)
