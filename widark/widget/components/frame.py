from ..widget import Widget
from ..style import Style


class Frame(Widget):
    def __init__(self, parent: 'Widget',
                 title: str = '',
                 title_style: Style = None,
                 style: Style = None) -> None:
        self.title = title
        self._title_style = (
            title_style or Style(align='C', template=' {} '))
        super().__init__(parent, style=style or Style(border=[0]))

    def title_style(self, *args, **kwargs) -> 'Frame':
        self._title_style.configure(*args, **kwargs)
        return self

    def amend(self) -> None:
        x = 0
        _, w = self.size()
        fill = len(self.title)
        origin, loss = (1, 2) if self._style.border else (0, 0)
        width = max(w - loss, 1)

        if self._title_style.align == 'C':
            x = int(max(width - fill, 0) / 2)
        elif self._title_style.align == 'R':
            x = max(width - fill, 0)

        title = (self.title and
                 self._title_style.template.format(self.title) or '')
        self.window.addstr(0, x + origin, title, self._title_style.color)
