from functools import partial
from typing import Dict, Callable, Iterable

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle

from DeclarativeQt.DqtCore.DqtBase import Remember, OptionKey, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Images.RImage import LutRatio
from DeclarativeQt.Resource.Strings.RString import RString


class BoxLayout(QWidget):
    MinAspectRatio: LutRatio = 0.001
    NoPaddingRatio: LutRatio = 0.0
    DefaultSize: QSize = QSize(40, 40)
    RefuseParentStyle: OptionKey = "RefuseParentStyle"
    AutoAspectRatioFix: OptionKey = "AutoAspectRatioFix"

    def __init__(
            self,
            size: QSize = None,
            options: Iterable = None,
            contentPaddingRatio: float = None,
            fixedAspectRatio: float = None,
            parent: QWidget = None,
            style: RState[str] = None,
            content: RState[QWidget] = None,
            destroyPrevious: bool = False,
            autoContentResize: bool = False,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__(parent)
        self._paddingRatio = Validate(contentPaddingRatio, DqtCanvasBase.DefaultWidgetPaddingRatio)
        self._fixedAspectRatio = None if not fixedAspectRatio else max(self.MinAspectRatio, fixedAspectRatio)
        self._content = content
        self._autoContentResize = autoContentResize
        self._options = options if options else set()
        self.initSize(size)
        self._size = size
        refuseParentStyle = bool(self.RefuseParentStyle in self._options)
        self._style = Validate(style, DqtStyle.emptyStyle(DqtStyle.QWidget) if refuseParentStyle else RString.pEmpty)
        self.setStyleSheet(self._style)
        if isinstance(self._style, Remember):
            self._style.connect(lambda value: self.setStyleSheet(value), host=self)
        if self._content:
            content: QWidget = Remember.getValue(self._content)
            content.setParent(self)
        self._destroyPrevious = destroyPrevious
        if isinstance(self._content, Remember):
            self._content.actConnect(self.updateContent, host=self)
        triggers = triggers if triggers else dict()
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    @property
    def content(self):
        return self._content

    @private
    def initSize(self, size: QSize = None):
        if size:
            self.setFixedSize(size)
        elif self._content:
            content: QWidget = Remember.getValue(self._content)
            self.setFixedSize(DqtCanvas.scaleSingleContentCanvas(content, self._paddingRatio))
        else:
            self.setFixedSize(self.DefaultSize)
        return None

    def paintEvent(self, a0):
        super().paintEvent(a0)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def setStyleSheet(self, styleSheet):
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None

    @private
    def updateContent(self, current: QWidget, previous: QWidget):
        if previous is not None:
            previous.hide()
            previous.setParent(None)
            if self._destroyPrevious:
                previous.deleteLater()
        if current is not None:
            current.setParent(self)
            current.show()
            self.initSize(self._size)
        self.resizeContent()
        return None

    @private
    def resizeContent(self) -> None:
        content: QWidget = Remember.getValue(self._content)
        if not content:
            return None
        if self._autoContentResize:
            DqtCanvas.resizeCentralContent(self, content, self._paddingRatio)
        DqtCanvas.placeCentralContent(self, content)
        return None

    @private
    def sizeScale(self):
        if self._fixedAspectRatio is None and self.AutoAspectRatioFix in self._options:
            self._fixedAspectRatio = self.width() / self.height()
            return None
        DqtCanvas.scaleCanvasAspect(self, self._fixedAspectRatio)
        return None

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.sizeScale()
        self.resizeContent()
        return None
