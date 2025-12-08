from functools import partial
from typing import Dict, Union, Tuple, Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox, QDialog, QStyleOption, QStyle

from DeclarativeQt.DqtCore.DqtBase import Remember, OptionKey, OptionFlags, Run, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtMethods.DqtMethods import DqtMethods
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, isValid


class Window(QMainWindow):
    SubWindowArgs = Union[Remember, Tuple[Remember, OptionFlags]]
    DefaultSize: QSize = QSize(400, 300)

    def __init__(
            self,
            minSize: QSize = None,
            fixedSize: QSize = None,
            parent: QWidget = None,
            contentPaddingRatio: float = DqtCanvasBase.DefaultWidgetPaddingRatio,
            title: RState[str] = None,
            style: RState[str] = None,
            content: QWidget = None,
            dialogs: Dict[Union[QDialog, QMessageBox], Remember] = None,
            subWindows: Dict[QMainWindow, SubWindowArgs] = None,
            closeMethod: Callable = None
    ):
        super().__init__(parent)
        self._closeMethod = Validate(closeMethod, lambda: True)
        self._paddingRatio = contentPaddingRatio
        self._content = content
        if self._content:
            self._content.setParent(self)
            minSize = Validate(minSize, DqtCanvas.scaleSingleContentCanvas(self._content, self._paddingRatio))
        if isValid(fixedSize):
            self.setFixedSize(fixedSize)
        elif isValid(minSize):
            self.setMinimumSize(minSize)
        else:
            self.resize(self.DefaultSize)
        if isValid(title):
            self.setWindowTitle(title)
        if isValid(style):
            self.setStyleSheet(style)
        if isinstance(title, Remember):
            title.connect(lambda value: self.setWindowTitle(value), host=self)
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        for k, v in Validate(dialogs, dict()).items():
            k.setParent(self)
            k.setWindowFlag(Qt.Dialog)
            v.connect(partial(k.exec_), host=self)
        DqtMethods.buildSafeShortCutsForWidget(self)
        self.setWindowFlag(Qt.Window)
        self.initSubWindows(subWindows)

    def closeEvent(self, a0):
        if self._closeMethod():
            return super().closeEvent(a0)
        a0.ignore()
        return None

    @private
    def initSubWindows(self, subWindows: Dict[QMainWindow, SubWindowArgs]):
        subWindows = dict() if not subWindows else subWindows.copy()
        for window, val in subWindows.items():
            if window is None:
                continue
            if not isinstance(val, Tuple):
                trigger, options = val, None
            else:
                trigger, options = val
            options = options if options else set()
            if self.IndependentSubWindow not in options:
                window.setParent(self)
            window.setWindowFlag(Qt.Window)
            trigger.connect(lambda: Run(window.show(), window.showNormal()), host=self)
            if self.CloseWindowOption in options:
                trigger.connect(partial(self.close), host=self)
            elif self.HideWindowOption in options:
                trigger.connect(partial(self.hide), host=self)
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

    def setWindowTitle(self, a0):
        super().setWindowTitle(Remember.getValue(a0))
        return None

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        if not self._content:
            return None
        DqtCanvas.resizeCentralContent(self, self._content, self._paddingRatio)
        DqtCanvas.placeCentralContent(self, self._content)
        return None

    NoOption: OptionKey = "NoOption"
    CloseWindowOption: OptionKey = "CloseWindowOption"
    HideWindowOption: OptionKey = "HideWindowOption"
    IndependentSubWindow: OptionKey = "IndependentSubWindow"
