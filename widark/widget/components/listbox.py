from typing import Sequence, Type, List, Dict, Union
from ..widget import Widget
from ..style import Style
from ..event import Event


ItemType = Union[List[str], List[Dict[str, str]], List[Sequence[str]]]

DataType = List[ItemType]


class Listbox(Widget):
    def setup(self, **context) -> 'Listbox':
        self.data: DataType = context.pop(
            'data', getattr(self, 'data', []))
        self.fields: List[str] = context.pop(
            'fields', getattr(self, 'fields', []))
        self.template: Type[Widget] = context.pop(
            'template', getattr(self, 'template', None))
        self.item_styling: Style = context.pop(
            'item_style', getattr(self, 'item_styling', Style(align='C')))
        self.field_template: Type[Widget] = context.pop(
            'field_template', getattr(self, 'field_template', None))
        self.field_styling: Style = context.pop(
            'field_style', getattr(self, 'field_styling', Style(align='C')))
        self.limit: int = context.pop(
            'limit', getattr(self, 'limit', None))
        self.offset: int = context.pop(
            'offset', getattr(self, 'offset', None))
        self.orientation: str = context.pop(
            'orientation', getattr(self, 'orientation', 'vertical'))

        if context.get('command'):
            self.ignore('click')
            self.listen('click', context['command'])

        mode = context.pop('mode', 'compact')
        return super().setup(**context, mode=mode) and self

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
                self, item=item, fields=self.fields,
                orientation=self.orientation,
                style=self.item_styling,
                field_template=self.field_template,
                field_style=self.field_styling).grid(*coordinates)

        self.listen('click', self.on_click)
        self.listen('keydown', self.on_keydown)

    async def on_click(self, event: Event) -> None:
        self.focus()

    async def on_keydown(self, event: Event) -> None:
        if ord(event.key) == 338 and self.limit:  # Page Down
            self.offset = (self.offset or 0)
            delta = (self.limit if len(self.data)
                     - self.offset > self.limit else 0)
            self.offset += delta
            self.connect()
        elif ord(event.key) == 339 and self.limit:  # Page Up
            self.offset = max((self.offset or 0) - self.limit, 0)
            self.connect()


class Listitem(Widget):
    def setup(self, **context) -> 'Listitem':
        self.item = context.pop('item')
        self.fields = context.pop('fields')
        self.orientation = context.pop('orientation')
        self.field_template = context.pop('field_template')
        self.field_styling = context.pop('field_style')
        return super().setup(**context) and self

    def build(self) -> None:
        if not self.fields:
            self.content = str(self.item)
            return

        field_constructor = self.field_template or Widget
        item = self.item
        if hasattr(item, '__dict__'):
            item = vars(item)

        if not isinstance(item, dict):
            raise ValueError('Provide a dict or object for field indexing.')

        for index, field in enumerate(self.fields):
            coordinates = ((index, 0) if self.orientation == 'horizontal'
                           else (0, index))
            field_constructor(self, content=item.get(field, ''),
                              style=self.field_styling).grid(*coordinates)
