from typing import cast
from widark import Event, Label, Button, Frame


class Content(Frame):
    def setup(self):
        child_c_1 = Frame(self).grid(0, 1)
        Label(child_c_1, 'Content UP').style(
            'SUCCESS', border=[0], align='L').grid(0)
        Button(child_c_1, 'MIDDLE UP BUTTON', self.on_click).style(
            'WARNING', border=[0], align='C').grid(1)
        Button(child_c_1, 'MIDDLE DOWN BUTTON', self.on_click).style(
            'DANGER', border=[0], align='C').grid(2)
        Label(child_c_1, 'Content DOWN').style(
            'LIGHT', border=[0]).grid(3)

        self.listen('keydown', self.on_keydown)

    async def on_keydown(self, event: Event) -> None:
        print('Key:', event.key, ord(event.key))

    async def on_click(self, event: Event) -> None:
        self.update(f'Clicked on: y={event.y:03d}, x={event.x:03d}')
        button = cast(Button, event.target)
        button.focus()
