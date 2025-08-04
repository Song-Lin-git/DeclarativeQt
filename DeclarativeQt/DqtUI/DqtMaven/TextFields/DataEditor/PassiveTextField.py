from typing import List, Callable, Dict, Any

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BaseTextField.TextField import CompleterMethod
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BorderedTextField import TextFieldStyle
from DeclarativeQt.DqtUI.DqtMaven.TextFields.DataEditor.DataEditor import DataEditor
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, GTuple


class PassiveTextField(DataEditor):
    def __init__(
            self,
            size: QSize = None,
            placehold: str = None,
            data: RState[Any] = None,
            dataType: type = None,
            decimalRound: int = None,
            alignment: RState[int] = None,
            fixedHeight: int = None,
            fixedRadiusRatio: float = None,
            parent: QWidget = None,
            completer: RState[List[str]] = None,
            completerStyle: str = None,
            onCompletered: CompleterMethod = None,
            onValueChange: Callable = None,
            onEdited: Callable = None,
            enable: Remember[bool] = True,
            inputCheck: Remember[bool] = None,
            syncDataTrig: Remember = None,
            passwordMode: RState[bool] = False,
            autoWarning: bool = False,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: TextFieldStyle = None
    ):
        self._isReadOnly = Remember(True)
        styleEditor: TextFieldStyle = Validate(styleEditor, TextFieldStyle())
        styleEditor.setStyle(styleEditor.readOnlyColor, styleEditor.getStyle(DqtStyle.atColor))
        super().__init__(
            size=size,
            placehold=placehold,
            data=data,
            dataType=dataType,
            decimalRound=decimalRound,
            isReadOnly=self._isReadOnly,
            alignment=alignment,
            fixedHeight=fixedHeight,
            inputCheck=inputCheck,
            fixedRadiusRatio=fixedRadiusRatio,
            parent=parent,
            completer=completer,
            completerStyle=completerStyle,
            onCompletered=onCompletered,
            onValueChange=onValueChange,
            autoWarning=autoWarning,
            enable=enable,
            passwordMode=passwordMode,
            syncDataTrig=syncDataTrig,
            onEdited=onEdited,
            triggers=triggers,
            styleEditor=styleEditor
        )

    def finishEditing(self):
        if not Remember.getValue(self._isReadOnly):
            self._isReadOnly.setValue(True)
            self.deselect()
        return None

    def mouseDoubleClickEvent(self, a0):
        super().mouseDoubleClickEvent(a0)
        if Remember.getValue(self._isReadOnly):
            self._isReadOnly.setValue(False)
            self.setFocus()
            self.deselect()
        return None

    def keyPressEvent(self, a0):
        if a0.key() in GTuple(Qt.Key_Return, Qt.Key_Enter, Qt.Key_Escape):
            self.finishEditing()
        super().keyPressEvent(a0)
        return None

    def focusOutEvent(self, a0):
        self.finishEditing()
        super().focusOutEvent(a0)
        return None
