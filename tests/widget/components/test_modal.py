import curses
from types import MethodType
from widark.widget import Modal


def test_modal_instantiation_defaults(root):
    modal = Modal(root)
    assert modal.position == 'fixed'


def test_modal_amend(root):
    modal = Modal(root)

    modal.attach()

    assert modal.window is not None
    assert modal.panel is not None
    assert modal.panel.above() is None
