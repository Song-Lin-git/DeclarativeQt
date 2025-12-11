from functools import partial
from typing import Callable, Dict, List

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BaseTextField.TextField import TextField, CompleterMethod
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, DataBox, GList, DictData, Key


class TextFieldStyle(DqtStyleEditor):
    passwordFamily = "passwordFamily"
    passwordSize = "passwordSize"
    borderColor = "borderColor"
    borderWidth = "borderWidth"
    borderStyle = "borderStyle"
    placeholderFamily = "placeholderFamily"
    placeholderColor = "placeholderColor"
    placeholderSize = "placeholderSize"
    focusedBackground = "focusedBackground"
    focusedBorder = "focusedBorder"
    unfocusedBackground = "unfocusedBackground"
    unfocusedBorder = "unfocusedBorder"
    disabledColor = "disabledColor"
    disabledBackground = "disabledBackground"
    disabledBorder = "disabledBorder"
    readOnlyColor = "readOnlyColor"
    readOnlyBackground = "readOnlyBackground"
    readOnlyBorder = "readOnlyBorder"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            textColor: RState[str] = None,
            borderColor: RState[str] = None,
            borderStyle: RState[str] = None,
            borderWidth: RState[int] = None,
            borderRadius: RState[int] = None,
            backgroundColor: RState[str] = None,
            passwordFamily: RState[str] = None,
            passwordSize: RState[float] = None,
            placeholderFamily: RState[str] = None,
            placeholderSize: RState[float] = None,
            placeholderColor: RState[str] = None,
            focusedBackground: RState[str] = None,
            focusedBorder: RState[str] = None,
            unfocusedBackground: RState[str] = None,
            unfocusedBorder: RState[str] = None,
            disabledColor: RState[str] = None,
            disabledBackground: RState[str] = None,
            disabledBorder: RState[str] = None,
            readOnlyColor: RState[str] = None,
            readOnlyBackground: RState[str] = None,
            readOnlyBorder: RState[str] = None,
    ):
        self._styles: dict = DictData(
            Key(DqtStyle.atFontFamily).Val(Remember.toValid(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atFontSize).Val(Remember.toValid(fontSize, float(RFont.fzSmallSize))),
            Key(DqtStyle.atColor).Val(Remember.toValid(textColor, RColor.hexBlack)),
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, RColor.hexWhite)),
            Key(DqtStyle.atBorderRadius).Val(Remember.toValid(borderRadius, int(5))),
            Key(self.passwordFamily).Val(Remember.toValid(passwordFamily, RFont.TNR)),
            Key(self.passwordSize).Val(Remember.toValid(passwordSize, float(10.0))),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
            Key(self.borderColor).Val(Remember.toValid(borderColor, RColor.hexGrey)),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.placeholderFamily).Val(Remember.toValid(placeholderFamily, RFont.YaHei)),
            Key(self.placeholderColor).Val(Remember.toValid(placeholderColor, RColor.hexBlack)),
            Key(self.placeholderSize).Val(Remember.toValid(placeholderSize, float(10.8))),
            Key(self.focusedBorder).Val(Remember.toValid(focusedBorder, RColor.hexBlack)),
            Key(self.focusedBackground).Val(Remember.toValid(focusedBackground, self.DefaultFocusedBackground)),
            Key(self.unfocusedBorder).Val(Remember.toValid(unfocusedBorder, RColor.hexDarkGrey)),
            Key(self.unfocusedBackground).Val(Remember.toValid(unfocusedBackground, RColor.hexWhite)),
            Key(self.disabledBackground).Val(Remember.toValid(disabledBackground, RColor.hexWhite)),
            Key(self.disabledColor).Val(Remember.toValid(disabledColor, RColor.hexDarkGrey)),
            Key(self.disabledBorder).Val(Remember.toValid(disabledBorder, RColor.hexGrey)),
            Key(self.readOnlyBackground).Val(Remember.toValid(readOnlyBackground, RColor.hexWhite)),
            Key(self.readOnlyColor).Val(Remember.toValid(readOnlyColor, RColor.hexDarkGrey)),
            Key(self.readOnlyBorder).Val(Remember.toValid(readOnlyBorder, RColor.hexGrey)),
        ).data
        super().__init__(self._styles)

    def getStyleSheet(self, passwordMode: bool = False):
        return DqtStyle(
            fontFamily=str(
                self.getStyle(self.passwordFamily) if Remember.getValue(passwordMode) else
                self.getStyle(DqtStyle.atFontFamily)
            ),
            fontSize=float(
                self.getStyle(self.passwordSize) if Remember.getValue(passwordMode) else
                self.getStyle(DqtStyle.atFontSize)
            ),
            color=self.getStyle(DqtStyle.atColor),
            selector=DqtStyle.QLineEdit,
            appendix=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
            ).data
        ).appendStyle(
            apply=DqtStyle.QLineEditPlaceholder,
            styles=DictData(
                Key(DqtStyle.atFontFamily).Val(self.getStyle(self.placeholderFamily)),
                Key(DqtStyle.atFontSize).Val(DqtStyle.Pt(self.getStyle(self.placeholderSize))),
                Key(DqtStyle.atColor).Val(self.getStyle(self.placeholderColor)),
            ).data
        ).appendStyle(
            apply=DqtStyle.QLineEditDisabled,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(self.disabledColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.disabledBorder)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.disabledBackground))
            ).data
        ).appendStyle(
            apply=DqtStyle.QLineEditFocused,
            styles=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.focusedBorder)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.focusedBackground)),
            ).data
        ).appendStyle(
            apply=DqtStyle.QLineEditUnfocused,
            styles=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.unfocusedBorder)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.unfocusedBackground)),
            ).data
        ).appendStyle(
            apply=DqtStyle.QLineEditReadOnly,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(self.readOnlyColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.readOnlyBorder)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.readOnlyBackground)),
            ).data
        ).style

    DefaultFocusedBackground = RColor().setQStyleAlpha(color=RColor.hexPureMist, alpha=0.6)


class BorderedTextField(TextField):
    MaxRadiusRatio, MinRadiusRatio = 0.5, 0.001

    def __init__(
            self,
            size: QSize = None,
            placehold: str = None,
            text: RState[str] = None,
            alignment: RState[int] = None,
            isReadOnly: RState[bool] = False,
            fixedHeight: int = None,
            fixedRadiusRatio: float = None,
            parent: QWidget = None,
            completer: RState[List[str]] = None,
            onCompletered: CompleterMethod = None,
            completerStyle: str = None,
            onValueChange: Callable = None,
            enable: RState[bool] = True,
            passwordMode: RState[bool] = False,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: TextFieldStyle = None
    ):
        super().__init__(
            size=size,
            placehold=placehold,
            text=text,
            fixedHeight=fixedHeight,
            triggers=triggers,
            parent=parent,
            onValueChange=onValueChange,
            alignment=alignment,
            onCompletered=onCompletered,
            completer=completer,
            completerStyle=completerStyle,
            enable=enable,
            passwordMode=passwordMode,
            isReadOnly=isReadOnly
        )
        self._passwordMode = passwordMode
        self._styleEditor: TextFieldStyle = Validate(styleEditor, TextFieldStyle())
        self._fixedRadiusRatio = None if not fixedRadiusRatio else DataBox(max(
            min(self.MaxRadiusRatio, fixedRadiusRatio), self.MinRadiusRatio
        )).data
        self.updateStyle()
        self.updateBorderRadius()
        for v in list(self._styleEditor.styles.values()) + GList(self._passwordMode, text):
            if isinstance(v, Remember):
                v.connect(partial(self.updateStyle), host=self)
        if not isinstance(text, Remember):
            # noinspection PyUnresolvedReferences
            self.textChanged.connect(partial(self.updateStyle))

    @private
    def updateStyle(self):
        self.setStyleSheet(self._styleEditor.getStyleSheet(self._passwordMode))
        return None

    @private
    def updateBorderRadius(self):
        if self._fixedRadiusRatio:
            radius = int(self._fixedRadiusRatio * min(self.width(), self.height()))
            self._styleEditor.setStyle(DqtStyle.atBorderRadius, radius)
            self.updateStyle()
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.updateBorderRadius()
        return None
