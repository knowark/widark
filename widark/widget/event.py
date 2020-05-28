import curses
from typing import Awaitable, Callable, List, Dict, Optional, TypeVar, Any
from collections import defaultdict

CATEGORIES = {'Mouse': 'Mouse', 'Keyboard': 'Keyboard', 'Custom': 'Custom'}
PHASES = {'Capture': 'Capture', 'Target': 'Target', 'Bubble': 'Bubble', '': ''}


class Event:
    def __init__(self, category: str, type: str, **attributes) -> None:
        self.category = CATEGORIES[category]
        self.type = type
        self.y: int = attributes.get('y', 0)
        self.x: int = attributes.get('x', 0)
        self.key: str = attributes.get('key', '')
        self.button: int = attributes.get('button', 0)
        self.bubbles: bool = attributes.get('bubbles', True)
        self.stop: bool = attributes.get('stop', False)
        self.details: Dict[str, Any] = attributes.get('details', {})
        self.phase = PHASES[attributes.get('phase', '')]
        self.path: List['Target'] = []
        self.current: Optional['Target'] = None
        self.target: Optional['Target'] = None


Handler = Callable[[Event], Awaitable]


T = TypeVar('T', bound='Target')


class Target:
    def __init__(self) -> None:
        self.parent: Optional['Target'] = None
        self._y_min = 0
        self._x_min = 0
        self._y_max = 0
        self._x_max = 0
        self._capture_listeners: Dict[str, List[Handler]] = (
            defaultdict(lambda: []))
        self._bubble_listeners: Dict[str, List[Handler]] = (
            defaultdict(lambda: []))

    def hit(self, event: Event) -> bool:
        return (self._y_min <= event.y < self._y_max and
                self._x_min <= event.x < self._x_max)

    def listen(self: T, type: str, handler: Optional[Handler],
               capture: bool = False) -> T:
        listeners = (self._capture_listeners if capture
                     else self._bubble_listeners)
        if handler and handler not in listeners[type]:
            listeners[type].append(handler)
        return self

    def ignore(self: T, type: str, handler: Optional[Handler] = None,
               capture: bool = False) -> T:
        listeners = (self._capture_listeners if capture
                     else self._bubble_listeners)
        if not handler:
            listeners[type].clear()
        elif handler in listeners[type]:
            listeners[type].remove(handler)
        return self

    async def dispatch(self, event: Event) -> None:
        if event.phase == 'Capture':
            for listener in self._capture_listeners.get(event.type, []):
                await listener(event)

        elif event.phase == 'Bubble':
            for listener in self._bubble_listeners.get(event.type, []):
                await listener(event)

        elif event.phase == 'Target':
            for listener in self._capture_listeners.get(event.type, []):
                await listener(event)
            if event.bubbles:
                event.phase = 'Bubble'
                for element in event.path:
                    if event.stop:
                        return
                    event.current = element
                    await element.dispatch(event)

        else:
            event.phase = 'Capture'
            if not event.path:
                path_target: Optional['Target'] = self
                while path_target:
                    event.path.append(path_target)
                    path_target = path_target.parent

            for element in reversed(event.path):
                if event.stop:
                    return
                event.current = element
                if element == self:
                    event.phase = 'Target'
                    event.target = element

                await element.dispatch(event)


MOUSE_EVENTS = {
    curses.BUTTON1_PRESSED: (1, 'press'),
    curses.BUTTON1_RELEASED: (1, 'release'),
    curses.BUTTON1_CLICKED: (1, 'click'),
    curses.BUTTON1_DOUBLE_CLICKED: (1, 'doubleclick'),
    curses.BUTTON1_TRIPLE_CLICKED: (1, 'tripleclick'),

    curses.BUTTON2_PRESSED: (2, 'press'),
    curses.BUTTON2_RELEASED: (2, 'release'),
    curses.BUTTON2_CLICKED: (2, 'click'),
    curses.BUTTON2_DOUBLE_CLICKED: (2, 'doubleclick'),
    curses.BUTTON2_TRIPLE_CLICKED: (2, 'tripleclick'),

    curses.BUTTON3_PRESSED: (3, 'press'),
    curses.BUTTON3_RELEASED: (3, 'release'),
    curses.BUTTON3_CLICKED: (3, 'click'),
    curses.BUTTON3_DOUBLE_CLICKED: (3, 'doubleclick'),
    curses.BUTTON3_TRIPLE_CLICKED: (3, 'tripleclick'),

    curses.BUTTON4_PRESSED: (4, 'press'),
    curses.BUTTON4_RELEASED: (4, 'release'),
    curses.BUTTON4_CLICKED: (4, 'click'),
    curses.BUTTON4_DOUBLE_CLICKED: (4, 'doubleclick'),
    curses.BUTTON4_TRIPLE_CLICKED: (4, 'tripleclick')
}
