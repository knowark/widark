from typing import Awaitable, Callable, List, Dict, Optional, Any
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
        self.bubbles: bool = attributes.get('bubbles', True)
        self.stop: bool = attributes.get('stop', False)
        self.details: Dict[str, Any] = attributes.get('details', {})
        self.phase = PHASES[attributes.get('phase', '')]
        self.path: List['Target'] = []
        self.current: Optional['Target'] = None
        self.target: Optional['Target'] = None


Handler = Callable[[Event], Awaitable]


class Target:
    def __init__(self) -> None:
        self.parent: Optional['Target'] = None
        self._y_min = 0
        self._x_min = 0
        self._y_max = 1
        self._x_max = 1
        self._capture_listeners: Dict[str, List[Handler]] = (
            defaultdict(lambda: []))
        self._bubble_listeners: Dict[str, List[Handler]] = (
            defaultdict(lambda: []))

    def hit(self, event: Event) -> bool:
        return (self._y_min <= event.y <= self._y_max and
                self._x_min <= event.x <= self._x_max)

    def listen(self, type: str, handler: Handler,
               capture: bool = False) -> None:
        listeners = (self._capture_listeners if capture
                     else self._bubble_listeners)
        listeners[type].append(handler)

    def ignore(self, type: str, handler: Handler = None,
               capture: bool = False) -> None:
        listeners = (self._capture_listeners if capture
                     else self._bubble_listeners)
        if handler:
            listeners[type].remove(handler)
        else:
            listeners[type].clear()

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
