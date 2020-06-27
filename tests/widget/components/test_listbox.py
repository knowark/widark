import asyncio
from types import MethodType
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


async def test_listbox_page_down(root):
    data = [
        ['001', 'Hugo', 'hugo@mail.com'],
        ['002', 'Paco', 'paco@mail.com'],
        ['003', 'Luis', 'luis@mail.com'],
        ['004', 'Juan', 'juan@mail.com'],
        ['005', 'Nico', 'nico@mail.com'],
        ['006', 'Luka', 'luka@mail.com'],
        ['007', 'Mark', 'mark@mail.com'],
        ['008', 'Paul', 'paul@mail.com'],
        ['009', 'Mike', 'mike@mail.com'],
        ['010', 'Fran', 'fran@mail.com'],
        ['011', 'Karl', 'karl@mail.com'],
        ['012', 'Marx', 'marx@mail.com'],
        ['013', 'Anne', 'anne@mail.com'],
        ['014', 'Luke', 'luke@mail.com']
    ]

    connect_called = False

    def mock_connect(self):
        nonlocal connect_called
        connect_called = True
        return self

    listbox = Listbox(root, data=data, limit=4)
    listbox.connect = MethodType(mock_connect, listbox)

    assert listbox.offset is None

    await listbox.dispatch(Event('Keyboard', 'keydown', key='A'))
    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(338)))
    assert listbox.offset == 4
    assert connect_called is True

    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(338)))
    assert listbox.offset == 8

    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(338)))
    assert listbox.offset == 12

    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(338)))
    assert listbox.offset == 12


async def test_listbox_page_up(root):
    data = [
        ['001', 'Hugo', 'hugo@mail.com'],
        ['002', 'Paco', 'paco@mail.com'],
        ['003', 'Luis', 'luis@mail.com'],
        ['004', 'Juan', 'juan@mail.com'],
        ['005', 'Nico', 'nico@mail.com'],
        ['006', 'Luka', 'luka@mail.com'],
        ['007', 'Mark', 'mark@mail.com'],
        ['008', 'Paul', 'paul@mail.com'],
        ['009', 'Mike', 'mike@mail.com'],
        ['010', 'Fran', 'fran@mail.com'],
        ['011', 'Karl', 'karl@mail.com'],
        ['012', 'Marx', 'marx@mail.com'],
        ['013', 'Anne', 'anne@mail.com'],
        ['014', 'Luke', 'luke@mail.com']
    ]

    connect_called = False

    def mock_connect(self):
        nonlocal connect_called
        connect_called = True
        return self

    listbox = Listbox(root, data=data, limit=4, offset=8)
    listbox.connect = MethodType(mock_connect, listbox)

    assert listbox.offset == 8

    await listbox.dispatch(Event('Keyboard', 'keydown', key='A'))
    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(339)))
    assert listbox.offset == 4
    assert connect_called is True

    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(339)))
    assert listbox.offset == 0

    await listbox.dispatch(Event('Keyboard', 'keydown', key=chr(339)))
    assert listbox.offset == 0


async def test_listbox_focus_on_click(root):
    listbox = Listbox(root)
    focus_called = False

    def mock_focus(self):
        nonlocal focus_called
        focus_called = True
        return self

    listbox.focus = MethodType(mock_focus, listbox)

    await listbox.dispatch(Event('Mouse', 'click'))
    await asyncio.sleep(0)
    assert focus_called is True
