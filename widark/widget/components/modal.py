from ..style import Color
from ..event import Handler
from ..widget import Widget


class Modal(Widget):
    def __init__(self, parent: 'Widget',
                 close_command: Handler = None) -> None:
        super().__init__(parent, position='fixed')
        self.style(background_color=Color.WARNING.reverse(), border=[' ']*8)
        self.close = Widget(self, 'X', position='fixed').style(Color.DANGER())

        if close_command:
            self.close.listen('click', close_command)

    def launch(self, row=0, col=0, height=0, width=0) -> 'Modal':
        self.parent and self.parent.add(self, 0)
        self.attach(row, col, height, width)
        self.close.attach(0, self.width - 2, 1, 2)
        return self
