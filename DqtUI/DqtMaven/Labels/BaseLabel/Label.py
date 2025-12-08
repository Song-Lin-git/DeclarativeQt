from functools import partial
from typing import Callable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QToolTip

from DeclarativeQt.DqtCore.DqtBase import Remember, UiString, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtAlign import DqtAlign
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Strings.RString import RString


class Label(QLabel):
    Align = DqtAlign
    DefaultSize: QSize = QSize(240, 30)
    DefaultInfoTitle: UiString = RString.stLabelMessageBoxTitle[RString.EnglishIndex]

    def __init__(
            self,
            size: QSize = None,
            text: RState[str] = None,
            style: RState[str] = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            parent: QWidget = None,
            onClick: Callable = None,
            alignment: RState[int] = None,
            enable: RState[bool] = True,
            clickInfo: RState[bool] = False,
            infoTitle: RState[str] = None,
            hoverTip: RState[bool] = False,
            tipText: RState[str] = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__()
        size = Validate(size, QSize(self.DefaultSize))
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        self._fixedWidth = None if not fixedWidth else max(fixedWidth, DqtCanvasBase.MinWidth)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        if self._fixedWidth:
            size.setWidth(self._fixedWidth)
        self.setFixedSize(size)
        self.setParent(parent)
        text = Validate(text, RString.pEmpty)
        style = Validate(style, DqtStyle.emptyStyle(DqtStyle.QLabel))
        alignment = Validate(alignment, self.Align.Left | self.Align.VCenter)
        self.setText(text)
        self.setStyleSheet(style)
        self.setAlignment(alignment)
        if isinstance(text, Remember):
            text.connect(lambda value: self.setText(value), host=self)
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        if isinstance(alignment, Remember):
            alignment.connect(lambda value: self.setAlignment(value), host=self)
        self._onClick = onClick
        self._enable = enable
        self._clickInfo = clickInfo
        self._hoverTip = hoverTip
        self._infoTitle = Validate(infoTitle, self.DefaultInfoTitle)
        self._tipText = Validate(tipText, text)
        self.setMouseTracking(True)
        triggers = Validate(triggers, dict())
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        DqtCanvas.setFixedWidth(self, self._fixedWidth)
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        return None

    def enterEvent(self, a0):
        if Remember.getValue(self._hoverTip):
            self.setToolTip(RString.pEmpty)
            # noinspection PyUnresolvedReferences
            QToolTip.showText(a0.globalPos(), Remember.getValue(self._tipText), self)
        super().enterEvent(a0)

    def leaveEvent(self, a0):
        if Remember.getValue(self._hoverTip):
            QToolTip.hideText()
        super().leaveEvent(a0)

    def mouseReleaseEvent(self, ev):
        if not Remember.getValue(self._enable):
            return super().mouseReleaseEvent(ev)
        if Remember.getValue(self._clickInfo):
            QMessageBox.information(self, Remember.getValue(self._infoTitle), self.text())
        elif self._onClick:
            self._onClick()
        return super().mouseReleaseEvent(ev)

    def setAlignment(self, a0: int):
        super().setAlignment(Remember.getValue(a0))
        return None

    def setText(self, text) -> None:
        super().setText(Remember.getValue(text))
        return None

    def setStyleSheet(self, styleSheet) -> None:
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None
