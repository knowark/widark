import asyncio
from widark import (
    Application, Event, Button, Label, Frame, Modal, Color)
from .content import Content


class Main(Application):
    def build(self) -> None:
        self.style(border=[0])
        self.modal = None
        master = Frame(self, content='Master').grid(
            0).style(background_color=Color.LIGHT.reverse(),
                     border_color=Color.PRIMARY.reverse())

        Label(master, content='Label:').grid(0, 0).style(
            Color.DANGER.reverse(), Color.DANGER.reverse())

        Button(master, content='Create',
               command=self.launch_modal).grid(0, 1).style(
            Color.SUCCESS.reverse(), Color.SUCCESS.reverse())

        Frame(master, title='Details').title_style(
            Color.DANGER()).grid(1, 0).span(col=3).weight(3).style(
                background_color=Color.LIGHT.reverse())

        Frame(self, title='World').title_style(Color.WARNING()).grid(1)
        Content(self, title='Content').grid(0, 1).span(2).weight(col=3)

        self.listen('click', self.on_backdrop_click, True)

    async def launch_modal(self, event: Event) -> None:
        self.modal = Modal(
            self, close_command=self.close_modal).launch(5, 5, 15, 50)

    async def on_backdrop_click(self, event: Event) -> None:
        if self.modal and not self.modal.hit(event):
            event.stop = True
            await self.close_modal(event)

    async def close_modal(self, event: Event) -> None:
        if self.modal:
            self.remove(self.modal)
            self.modal = None
            self.render()


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
