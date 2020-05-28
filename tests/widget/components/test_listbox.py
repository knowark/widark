import curses
from pytest import mark
from widark.widget.components.listbox import Listitem
from widark.widget import Listbox, Widget, Event

pytestmark = mark.asyncio


def test_frame_instantiation_defaults(root):
    listbox = Listbox(root)
    assert listbox.data == []
    assert listbox.template is None


def test_listbox_build(root):
    data = [
        'first',
        'second',
        'third'
    ]

    listbox = Listbox(root, data=data).render()

    assert len(listbox.children) == 3
    assert all(isinstance(item, Listitem) for item in listbox.children)


def test_listbox_template(root):
    data = [
        'first',
        'second',
        'third'
    ]

    class CustomTemplate(Widget):
        def setup(self, **context) -> 'CustomTemplate':
            item = context.pop('item', '')
            return super().setup(
                **context, content=f'-- {item} --') and self

    listbox = Listbox(root, data=data, template=CustomTemplate)

    assert len(listbox.children) == 3
    assert all(isinstance(item, CustomTemplate) for item in listbox.children)


async def test_listbox_command(root):
    data = [
        'first',
        'second',
        'third'
    ]

    clicked_item = None

    async def on_click(event: Event) -> None:
        nonlocal clicked_item
        clicked_item = event.target

    listbox = Listbox(root, data=data, command=on_click).render()

    await listbox.children[2].dispatch(Event('Mouse', 'click', y=15, x=45))

    assert len(listbox.children) == 3
    assert clicked_item == listbox.children[2]
