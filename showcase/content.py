from widark import Widget, Event, Style


class Content(Widget):
    def setup(self):
        child_c_1 = Widget(self, style=Style(border=[0])).grid(0, 1)
        Widget(child_c_1, 'Content UP', Style('SUCCESS', border=[0])).grid(0)
        Widget(child_c_1, 'Content MIDDLE UP',
               Style('WARNING', border=[0])).grid(1)
        Widget(child_c_1, 'Content MIDDLE DOWN',
               Style('DANGER', border=[0])).grid(2)
        Widget(child_c_1, 'Content DOWN', Style('LIGHT', border=[0])).grid(3)
        self.listen('click', self.on_click)

    async def on_click(self, event: Event) -> None:
        self.content = f'Clicked on: y={event.y:03d}, x={event.x:03d}'
        self.update()
