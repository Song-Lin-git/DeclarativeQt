from functools import partial
from typing import Dict, Union

from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog, QStyleOption, QStyle

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtMethods.DqtMethods import DqtMethods
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, DictData, Key
from DeclarativeQt.Resource.Strings.RString import RString


class Dialog(QDialog):
    Accepted = QDialog.Accepted
    Rejected = QDialog.Rejected
    DefaultSize: QSize = QSize(400, 400)

    def __init__(
            self,
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
        super().__init__(parent)
        self._paddingRatio = Validate(contentPaddingRatio, DqtCanvasBase.DefaultWidgetPaddingRatio)
        self._content = content
        self.setAttribute(Qt.WA_DeleteOnClose)
        if self._content:
            self._content.setParent(self)
            size = Validate(size, DqtCanvas.scaleSingleContentCanvas(self._content, self._paddingRatio))
        size = Validate(size, QSize(self.DefaultSize))
        self.resize(size)
        self._fixSize = fixSize
        self._fixWidth = fixWidth
        if fixedHeight:
            self.setFixedHeight(fixedHeight)
        if fixedWidth:
            self.setFixedWidth(fixedWidth)
        self.setPosition(offset)
        self.setWindowFlag(Qt.Dialog)
        title = Validate(title, RString.pEmpty)
        self.setWindowTitle(title)
        if isinstance(title, Remember):
            title.connect(lambda value: self.setWindowTitle(value), host=self)
        style = Validate(style, RString.pEmpty)
        self.setStyleSheet(style)
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        self._subDialogs = Validate(subDialogs, dict())
        for k, v in self._subDialogs.items():
            k.setParent(self)
            k.setWindowFlag(Qt.Dialog)
            v.connect(partial(k.exec_), host=self)
        triggers = DictData(
            Key(closeTrig).Val(partial(self.close)),
            Key(acceptTrig).Val(partial(self.accept))
        ).data
        for k, v in triggers.items():
            if isinstance(k, Remember):
                k.connect(partial(v), host=self)
        if maximizeHint:
            self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        DqtMethods.buildSafeShortCutsForWidget(self)

    def setPosition(self, offset: QPoint):
        DqtCanvas.setWindowOffset(self, offset, self.parent())
        return None

    def setStyleSheet(self, styleSheet):
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None

    def setWindowTitle(self, a0):
        super().setWindowTitle(Remember.getValue(a0))
        return None

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        if self._fixWidth:
            self.setFixedWidth(self.width())
        if self._fixSize:
            self.setFixedSize(self.size())
        if not self._content:
            return None
        DqtCanvas.resizeCentralContent(self, self._content, self._paddingRatio)
        DqtCanvas.placeCentralContent(self, self._content)
        return None

    def paintEvent(self, a0):
        super().paintEvent(a0)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
