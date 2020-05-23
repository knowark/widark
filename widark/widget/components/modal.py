from curses import color_pair, A_REVERSE, A_INVIS, A_DIM
from ..style import Color
from ..event import Event, Handler
from ..widget import Widget


class Modal(Widget):
    def __init__(self, parent: 'Widget',
                 close_command: Handler = None) -> None:
        super().__init__(parent)
        self.position = 'fixed'
        self.body = Widget(self).style(border=[0])
        self.body.position = 'fixed'
        self.listen('click', self.on_backdrop)
        if close_command:
            self.listen('close', close_command)

    def launch(self, row=0, col=0, height=0, width=0) -> 'Modal':
        self.parent and self.parent.add(self, 0)
        super().attach()
        self.body.attach(row, col, height, width)
        return self

    async def on_backdrop(self, event: Event) -> None:
        if not self.body.hit(event):
            await self.dispatch(Event('Custom', 'close'))

    def attach(self, row=0, col=0, height=0, width=0) -> 'Modal':
        super().attach()
        self.body.attach(*self.body.beginning(), *self.body.size())
        return self
