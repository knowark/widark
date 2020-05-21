import asyncio
from widark import (
    Application, Event, Button, Label, Frame, Modal)
from .content import Content


class Main(Application):
    async def build(self):
        self.modal = Modal(self)
        master = Frame(self, 'Master').grid(0)
        Label(master, 'Label:').grid(0, 0)
        Button(master, 'Create', self.launch_modal).grid(0, 1)
        Button(master, 'Toggle', self.toggle_modal).grid(0, 2)
        Button(master, 'Delete', self.delete_modal).grid(0, 3)
        Frame(master, 'Details').title_style(
            'DANGER').grid(1, 0).span(col=3).weight(3)

        Frame(self, 'World').title_style('WARNING').grid(1)

        Content(self, 'Content').grid(0, 1).span(2).weight(col=3)

    async def launch_modal(self, event: Event) -> None:
        self.modal.attach(5, 5)

    async def toggle_modal(self, event: Event) -> None:
        if self.modal.panel.hidden():
            self.modal.panel.show()
        else:
            self.modal.panel.hide()

    async def delete_modal(self, event: Event) -> None:
        self.remove(self.modal)


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
