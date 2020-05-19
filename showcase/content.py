from widark import Event, Label, Button, Frame


class Content(Frame):
    def setup(self):
        child_c_1 = Frame(self).grid(0, 1)
        Label(child_c_1, 'Content UP').style(
            'SUCCESS', border=[0], align='L').grid(0)
        Label(child_c_1, 'Content MIDDLE UP').style(
            'WARNING', border=[0], align='C').grid(1)
        self.button = Button(child_c_1, 'MIDDLE BUTTON', self.on_click).style(
            'DANGER', border=[0], align='C').grid(2)
        Label(child_c_1, 'Content DOWN').style(
            'LIGHT', border=[0]).grid(3)

    async def on_click(self, event: Event) -> None:
        self.content = f'Clicked on: y={event.y:03d}, x={event.x:03d}'
        self.update()
        self.button.focus()
