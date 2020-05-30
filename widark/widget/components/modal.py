from typing import Dict, Optional, Any
from ..style import Style, Color
from ..event import Event, Handler
from ..widget import Widget


class Modal(Widget):
    def setup(self, **context) -> 'Modal':
        self.done_command: Optional[Handler] = context.pop(
            'done_command', getattr(self, 'done_command', None))

        style = context.pop('style', Style(
            background_color=Color.WARNING.reverse(), border=[0]))
        return super().setup(
            **context, style=style, position='fixed') and self

    def build(self) -> None:
        self.close = Widget(
            self, content='X', position='fixed').style(
                Color.DANGER()).listen('click', self.on_close)

    def launch(self, row=0, col=0, height=0, width=0) -> 'Modal':
        self.parent and self.parent.add(self, 0)
        self.pin(row, col, height, width).render()
        self.close.pin(0, self.width - 2, 1, 2).render()
        return self

    async def on_close(self, event: Event) -> None:
        await self.done({'result': 'closed'})

    async def done(self, details: Dict[str, Any] = None) -> None:
        event = Event('Custom', 'done', details=details or {})
        if self.done_command:
            await self.done_command(event)
        await self.dispatch(event)
