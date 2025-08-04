from PyQt5.QtCore import QSize

from DeclarativeQt.DqtUI.DqtWidgets.Control import Label


class VerticalSpacer(Label):
    def __init__(
            self,
            height: int,
            fixed: bool = False
    ):
        if fixed:
            super().__init__(
                fixedWidth=int(1),
                fixedHeight=height
            )
        else:
            super().__init__(
                size=QSize(int(1), height)
            )


class HorizontalSpacer(Label):
    def __init__(
            self,
            width: int,
            fixed: bool = False
    ):
        if fixed:
            super().__init__(
                fixedWidth=width,
                fixedHeight=int(1)
            )
        else:
            super().__init__(
                size=QSize(width, int(1))
            )
