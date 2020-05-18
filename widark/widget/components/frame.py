from typing import Optional
from ..widget import Widget
from ..style import Style


class Frame(Widget):
    def __init__(self, parent: Optional['Widget'],
                 title: str = '',
                 title_align: str = 'C',
                 title_template: str = ' {} ') -> None:
        self.title = title
        self.title_align = title_align
        self.title_template = title_template
        style = Style(border=[0])
        super().__init__(parent, style=style)

    def settle(self) -> None:
        x = 0
        _, w = self.size()
        fill = len(self.title)
        origin, loss = (1, 2) if self._style.border else (0, 0)
        width = max(w - loss, 1)

        if self.title_align == 'C':
            x = int(max(width - fill, 0) / 2)
        elif self.title_align == 'R':
            x = max(width - fill, 0)

        title = self.title_template.format(self.title)
        self.window.addstr(0, x + origin, title)
