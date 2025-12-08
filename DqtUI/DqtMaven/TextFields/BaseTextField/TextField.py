from functools import partial
from typing import Union, Callable, Dict, List, Any

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLineEdit

from DeclarativeQt.DqtCore.DqtBase import Remember, Run, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtAlign import DqtAlign
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember
from DeclarativeQt.DqtUI.DqtTools import Completer
from DeclarativeQt.DqtUI.DqtTools.AppMenu import AppMenuStyle
from DeclarativeQt.DqtUI.DqtTools.Completer import CompleterStyle
from DeclarativeQt.Resource.Colors.RColor import HexColor, RColor
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, GTuple, GStr, isValid
from DeclarativeQt.Resource.Grammars.RGrmBase.RGrmObject import DataBox
from DeclarativeQt.Resource.Strings.RString import RString

CompleterMethod = Union[Callable[[bool], Any], Callable]


class TextField(QLineEdit):
    Align = DqtAlign
    DefaultSize: QSize = QSize(240, 30)
    PlaceholdColor: HexColor = RColor.hexLightGrey

    def __init__(
            self,
            size: QSize = None,
            placehold: str = None,
            text: RState[str] = None,
            style: RState[str] = None,
            alignment: RState[int] = None,
            fixedHeight: int = None,
            parent: QWidget = None,
            completer: RState[List[str]] = None,
            completerStyle: CompleterStyle = None,
            onCompletered: CompleterMethod = None,
            onValueChange: Callable = None,
            enable: RState[bool] = True,
            isReadOnly: RState[bool] = False,
            passwordMode: RState[bool] = False,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__()
        size = Validate(size, QSize(self.DefaultSize))
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        self.setFixedSize(size)
        self.setParent(parent)
        style = Validate(style, DqtStyle.emptyStyle(DqtStyle.QLineEdit))
        alignment = Validate(alignment, self.Align.Left)
        self.setStyleSheet(style)
        self.setAlignment(alignment)
        self._text = ValToRemember(Validate(text, RString.pEmpty))
        self.setText(self._text)
        if placehold:
            self.setPlaceholderText(placehold)
        if Remember.getValue(passwordMode):
            self.setEchoMode(QLineEdit.Password)
        self.setEnabled(enable)
        self.setReadOnly(isReadOnly)
        if isinstance(self._text, Remember):
            self._text.connect(lambda value: self.setText(value), host=self)
            self._text.connect(partial(Validate(onValueChange, lambda: None)), host=self)
            # noinspection PyUnresolvedReferences
            self.textChanged.connect(lambda: self.setText(Remember.getValue(self._text)))
            # noinspection PyUnresolvedReferences
            self.textEdited.connect(lambda: self._text.setValue(self.text()))
        self._completer = Validate(completer, list())
        self._completered = Remember(False)
        self.buildCompleter(completerStyle)
        if onCompletered:
            self._completered.connect(partial(onCompletered), host=self)
        if isinstance(self._completer, Remember):
            self._completer.connect(partial(self.buildCompleter, completerStyle), host=self)
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        if isinstance(alignment, Remember):
            alignment.connect(lambda value: self.setAlignment(value), host=self)
        if isinstance(enable, Remember):
            enable.connect(lambda value: self.setEnabled(value), host=self)
        if isinstance(isReadOnly, Remember):
            isReadOnly.connect(lambda value: self.setReadOnly(value), host=self)
        if isinstance(passwordMode, Remember):
            passwordMode.connect(lambda value: Run(self.setPasswordMode(value)), host=self)
        triggers = triggers if triggers else dict()
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def setPasswordMode(self, isPassword: bool):
        echoMode = QLineEdit.Password if isPassword else QLineEdit.Normal
        self.setEchoMode(echoMode)
        return None

    def setCompleterMethod(self, method: CompleterMethod = None):
        self._completered.disconnect(host=self)
        if isValid(method):
            self._completered.connect(partial(method), host=self)
        return None

    @private
    def buildCompleter(self, complterStyle: CompleterStyle = None):
        datas = Remember.getValue(self._completer)
        showMethod = lambda: self._completered.setValue(True)
        hideMethod = lambda: self._completered.setValue(False)
        completer = DataBox(Completer.buildCompleterForLineEdit(
            dataModel=datas, lineEdit=self,
            onCompleterShow=partial(showMethod),
            onCompleterHide=partial(hideMethod),
            styleEditor=complterStyle,
        )).data
        if completer and isinstance(self._text, Remember):
            # noinspection PyUnresolvedReferences
            completer.activated.connect(lambda value: self._text.setValue(value))
        return None

    def contextMenuEvent(self, a0):
        menu = self.createStandardContextMenu()
        menu.setStyleSheet(AppMenuStyle().getStyleSheet())
        menu.move(a0.globalPos())
        menu.exec_()
        return None

    def keyPressEvent(self, a0):
        if self.completer() and self.completer().popup().isVisible():
            if a0.key() in GTuple(Qt.Key_Up, Qt.Key_Down):
                self.setText(self._text)
                return None
            if a0.key() in GTuple(Qt.Key_Return, Qt.Key_Enter):
                data = self.completer().popup().currentIndex().data()
                if isValid(data):
                    self._text.setValue(data)
                self.completer().popup().hide()
                return None
        return super().keyPressEvent(a0)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        return None

    def setReadOnly(self, a0):
        super().setReadOnly(Remember.getValue(a0))
        return None

    def setEnabled(self, a0):
        super().setEnabled(Remember.getValue(a0))
        return None

    def setAlignment(self, a0):
        super().setAlignment(Remember.getValue(a0))
        return None

    def setText(self, a0: Union[RState[str], Any]):
        a0 = GStr(Remember.getValue(a0))
        if self.text() != a0:
            cursorAt, adjust = self.cursorPosition(), True
            if cursorAt >= len(self.text()) or cursorAt >= len(a0):
                adjust = False
            super().setText(a0)
            if adjust:
                self.setCursorPosition(cursorAt)
        return None

    def setStyleSheet(self, styleSheet):
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None
