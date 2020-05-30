from typing import Dict, Optional, List, Any
from ..style import Style, Color
from ..event import Event, Handler
from ..widget import Widget


class Modal(Widget):
    def setup(self, **context) -> 'Modal':
        self.done_command: Optional[Handler] = context.pop(
            'done_command', getattr(self, 'done_command', None))
        self.proportion: Dict[str, float] = context.get(
            'proportion', getattr(
                self, 'proportion', {'height': 0.8, 'width': 0.8}))
        self.margin: Dict[str, float] = context.get(
            'margin', getattr(self, 'margin', {
                'left': None, 'top': None, 'right': None, 'bottom': None}))
        self.align = str.upper(context.get(
            'align', getattr(self, 'align', 'CC')))

        style = context.pop('style', Style(
            background_color=Color.WARNING.reverse(), border=[0]))
        return super().setup(
            **context, style=style, position='fixed') and self

    def build(self) -> None:
        self.close = Widget(
            self, content='X', position='fixed').style(
                Color.DANGER()).listen('click', self.on_close)

    def launch(self) -> 'Modal':
        if not self.parent:
            return self

        self.parent.add(self, 0)
        height = int(self.proportion.get('height', 1) * self.parent.height)
        width = int(self.proportion.get('width', 1) * self.parent.width)

        self.pin(0, 0, height, width).render()

        self.close.pin(0, self.width - 2, 1, 2).render()
        return self

    async def on_close(self, event: Event) -> None:
        await self.done({'result': 'closed'})

    async def done(self, details: Dict[str, Any] = None) -> None:
        event = Event('Custom', 'done', details=details or {})
        if self.done_command:
            await self.done_command(event)
        await self.dispatch(event)
