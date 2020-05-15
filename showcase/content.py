from widark import Widget, Event


class Content(Widget):
    def setup(self):
        child_c_1 = Widget(self, border=[0]).grid(0, 1)
        Widget(child_c_1, 'Content UP', border=[0]).grid(0)
        Widget(child_c_1, 'Content MIDDLE', border=[0]).grid(1)
        Widget(child_c_1, 'Content DOWN', border=[0]).grid(2)
        self.listen('click', self.on_click)

    async def on_click(self, event: Event) -> None:
        self.content = f'Clicked on: y={event.y:03d}, x={event.x:03d}'
        self.update()
