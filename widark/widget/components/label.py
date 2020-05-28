from ..widget import Widget
from ..style import Style, Color


class Label(Widget):
    def setup(self, **context) -> 'Label':
        self.styling = context.pop('style', getattr(
            self, 'styling', Style(Color.INFO(), align='C')))
        return super().setup(**context) and self
