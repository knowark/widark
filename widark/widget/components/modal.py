from ..style import Style, Color
from ..event import Handler
from ..widget import Widget


class Modal(Widget):
    def setup(self, **context) -> 'Modal':
        self.close_command = context.pop(
            'close_command', getattr(self, 'close_command', None))

        style = context.pop('style', Style(
            background_color=Color.WARNING.reverse(), border=[0]))
        return super().setup(
            **context, style=style, position='fixed') and self

    def build(self) -> None:
        self.close = Widget(
            self, content='X', position='fixed').style(
                Color.DANGER()).listen('click', self.close_command)

    def launch(self, row=0, col=0, height=0, width=0) -> 'Modal':
        self.parent and self.parent.add(self, 0)
        self.pin(row, col, height, width).render()
        self.close.pin(0, self.width - 2, 1, 2).render()
        return self
