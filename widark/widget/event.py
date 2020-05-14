from typing import Dict, Any


CATEGORIES = {'Mouse': 'Mouse', 'Keyboard': 'Keyboard', 'Custom': 'Custom'}


class Event:
    def __init__(self, category: str, type: str, **attributes) -> None:
        self.category = CATEGORIES[category]
        self.type = type
        self.y = attributes.get('y', 0)
        self.x = attributes.get('x', 0)
        self.details: Dict[str, Any] = attributes.get('details', {})
