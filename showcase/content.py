from typing import cast
from widark import Event, Button, Frame, Entry, Color, Listbox, Style


class Content(Frame):
    def build(self) -> None:
        self.left = Frame(self, title='Left').grid(0, 1)
        Button(self.left, content='Content UP',
               command=self.on_click).style(
            Color.INFO(), Color.DANGER.reverse(),
            border=[0], align='C').grid(0)
        Button(self.left, content='MIDDLE UP BUTTON',
               command=self.on_click).style(
            Color.WARNING(), border=[0], align='C').grid(1)
        Button(self.left, content='MIDDLE DOWN BUTTON',
               command=self.on_click).style(
            Color.DANGER(), border=[0], align='C').grid(2)

        Entry(self.left, content=(
            'Nulla mollis mollis ornare. Cras tempor, metus semper pulvinar '
            '\nmattis, metus urna hendrerit orci, eget gravida tellus '
            '\nipsum a ex. Donec hendrerit metus vitae hendrerit dictum. '
            '\nSed varius venenatis ligula in scelerisque. Donec luctus sem '
            '\nnon lorem venenatis, eget lobortis tortor tincidunt. Nunc '
            '\nquis venenatis diam. Ut ac aliquam mi, a tempus nunc. Nunc '
            '\nluctus vulputate dui malesuada cursus.'
        )).style(Color.LIGHT(), border=[0]).grid(3)

        self.right = Frame(self, title='Right').grid(0, 2)

        data = [{'name': 'first'}, {'name': 'second'}, {'name': 'third'}] * 3
        Listbox(self.right, data=data, limit=4,
                item_style=Style(border=[], align='C'))

    async def on_click(self, event: Event) -> None:
        button = cast(Button, event.target)
        button.focus()

    async def on_content_click(self, event: Event) -> None:
        self.right.content = f'Clicked on: y={event.y:03d}, x={event.x:03d}'
        self.right.render()
