import asyncio
import curses
from widark import Application, Widget


class Main(Application):
    async def build(self):

        self.border = [0]
        child_a = Widget(self, border=[0]).grid(0)

        child_a_1 = Widget(child_a, 'Label:').grid(0, 0)
        child_a_2 = Widget(child_a).grid(0, 1)  # spacer
        child_a_3 = Widget(child_a, '<Button>').grid(0, 2)
        child_a_4 = Widget(
            child_a, 'Details', [0]).grid(1, 0).span(col=3).weight(3)

        child_b = Widget(self, 'World', [0]).grid(1)
        child_c = Widget(self, border=[0]).grid(0, 1).span(2).weight(col=3)

        child_c_1 = Widget(child_c, border=[0]).grid(0, 1)
        child_c_1_1 = Widget(child_c_1, 'Content UP', border=[0]).grid(0)
        child_c_1_2 = Widget(child_c_1, 'Content DOWN', border=[0]).grid(1)

        child_c_2 = Widget(child_c, border=[0]).grid(0, 2)


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()

    main.attach()

    curses.doupdate()

    main.window.getch()
