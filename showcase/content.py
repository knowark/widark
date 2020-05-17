from widark import Widget, Event, Color


class Content(Widget):
    def setup(self):
        child_c_1 = Widget(self, border=[0]).grid(0, 1)
        Widget(child_c_1, 'Content UP', [0], Color.DANGER).grid(0)
        Widget(child_c_1, 'Content MIDDLE', [0], Color.INFO).grid(1)
        Widget(child_c_1, 'Content DOWN', [0], Color.PRIMARY).grid(2)
        self.listen('click', self.on_click)

    async def on_click(self, event: Event) -> None:
        self.content = f'Clicked on: y={event.y:03d}, x={event.x:03d}'
        self.update()
