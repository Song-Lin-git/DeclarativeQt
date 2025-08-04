from typing import Dict, Union, List

from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, isValid


class PlotterDialog(Dialog):
    def __init__(
            self,
            figures: List[Figure] = None,
            size: QSize = None,
            fixedWidth: int = None,
            fixedHeight: int = None,
            fixSize: bool = False,
            fixWidth: bool = False,
            parent: QWidget = None,
            offset: QPoint = None,
            contentPaddingRatio: float = None,
            title: RState[str] = None,
            style: RState[str] = None,
            content: QWidget = None,
            closeTrig: Remember = None,
            acceptTrig: Remember = None,
            maximizeHint: bool = False,
            subDialogs: Dict[Union[QDialog, QMessageBox], Remember] = None
    ):
        super().__init__(
            size=size,
            fixedHeight=fixedHeight,
            fixSize=fixSize,
            fixWidth=fixWidth,
            fixedWidth=fixedWidth,
            parent=parent,
            offset=offset,
            content=content,
            closeTrig=closeTrig,
            contentPaddingRatio=contentPaddingRatio,
            title=title,
            style=style,
            acceptTrig=acceptTrig,
            maximizeHint=maximizeHint,
            subDialogs=subDialogs,
        )
        self._pltFigures = Validate(figures, list())

    def closeFigures(self):
        for fig in self._pltFigures:
            if isValid(fig):
                plt.close(fig)
        return None

    def closeEvent(self, a0):
        self.closeFigures()
        super().closeEvent(a0)
        return None

    def accept(self):
        self.closeFigures()
        super().accept()
        return None

    def reject(self):
        self.closeFigures()
        super().reject()
        return None
