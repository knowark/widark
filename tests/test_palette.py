from pytest import raises
from widark.palette import Palette, DefaultPalette


def test_palette_instantiation():
    palette = DefaultPalette()
    assert isinstance(palette, Palette)


def test_palette_not_implemented():
    palette = Palette()
    with raises(NotImplementedError):
        palette.generate()


def test_palette_generate():
    palette = DefaultPalette()
    colors = palette.generate()
    assert isinstance(colors, list)
