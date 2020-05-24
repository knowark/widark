from ..widget import Widget
from ..style import Style


class Frame(Widget):
    def __init__(self, parent: 'Widget',
                 title: str = '',
                 title_style: Style = None,
                 style: Style = None) -> None:
        self.title = title
        self.title_styling = (
            title_style or Style(align='C', template=' {} '))
        super().__init__(parent, style=style or Style(border=[0]))

    def title_style(self, *args, **kwargs) -> 'Frame':
        self.title_styling.configure(*args, **kwargs)
        return self

    def amend(self) -> None:
        x = 0
        fill = len(self.title)
        origin, loss = (1, 2) if self.styling.border else (0, 0)
        width = max(self.width - loss, 1)

        if self.title_styling.align == 'C':
            x = int(max(width - fill, 0) / 2)
        elif self.title_styling.align == 'R':
            x = max(width - fill, 0)

        title = (self.title and
                 self.title_styling.template.format(self.title) or '')
        self.window.addstr(0, x + origin, title, self.title_styling.color)
