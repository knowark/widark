from ..widget import Widget
from ..style import Style, Color
from ..event import Handler


class Button(Widget):
    def setup(self, **context) -> 'Button':
        style = context.pop('style', Style(
            Color.PRIMARY(), align='C', template='< {} >'))
        super().setup(**context, style=style)

        if context.get('command'):
            self.ignore('click')
            self.listen('click', context['command'])

        return self
