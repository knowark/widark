from ..widget import Widget
from ..style import Style, Color


class Label(Widget):
    def setup(self, **context) -> 'Label':
        style = context.pop('style', Style(Color.INFO(), align='C'))
        super().setup(**context, style=style)

        return self
