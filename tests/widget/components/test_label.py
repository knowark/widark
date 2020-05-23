from widark.widget import Label


def test_label_instantiation_defaults(root):
    label = Label(root)
    assert label._style.template == '{}'
    assert label._style.color > 0
    assert label._style.align == 'C'
    assert label.content == ''
