import asyncio
from widark import (
    Application, Event, Button, Label, Frame, Modal, Color)
from .content import Content


class Main(Application):
    async def build(self):
        self.modal = None
        master = Frame(self, 'Master').grid(
            0).style(background_color=Color.LIGHT.reverse(),
                     border_color=Color.PRIMARY.reverse())

        Label(master, 'Label:').grid(0, 0).style(
            Color.DANGER.reverse(), Color.DANGER.reverse())

        Button(master, 'Create', self.launch_modal).grid(0, 1).style(
            Color.SUCCESS.reverse(), Color.SUCCESS.reverse()
        )

        Frame(master, 'Details').title_style(
            Color.DANGER()).grid(1, 0).span(col=3).weight(3).style(
                background_color=Color.LIGHT.reverse()
        )

        Frame(self, 'World').title_style(Color.WARNING()).grid(1)
        Content(self, 'Content').grid(0, 1).span(2).weight(col=3)

    async def launch_modal(self, event: Event) -> None:
        self.modal = Modal(self, self.on_modal_close).launch(5, 5, 20, 100)

    async def on_modal_close(self, event: Event) -> None:
        if self.modal:
            self.remove(self.modal)
            self.modal = None
            self.update()


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
