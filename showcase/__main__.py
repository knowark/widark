import asyncio
from widark import Application


class Main(Application):
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    main = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main.run())
    loop.close()
