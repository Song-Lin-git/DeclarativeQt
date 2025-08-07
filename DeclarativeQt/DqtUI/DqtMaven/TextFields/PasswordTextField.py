from typing import Callable

from PyQt5.QtCore import QSize, QSizeF

from DeclarativeQt.DqtCore.DqtBase import Remember, Run, ReferState, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtUI.DqtMaven.Labels.IconLabel import IconLabel
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BorderedTextField import BorderedTextField, \
    TextFieldStyle
from DeclarativeQt.DqtUI.DqtWidgets.Container import Row
from DeclarativeQt.Resource.Colors.RColor import RColor, HexColor
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, GList, DataBox, DictData, Key
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Strings.RString import RString


class PasswordTextField(Row):
    DefaultSize = QSize(240, 40)
    DefaultLabelWidth = int(40)
    DefaultHeight = int(30)
    DefaultLabelGap = int(4)
    DefaultBorderRadius = int(5)

    def __init__(
            self,
            size: QSize = None,
            fixedHeight: int = None,
            text: Remember[str] = None,
            enable: RState[bool] = True,
            fontFamily: str = None,
            fontSize: float = None,
            fixedLabelWidth: int = None,
            placehold: str = None,
            labelGap: int = None,
            borderRadius: int = None,
            validityCheck: bool = True,
            validityCheckMethod: Callable = None,
            correction: Remember[bool] = None,
            onValueChange: Callable = None,
    ):
        text = Validate(text, Remember[str](RString.pEmpty))
        self._size = Validate(size, QSize(self.DefaultSize))
        self._fixedLabelWidth = Validate(fixedLabelWidth, self.DefaultLabelWidth)
        self._fixedHeight = Validate(fixedHeight, self.DefaultHeight)
        self._labelGap = Validate(labelGap, self.DefaultLabelGap)
        self._borderRadius = Validate(borderRadius, self.DefaultBorderRadius)
        visible = Remember[bool](False)
        validity = Remember[bool](True)
        correction = Validate(correction, Remember(True))
        validityCheckMethod = Validate(validityCheckMethod, self.passwordValidityCheck)
        super().__init__(
            autoContentResize=True,
            spacing=self._labelGap,
            options=GList(Row.AutoSizeNoRemain),
            padding=int(0),
            arrangement=Row.Align.Left,
            alignment=Row.Align.VCenter,
            content=GList(
                BorderedTextField(
                    size=self._size,
                    fixedHeight=self._fixedHeight,
                    text=text,
                    styleEditor=TextFieldStyle(
                        fontFamily=fontFamily,
                        fontSize=fontSize,
                        borderRadius=self._borderRadius,
                        focusedBorder=ReferState(
                            *GList(validity, text, correction),
                            lambdaExp=lambda a0, a1, a2: HexColor(
                                RColor.hexRed if not a2 or bool(
                                    len(a1) > 0 and validityCheck and not a0
                                ) else RColor.hexBlack
                            )
                        ),
                        unfocusedBorder=ReferState(
                            *GList(validity, text, correction),
                            lambdaExp=lambda a0, a1, a2: HexColor(
                                RColor.hexRed if not a2 or bool(
                                    len(a1) > 0 and validityCheck and not a0
                                ) else RColor.hexDarkGrey
                            )
                        ),
                    ),
                    enable=enable,
                    placehold=placehold,
                    passwordMode=ReferState(visible, lambdaExp=lambda a0: not visible.value()),
                    onValueChange=lambda: Run(
                        onValueChange(), text.setValue(RString.eraseBlank(text.value())),
                        validity.setValue(validityCheckMethod(text)) if validityCheck else None,
                    ),
                ),
                IconLabel(
                    fixedHeight=self._fixedHeight,
                    fixedWidth=self._fixedLabelWidth,
                    alignment=IconLabel.Align.Center,
                    enable=enable,
                    style=ReferState(
                        visible, lambdaExp=lambda a0: DqtStyle(
                            selector=DqtStyle.QLabel,
                            appendix=DictData(
                                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                                    DqtStyle.Px(int(1)), DqtStyle.valBorderSolid, RColor.hexLightGrey
                                )),
                                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self._borderRadius)),
                                Key(DqtStyle.atBackgroundColor).Val(RColor.qtTransparent),
                            ).data
                        ).style if a0 else DqtStyle(
                            selector=DqtStyle.QLabel,
                            appendix=DictData(
                                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                                    DqtStyle.Px(int(1)), DqtStyle.valBorderSolid, RColor.qtTransparent
                                )),
                                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self._borderRadius)),
                                Key(DqtStyle.atBackgroundColor).Val(RColor.qtTransparent),
                            ).data
                        ).style
                    ),
                    iconSizeRatio=QSizeF(0.7, 0.7),
                    iconPixmap=ReferState(
                        visible, lambdaExp=lambda a0: DataBox(
                            RIcon().loadIconPixmap(RIcon.Src.visibility_dark) if a0 else
                            RIcon().loadIconPixmap(RIcon.Src.visibility_off_light)
                        ).data
                    ),
                    onClick=lambda: Run(visible.setValue(not visible.value())),
                )
            ),
        )

    @staticmethod
    def passwordValidityCheck(password: RState[str]):
        digits = RString.Digits
        letters = RString.Letters
        min_length = 8
        special_char = RString.pSpecialChars
        password_value = Remember.getValue(password)
        if len(password_value) < min_length:
            return False
        for p in password_value:
            if p not in digits and p not in letters and p not in special_char:
                return False
        return True
