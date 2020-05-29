from typing import Sequence, Type, List, Dict, Union
from ..widget import Widget
from ..style import Style


ItemType = Union[List[str], List[Dict[str, str]], List[Sequence[str]]]

DataType = List[ItemType]


class Listbox(Widget):
    def setup(self, **context) -> 'Listbox':
        self.data: DataType = context.pop(
            'data', getattr(self, 'data', []))
        self.template: Type[Widget] = context.pop(
            'template', getattr(self, 'template', None))
        self.item_styling: Style = context.pop(
            'item_style', getattr(self, 'item_styling', Style(align='C')))
        self.limit: int = context.pop(
            'limit', getattr(self, 'limit', None))
        self.offset: int = context.pop(
            'offset', getattr(self, 'offset', None))
        self.orientation: str = context.pop(
            'orientation', getattr(self, 'orientation', 'vertical'))

        if context.get('command'):
            self.ignore('click')
            self.listen('click', context['command'])

        return super().setup(**context) and self

    def build(self) -> None:
        item_constructor = self.template or Listitem
        items = self.data

        if self.offset is not None:
            items = items[self.offset:]

        if self.limit is not None:
            items = items[:self.limit]

        for index, item in enumerate(items):
            coordinates = ((0, index) if self.orientation == 'horizontal'
                           else (index, 0))
            item_constructor(
                self, item=item, style=self.item_styling).grid(*coordinates)


class Listitem(Widget):
    def setup(self, **context) -> 'Listitem':
        content = str(context.pop('item', ''))
        return super().setup(**context, content=content) and self
