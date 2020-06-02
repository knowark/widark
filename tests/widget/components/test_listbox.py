from pytest import mark, raises
from widark.widget.components.listbox import Listitem
from widark.widget import Listbox, Widget, Event

pytestmark = mark.asyncio


def test_frame_instantiation_defaults(root):
    listbox = Listbox(root)
    assert listbox.data == []
    assert listbox.template is None
    assert listbox.item_styling is not None
    assert listbox.field_template is None
    assert listbox.field_styling is not None
    assert listbox.limit is None
    assert listbox.offset is None
    assert listbox.orientation == 'vertical'
    assert listbox.mode == 'compact'


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


async def test_listbox_limit_and_offset(root):
    data = [
        'first',
        'second',
        'third',
        'fourth',
        'fifth',
        'sixth',
        'seventh',
        'eighth',
        'ninth',
        'tenth'
    ]

    listbox = Listbox(root, data=data, limit=3, offset=3).render()

    assert len(listbox.children) == 3
    assert listbox.children[0].content == 'fourth'
    assert listbox.children[1].content == 'fifth'
    assert listbox.children[2].content == 'sixth'


async def test_listbox_orientation(root):
    data = [
        'first',
        'second',
        'third'
    ]

    listbox = Listbox(root, data=data).render()

    assert len(listbox.children) == 3
    assert (listbox.children[0]._y_min, listbox.children[0]._x_min) == (0, 0)
    assert (listbox.children[1]._y_min, listbox.children[1]._x_min) == (6, 0)
    assert (listbox.children[2]._y_min, listbox.children[2]._x_min) == (12, 0)

    listbox = Listbox(root, data=data, orientation='horizontal').render()

    assert len(listbox.children) == 3
    assert (listbox.children[0]._y_min, listbox.children[0]._x_min) == (0, 0)
    assert (listbox.children[1]._y_min, listbox.children[1]._x_min) == (0, 30)
    assert (listbox.children[2]._y_min, listbox.children[2]._x_min) == (0, 60)


async def test_listbox_fields(root):
    data = [
        {'id': '001', 'name': 'Hugo', 'email': 'hugo@mail.com'},
        {'id': '002', 'name': 'Paco', 'email': 'paco@mail.com'},
        {'id': '003', 'name': 'Luis', 'email': 'luis@mail.com'}
    ]

    listbox = Listbox(root, data=data, fields=['name', 'email']).render()

    assert len(listbox.children) == 3
    assert (listbox.children[0]._y_min, listbox.children[0]._x_min) == (0, 0)
    assert len(listbox.children[0].children) == 2
    assert (listbox.children[0].children[0]._y_min,
            listbox.children[0].children[0]._x_min) == (0, 0)
    assert (listbox.children[0].children[1]._y_min,
            listbox.children[0].children[1]._x_min) == (0, 45)

    assert (listbox.children[1]._y_min, listbox.children[1]._x_min) == (6, 0)
    assert len(listbox.children[1].children) == 2
    assert (listbox.children[1].children[0]._y_min,
            listbox.children[1].children[0]._x_min) == (6, 0)
    assert (listbox.children[1].children[1]._y_min,
            listbox.children[1].children[1]._x_min) == (6, 45)

    assert (listbox.children[2]._y_min, listbox.children[2]._x_min) == (12, 0)
    assert len(listbox.children[2].children) == 2
    assert (listbox.children[2].children[0]._y_min,
            listbox.children[2].children[0]._x_min) == (12, 0)
    assert (listbox.children[2].children[1]._y_min,
            listbox.children[2].children[1]._x_min) == (12, 45)

    class Dummy:
        def __init__(self, id: str, name: str, email: str) -> None:
            self.id = id
            self.name = name
            self.email = email

    data = [
        Dummy(id='001', name='Hugo', email='hugo@mail.com'),
        Dummy(id='002', name='Paco', email='paco@mail.com'),
        Dummy(id='003', name='Luis', email='luis@mail.com')
    ]

    listbox = Listbox(root, data=data, fields=['name', 'email'],
                      orientation='horizontal').render()

    assert len(listbox.children) == 3
    assert (listbox.children[0]._y_min, listbox.children[0]._x_min) == (0, 0)
    assert len(listbox.children[0].children) == 2
    assert (listbox.children[0].children[0]._y_min,
            listbox.children[0].children[0]._x_min) == (0, 0)
    assert (listbox.children[0].children[1]._y_min,
            listbox.children[0].children[1]._x_min) == (9, 0)

    assert (listbox.children[1]._y_min, listbox.children[1]._x_min) == (0, 30)
    assert len(listbox.children[1].children) == 2
    assert (listbox.children[1].children[0]._y_min,
            listbox.children[1].children[0]._x_min) == (0, 30)
    assert (listbox.children[1].children[1]._y_min,
            listbox.children[1].children[1]._x_min) == (9, 30)

    assert (listbox.children[2]._y_min, listbox.children[2]._x_min) == (0, 60)
    assert len(listbox.children[2].children) == 2
    assert (listbox.children[2].children[0]._y_min,
            listbox.children[2].children[0]._x_min) == (0, 60)
    assert (listbox.children[2].children[1]._y_min,
            listbox.children[2].children[1]._x_min) == (9, 60)


async def test_listbox_fields_wrong_item_type(root):
    data = [
        ['001', 'Hugo', 'hugo@mail.com'],
        ['002', 'Paco',  'paco@mail.com'],
        ['003', 'Luis', 'luis@mail.com']
    ]

    with raises(ValueError):
        Listbox(root, data=data, fields=['name', 'email']).render()
