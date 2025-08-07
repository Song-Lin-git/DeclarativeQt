from decimal import Decimal
from functools import partial
from typing import List, Callable, Dict, Any

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, ReferState, RState
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BaseTextField.TextField import CompleterMethod
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BorderedTextField import BorderedTextField, \
    TextFieldStyle
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, GList, isEmpty, DictData, Key
from DeclarativeQt.Resource.PhyMetrics.PhyMtrBase.PhyMtrBase import PhyMeasure
from DeclarativeQt.Resource.Strings.RString import RString


class DataEditor(BorderedTextField):
    DefaultSize: QSize = QSize(180, 30)
    FocusedBackgroundColor: str = RColor.setQStyleAlpha(RColor.hexWhite, 0.94)
    WarningBackgroundColor: str = RColor.setQStyleAlpha(RColor.hexSalmonPink, 0.1)
    WarningBorderColor: str = RColor.setQStyleAlpha(RColor.hexDeepCrimson, 0.97)

    def __init__(
            self,
            size: QSize = None,
            placehold: str = None,
            data: RState[Any] = None,
            dataType: type = None,
            decimalRound: int = None,
            alignment: RState[int] = None,
            isReadOnly: RState[bool] = False,
            fixedHeight: int = None,
            fixedRadiusRatio: float = None,
            parent: QWidget = None,
            completer: RState[List[str]] = None,
            onCompletered: CompleterMethod = None,
            completerStyle: str = None,
            onValueChange: Callable = None,
            onEdited: Callable = None,
            inputCheck: Remember[bool] = None,
            autoWarning: bool = False,
            enable: RState[bool] = True,
            syncDataTrig: Remember = None,
            passwordMode: RState[bool] = False,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: TextFieldStyle = None
    ):
        data = ValToRemember(data)
        dataVal = lambda: Remember.getValue(data)
        dataType = Validate(dataType, type(dataVal()))
        fixData = lambda: Validate(dataVal(), RString.pEmpty)
        dataPiece = lambda: str(fixData())
        if dataType in GList(float, Decimal):
            decimalRound = Validate(decimalRound, PhyMeasure.DecimalRound)
            dataPiece = lambda: RString.decimalRound(fixData(), decimalRound)
        dataStr = Remember(dataPiece())
        isInputValid = lambda: not isEmpty(dataStr.value())
        checkInputValue = lambda: RString.checkValue(dataStr.value(), dataType) if isInputValid() else True
        inputCheck = Validate(inputCheck, Remember(checkInputValue()))
        styleEditor = Validate(styleEditor, TextFieldStyle())
        if autoWarning:
            self.setAutoWarningStyle(styleEditor, inputCheck)
        self._optSyncData = lambda: dataStr.setValue(dataPiece())
        super().__init__(
            size=size,
            placehold=placehold,
            text=dataStr,
            isReadOnly=isReadOnly,
            alignment=alignment,
            fixedHeight=fixedHeight,
            fixedRadiusRatio=fixedRadiusRatio,
            parent=parent,
            completer=completer,
            completerStyle=completerStyle,
            onCompletered=onCompletered,
            onValueChange=onEdited,
            enable=enable,
            passwordMode=passwordMode,
            triggers=triggers,
            styleEditor=styleEditor
        )
        dataStr.connect(lambda a0: inputCheck.setValue(checkInputValue()), host=self)
        if isinstance(data, Remember):
            self.textEdited.connect(lambda: data.setValue(RString.matchOne(dataStr.value(), dataType)))
            data.connect(partial(Validate(onValueChange, lambda: None)), host=self)
        if isinstance(syncDataTrig, Remember):
            syncDataTrig.connect(partial(self._optSyncData), host=self)

    def keyPressEvent(self, a0) -> None:
        if a0.modifiers() & Qt.ControlModifier and a0.key() in GList(Qt.Key_Enter, Qt.Key_Return):
            syncData = partial(self._optSyncData)
            syncData()
            a0.accept()
            return None
        return super().keyPressEvent(a0)

    @staticmethod
    def setAutoWarningStyle(styleEditor: TextFieldStyle, checkMark: Remember[bool]) -> Dict[str, Any]:
        warningBackground = DataEditor.WarningBackgroundColor
        warningBorder = DataEditor.WarningBorderColor
        focusedBorderExp = lambda a0: warningBorder if not a0 else RColor.hexBlack
        unfocusedBorderExp = lambda a0: warningBorder if not a0 else RColor.hexDarkGrey
        focusedBackgroundExp = lambda a0: warningBackground if not a0 else DataEditor.FocusedBackgroundColor
        unfocusedBackgroundExp = lambda a0: warningBackground if not a0 else RColor.hexWhite
        status = ReferState
        for key, val in DictData(
                Key(styleEditor.focusedBorder).Val(status(checkMark, lambdaExp=focusedBorderExp)),
                Key(styleEditor.unfocusedBorder).Val(status(checkMark, lambdaExp=unfocusedBorderExp)),
                Key(styleEditor.focusedBackground).Val(status(checkMark, lambdaExp=focusedBackgroundExp)),
                Key(styleEditor.unfocusedBackground).Val(status(checkMark, lambdaExp=unfocusedBackgroundExp)),
        ).data.items():
            styleEditor.setStyle(key, val)
        return styleEditor.styles
