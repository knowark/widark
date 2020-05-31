from typing import Dict, Optional, List, Any
from ..style import Style, Color
from ..event import Event, Handler
from ..widget import Widget


class Modal(Widget):
    def setup(self, **context) -> 'Modal':
        self.done_command: Optional[Handler] = context.pop(
            'done_command', getattr(self, 'done_command', None))

        proportion = context.pop(
            'proportion', {'height': 0.8, 'width': 0.8})
        align = context.pop('align', 'CC')
        style = context.pop('style', Style(
            background_color=Color.WARNING.reverse(), border=[0]))
        return super().setup(
            **context, style=style, position='fixed',
            proportion=proportion, align=align) and self

    def build(self) -> None:
        self.close = Widget(
            self, content='X', position='fixed',).pin(0, 1, 1, 1).style(
                Color.DANGER()).listen('click', self.on_close)

    def launch(self) -> 'Modal':
        if not (self.parent and self.parent.window):
            return self

        self.parent.add(self, 0).render()
        return self

    async def on_close(self, event: Event) -> None:
        await self.done({'result': 'closed'})

    async def done(self, details: Dict[str, Any] = None) -> None:
        event = Event('Custom', 'done', details=details or {})
        if self.done_command:
            await self.done_command(event)
        await self.dispatch(event)
