from widark.widget import Label


def test_label_instantiation_defaults(root):
    label = Label(root)
    assert label.styling.template == '{}'
    assert label.styling.color > 0
    assert label.styling.align == 'C'
    assert label.content == ''
