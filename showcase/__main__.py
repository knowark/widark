import asyncio
from widark import (
    Application, Event, Button, Label, Frame, Modal)
from .content import Content


class Main(Application):
    async def build(self):
        self.modal = None
        master = Frame(self, 'Master').grid(0)
        Label(master, 'Label:').grid(0, 0)
        Button(master, 'Create', self.launch_modal).grid(0, 1)
        Frame(master, 'Details').title_style(
            'DANGER').grid(1, 0).span(col=3).weight(3)
        Frame(self, 'World').title_style('WARNING').grid(1)
        Content(self, 'Content').grid(0, 1).span(2).weight(col=3)

    async def launch_modal(self, event: Event) -> None:
        self.modal = Modal(self, self.on_modal_close).launch(5, 5, 20, 100)

    async def on_modal_close(self, event: Event) -> None:
        if self.modal:
            self.remove(self.modal)
            self.modal = None


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
