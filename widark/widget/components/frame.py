from ..widget import Widget
from ..style import Style


class Frame(Widget):
    def setup(self, **context) -> 'Frame':
        style = context.pop('style', Style(border=[0]))
        super().setup(**context, style=style)

        self.title: str = context.get(
            'title', getattr(self, 'title', ''))
        self.title_styling: Style = context.get(
            'title_style', getattr(self, 'title_styling', Style(
                align='C', template=' {} ')))

        return self

    def title_style(self, *args, **kwargs) -> 'Frame':
        self.title_styling.configure(*args, **kwargs)
        return self

    def amend(self) -> None:
        x = 0
        fill = len(self.title)
        origin, loss = (1, 2) if self.styling.border else (0, 0)
        width = max(self.width - loss, 1)

        if self.title_styling.align == 'C':
            x = int(max(width - fill, 0) / 2)
        elif self.title_styling.align == 'R':
            x = max(width - fill, 0)

        title = (self.title and
                 self.title_styling.template.format(self.title) or '')
        self.window.addstr(0, x + origin, title, self.title_styling.color)


# class Frame(Widget):
#     def __init__(self, parent: 'Widget', **context) -> None:
#         self.title = context.get('title', '')
#         self.title_styling = context.get(
#             'title_style', Style(align='C', template=' {} '))

#         style = context.get('style', Style(border=[0]))
#         super().__init__(parent, **context, style=style)

#     def title_style(self, *args, **kwargs) -> 'Frame':
#         self.title_styling.configure(*args, **kwargs)
#         return self

#     def amend(self) -> None:
#         x = 0
#         fill = len(self.title)
#         origin, loss = (1, 2) if self.styling.border else (0, 0)
#         width = max(self.width - loss, 1)

#         if self.title_styling.align == 'C':
#             x = int(max(width - fill, 0) / 2)
#         elif self.title_styling.align == 'R':
#             x = max(width - fill, 0)

#         title = (self.title and
#                  self.title_styling.template.format(self.title) or '')
#         self.window.addstr(0, x + origin, title, self.title_styling.color)
