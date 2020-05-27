from typing import cast
from widark import Event, Button, Frame, Entry, Color


class Content(Frame):
    def attach(self) -> 'Content':
        self.clear()
        self.child_c_1 = Frame(self).grid(0, 1)
        self.b1 = Button(
            self.child_c_1, content='Content UP',
            command=self.on_click).style(
            Color.INFO(), Color.DANGER.reverse(),
            border=[0], align='C').grid(0)
        Button(self.child_c_1, content='MIDDLE UP BUTTON',
               command=self.on_click).style(
            Color.WARNING(), border=[0], align='C').grid(1)
        Button(self.child_c_1, content='MIDDLE DOWN BUTTON',
               command=self.on_click).style(
            Color.DANGER(), border=[0], align='C').grid(2)

        self.edit = Entry(self.child_c_1, content='abcdario').style(
            Color.LIGHT()).grid(3)

        self.right = Frame(self).grid(0, 2)
        self.right.listen('click', self.on_content_click)

        return cast('Content', super().attach())

    async def on_click(self, event: Event) -> None:
        button = cast(Button, event.target)
        button.focus()

    async def on_content_click(self, event: Event) -> None:
        self.right.update(f'Clicked on: y={event.y:03d}, x={event.x:03d}')
