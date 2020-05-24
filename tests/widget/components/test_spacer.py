from widark.widget import Spacer


def test_spacer_instantiation_defaults(root):
    spacer = Spacer(root)
    assert spacer.styling.template == '{}'
    assert spacer.content == ''
