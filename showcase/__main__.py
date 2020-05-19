import asyncio
import curses
from widark import (
    Application, Widget, Event, Style, Button, Label, Spacer, Frame)
from .content import Content
from random import randint


class Main(Application):
    async def build(self):
        self.style(
            border=[ord('/'), ord('\\'), ord('^'), ord('v'), 0, 0, 0, 0])

        master = Frame(self, 'Master').grid(0)
        Label(master, 'Label:').grid(0, 0)
        Spacer(master).grid(0, 1)
        Button(master, 'Button', self.say_hello).grid(0, 2)
        Frame(master, 'Details').title_style(
            'DANGER').grid(1, 0).span(col=3).weight(3)

        Frame(self, 'World').title_style('WARNING').grid(1)

        content = Content(self, 'Content').grid(0, 1).span(2).weight(col=3)
        Frame(content).grid(0, 2)

    async def say_hello(self, event: Event) -> None:
        curses.setsyx(randint(0, 20), randint(0, 120))


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
