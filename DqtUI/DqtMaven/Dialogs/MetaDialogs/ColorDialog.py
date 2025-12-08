from typing import Any, Union

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import RState
from DeclarativeQt.Resource.Colors.RColor import HexColor
from DeclarativeQt.Resource.Grammars.RGrammar import DataBox


class ColorDialog(QColorDialog):
    def __init__(
            self,
            parent: QWidget = None,
            offset: QPoint = None,
            title: RState[str] = None,
            initial: Union[QColor, HexColor] = None,
    ):
        super().__init__(None)
        self._parent = parent
        self.setWindowTitle(Remember.getValue(title))
        self.setCurrentColor(QColor(initial))
        self.setPosition(offset)

    def setPosition(self, offset: QPoint):
        DqtCanvas.setWindowOffset(self, offset, self._parent)
        return None

    @staticmethod
    def getColor(
            initial: Union[QColor, HexColor] = None,
            parent: QWidget = None,
            title: RState[str] = None,
            offset: QPoint = None, **kwargs: Any,
    ) -> QColor:
        initial = QColor(initial)
        dialog = DataBox(ColorDialog(
            parent=parent,
            offset=offset,
            title=title,
            initial=initial
        )).data
        choice = initial if not bool(dialog.exec_()) else dialog.currentColor()
        if not choice.isValid():
            return initial
        return choice
