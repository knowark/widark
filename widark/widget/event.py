from typing import Awaitable, Callable, List, Dict, Optional, Any
from collections import defaultdict

CATEGORIES = {'Mouse': 'Mouse', 'Keyboard': 'Keyboard', 'Custom': 'Custom'}


class Event:
    def __init__(self, category: str, type: str, **attributes) -> None:
        self.category = CATEGORIES[category]
        self.type = type
        self.y = attributes.get('y', 0)
        self.x = attributes.get('x', 0)
        self.details: Dict[str, Any] = attributes.get('details', {})


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
