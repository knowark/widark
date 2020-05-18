import asyncio
from widark import (
    Application, Widget, Event, Style, Button, Label, Spacer, Frame)
from .content import Content


class Main(Application):
    async def build(self):
        self.style(
            border=[ord('/'), ord('\\'), ord('^'), ord('v'), 0, 0, 0, 0])

        child_a = Widget(self, style=Style(border=[0])).grid(0)

        Label(child_a, 'Label:').grid(0, 0)
        Spacer(child_a).grid(0, 1)
        Button(child_a, 'Button', self.say_hello).grid(0, 2)

        Widget(child_a, 'Details', Style(border=[0])
               ).grid(1, 0).span(col=3).weight(3)

        Frame(self, 'World').grid(1)

        # Widget(self, 'World', Style(border=[0])).grid(1)

        child_c = Content(self, style=Style(border=[0])).grid(
            0, 1).span(2).weight(col=3)
        Widget(child_c, style=Style(border=[0])).grid(0, 2)

    async def say_hello(self, event: Event) -> None:
        print('Hello!')


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
