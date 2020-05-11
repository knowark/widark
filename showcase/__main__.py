import asyncio
import curses
from widark import Application, Widget


class Main(Application):
    async def run(self):

        self.border = [0]
        child_a = Widget(self).sequence(0)
        child_a.border = [0]

        child_a_1 = Widget(child_a).sequence(0, 0)
        child_a_1.content = 'Label:'
        spacer = Widget(child_a).sequence(0, 1)
        child_a_3 = Widget(child_a).sequence(0, 2)
        child_a_3.content = '<Button>'
        child_a_4 = Widget(child_a).sequence(1, 0).span(column=3).weight(2)
        child_a_4.content = 'Details'

        child_b = Widget(self).sequence(1)
        child_b.border = [0]
        child_b.content = 'World'
        child_c = Widget(self).sequence(0, 1).span(2).weight(column=3)
        child_c.border = [0]


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()

    main.attach()

    curses.doupdate()

    main.window.getch()
