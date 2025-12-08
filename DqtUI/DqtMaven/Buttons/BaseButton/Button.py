from functools import partial
from typing import Callable, Dict, Iterable, Tuple, List, Optional

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QPushButton, QWidget, QShortcut

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import Callback
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, isEmpty, GTuple, GList, PureList
from DeclarativeQt.Resource.Images.RImage import LutRatio
from DeclarativeQt.Resource.Strings.RString import RString

KeyHint = QKeySequence


class Button(QPushButton):
    DefaultSize: QSize = QSize(120, 30)
    MinAspectRatio: LutRatio = 0.001

    def __init__(
            self,
            size: QSize = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            text: RState[str] = None,
            style: RState[str] = None,
            parent: QWidget = None,
            onClick: Callable = None,
            fixedAspectRatio: float = None,
            enable: RState[bool] = True,
            shortCut: KeyHint = None,
            shortCuts: Iterable[KeyHint] = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__()
        size = Validate(size, QSize(self.DefaultSize))
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        self._fixedWidth = None if not fixedWidth else max(fixedWidth, DqtCanvasBase.MinWidth)
        self._fixedAspectRatio = None if not fixedAspectRatio else max(self.MinAspectRatio, fixedAspectRatio)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        if self._fixedWidth:
            size.setWidth(self._fixedWidth)
        self.setFixedSize(size)
        self.sizeScale()
        self.setParent(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        text = Validate(text, RString.pEmpty)
        style = Validate(style, DqtStyle.emptyStyle(DqtStyle.QPushButton))
        self.setEnabled(Remember.getValue(enable))
        self.setText(text)
        self.setStyleSheet(style)
        if isinstance(text, Remember):
            text.connect(lambda value: self.setText(value), host=self)
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        if isinstance(enable, Remember):
            enable.connect(lambda value: self.setEnabled(value), host=self)
        if onClick:
            # noinspection PyUnresolvedReferences
            self.clicked.connect(Callback(self, onClick))
        self._shortCuts = list()
        shortCuts = Validate(shortCuts, GList(shortCut))
        self.initShortCuts(shortCuts)
        triggers = dict() if not triggers else triggers
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def restoreShortCuts(self):
        if isEmpty(self._shortCuts):
            return None
        self.setShortcut(self._shortCuts[0])
        for opt in self._shortCuts[1:]:
            opt.setEnabled(True)
        return None

    def disableShortCuts(self):
        if isEmpty(self._shortCuts):
            return None
        keyEmpty = QKeySequence()
        self.setShortcut(keyEmpty)
        for opt in self._shortCuts[1:]:
            opt.setEnabled(False)
        return None

    @private
    def initShortCuts(self, shortCuts: Iterable[KeyHint] = None):
        shortCuts = PureList(list(shortCuts))
        if isEmpty(shortCuts):
            return None
        self.setShortcut(shortCuts[0])
        self._shortCuts.append(shortCuts[0])
        for key in shortCuts[1:]:
            opt = QShortcut(key, self)
            # noinspection PyUnresolvedReferences
            opt.activated.connect(partial(self.click))
            self._shortCuts.append(opt)
        return None

    @property
    def shortcuts(self) -> Tuple[Optional[KeyHint], List[QShortcut]]:
        if isEmpty(self._shortCuts):
            return GTuple(None, list())
        return GTuple(self._shortCuts[0], self._shortCuts[1:])

    @private
    def sizeScale(self):
        if self._fixedWidth or self._fixedHeight:
            return None
        if self._fixedAspectRatio is not None:
            DqtCanvas.scaleCanvasAspect(self, self._fixedAspectRatio)
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        DqtCanvas.setFixedWidth(self, self._fixedWidth)
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        self.sizeScale()
        return None

    def setText(self, text) -> None:
        super().setText(Remember.getValue(text))
        return None

    def setStyleSheet(self, styleSheet) -> None:
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None
