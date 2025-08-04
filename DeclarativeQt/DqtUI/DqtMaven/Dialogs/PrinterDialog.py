from typing import Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeySequence
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrintPreviewWidget, QPrinter
from PyQt5.QtWidgets import QToolButton, QShortcut, QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import RState


class PrinterDialog(QPrintPreviewDialog):
    KEY_X = "X"
    KEY_Z = "Z"

    def __init__(
            self,
            printer: Optional[QPrinter],
            parent: QWidget = None,
            offset: QPoint = None,
            title: RState[str] = None,
    ):
        super().__init__(printer)
        self._parent = parent
        self.setWindowTitle(Remember.getValue(title))
        self.setPosition(offset)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.previewWidget = self.findChild(QPrintPreviewWidget)
        self.toolButtons = self.findChildren(QToolButton)
        self.zoomInButton = self.toolButtons[4]
        self.zoomOutButton = self.toolButtons[3]
        # noinspection PyUnresolvedReferences
        QShortcut(QKeySequence(self.KEY_X), self).activated.connect(self.zoomOutButton.click)
        # noinspection PyUnresolvedReferences
        QShortcut(QKeySequence(self.KEY_Z), self).activated.connect(self.zoomInButton.click)
        self.previewWidget.setFocus()

    def setPosition(self, offset: QPoint):
        DqtCanvas.setWindowOffset(self, offset, self._parent)
        return None
