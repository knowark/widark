from typing import Awaitable, Callable, List, Dict, Optional, Any
from collections import defaultdict

CATEGORIES = {'Mouse': 'Mouse', 'Keyboard': 'Keyboard', 'Custom': 'Custom'}
PHASES = {'Capture': 'Capture', 'Target': 'Target', 'Bubble': 'Bubble', '': ''}


class Event:
    def __init__(self, category: str, type: str, **attributes) -> None:
        self.category = CATEGORIES[category]
        self.type = type
        self.y = attributes.get('y', 0)
        self.x = attributes.get('x', 0)
        self.details: Dict[str, Any] = attributes.get('details', {})
        self.phase = PHASES[attributes.get('phase', '')]
        self.path: List['Target'] = []
        self.current: Optional['Target'] = None
        self.target: Optional['Target'] = None


Handler = Callable[[Event], Awaitable]


class Target:
    def __init__(self) -> None:
        self.parent: Optional['Target'] = None
        self.y_min = 0
        self.x_min = 0
        self.y_max = 1
        self.x_max = 1
        self.capture_listeners: Dict[str, List[Handler]] = (
            defaultdict(lambda: []))
        self.bubble_listeners: Dict[str, List[Handler]] = (
            defaultdict(lambda: []))

    def hit(self, event: Event) -> bool:
        return (self.y_min <= event.y <= self.y_max and
                self.x_min <= event.x <= self.x_max)

    def listen(self, type: str, handler: Handler,
               capture: bool = False) -> None:
        listeners = (self.capture_listeners if capture
                     else self.bubble_listeners)
        listeners[type].append(handler)

    def ignore(self, type: str, handler: Handler,
               capture: bool = False) -> None:
        listeners = (self.capture_listeners if capture
                     else self.bubble_listeners)
        listeners[type].remove(handler)

    async def dispatch(self, event: Event) -> None:
        if event.phase == 'Capture':
            for listener in self.capture_listeners.get(event.type, []):
                await listener(event)

        elif event.phase == 'Bubble':
            for listener in self.bubble_listeners.get(event.type, []):
                await listener(event)

        elif event.phase == 'Target':
            event.phase = 'Bubble'
            for element in event.path:
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
                event.current = element
                if element == self:
                    event.phase = 'Target'
                    event.target = element

                await element.dispatch(event)
