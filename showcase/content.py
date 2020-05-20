from typing import cast
from widark import Event, Label, Button, Frame, Entry


class Content(Frame):
    def setup(self):
        child_c_1 = Frame(self).grid(0, 1)
        Button(child_c_1, 'Content UP', self.on_click).style(
            'INFO', border=[0], align='C').grid(0)
        Button(child_c_1, 'MIDDLE UP BUTTON', self.on_click).style(
            'WARNING', border=[0], align='C').grid(1)
        Button(child_c_1, 'MIDDLE DOWN BUTTON', self.on_click).style(
            'DANGER', border=[0], align='C').grid(2)
        Entry(child_c_1, 'abcdario').style('LIGHT', border=[0]).grid(3)
        Entry(child_c_1, 'abcdario').style(border=[0]).grid(4)

        self.listen('click', self.on_content_click)

    async def on_keydown(self, event: Event) -> None:
        print('Key:', event.key, ord(event.key))

    async def on_click(self, event: Event) -> None:
        button = cast(Button, event.target)
        button.update(f'{button._y_min}, {button._y_max} | '
                      f'{button._x_min}, {button._x_max}')
        button.focus()

    async def on_label_click(self, event: Event) -> None:
        label = cast(Label, event.target)
        label.update('clicked!').focus()

    async def on_content_click(self, event: Event) -> None:
        self.update(f'Clicked on: y={event.y:03d}, x={event.x:03d}')
