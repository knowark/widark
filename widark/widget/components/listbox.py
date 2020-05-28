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

        if context.get('command'):
            self.ignore('click')
            self.listen('click', context['command'])

        return super().setup(**context) and self

    def build(self) -> None:
        item_constructor = self.template or Listitem
        for index, item in enumerate(self.data):
            item_constructor(
                self, item=item, style=self.item_styling).grid(index)


class Listitem(Widget):
    def setup(self, **context) -> 'Listitem':
        content = str(context.pop('item', ''))
        return super().setup(**context, content=content) and self
