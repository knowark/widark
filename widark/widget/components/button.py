from typing import Optional
from ..widget import Widget
from ..style import Style
from ..event import Handler


class Button(Widget):
    def __init__(self, parent: Optional['Widget'], text: str = '',
                 command: Handler=None, style: Style = None) -> None:
        self.text = text
        self.template = '< {} >'
        self.command = command
        super().__init__(parent, self.template.format(self.text), style)
        if self.command:
            self.listen('click', self.command)
