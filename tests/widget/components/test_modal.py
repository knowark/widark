import curses
from widark.widget import Modal


def test_modal_instantiation_defaults(root):
    modal = Modal(root)
    assert modal.position == 'fixed'
