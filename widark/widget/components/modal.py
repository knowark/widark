from ..style import Style, Color
from ..event import Handler
from ..widget import Widget


class Modal(Widget):
    def __init__(self, parent: 'Widget', **context) -> None:
        position = context.pop('position', 'fixed')
        super().__init__(parent, **context, position=position)

    def setup(self, **context) -> 'Modal':
        style = context.pop('style', Style(
            background_color=Color.WARNING.reverse(), border=[' ']))
        super().setup(**context, style=style)

        self.close = Widget(
            self, content='X', position='fixed').style(Color.DANGER())
        if context.get('close_command'):
            self.close.listen('click', context['close_command'])

        return self

    def launch(self, row=0, col=0, height=0, width=0) -> 'Modal':
        self.parent and self.parent.add(self, 0)
        self.pin(row, col, height, width).attach()
        self.close.pin(0, self.width - 2, 1, 2).attach()
        return self
