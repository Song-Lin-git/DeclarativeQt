from functools import partial
from typing import Callable, Dict, List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BaseButton.Button import Button
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate, NxLimitVal


class ButtonStyle(DqtStyleEditor):
    borderStyle = "borderStyle"
    borderWidth = "borderWidth"
    borderColor = "borderColor"
    pressedBorder = "pressedBorder"
    pressedBackground = "pressedBackground"
    disabledBorder = "disabledBorder"
    disabledColor = "disabledColor"
    disabledBackground = "disabledBackground"
    hoverBackground = "hoverBackground"
    hoverBorder = "hoverBorder"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            textColor: RState[str] = None,
            borderWidth: RState[int] = None,
            borderColor: RState[str] = None,
            borderStyle: RState[str] = None,
            borderRadius: RState[int] = None,
            backgroundColor: RState[str] = None,
            pressedBackground: RState[str] = None,
            pressedBorder: RState[str] = None,
            disabledBackground: RState[str] = None,
            disabledColor: RState[str] = None,
            disabledBorder: RState[str] = None,
            hoverBackground: RState[str] = None,
            hoverBorder: RState[str] = None,
    ):
        hoverSkyBlue: str = RColor().setQStyleAlpha(RColor.hexSkyBlue, alpha=0.1)
        clickSkyBlue: str = RColor().setQStyleAlpha(RColor.hexSkyBlue, alpha=0.6)
        self._styles: dict = DictData(
            Key(DqtStyle.atFontFamily).Val(Validate(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atColor).Val(Validate(textColor, RColor.hexBlack)),
            Key(DqtStyle.atFontSize).Val(Validate(fontSize, RFont.fzSmallSize)),
            Key(self.borderWidth).Val(Validate(borderWidth, 1)),
            Key(self.borderColor).Val(Validate(borderColor, RColor.hexGrey)),
            Key(self.borderStyle).Val(Validate(borderStyle, DqtStyle.valBorderSolid)),
            Key(DqtStyle.atBorderRadius).Val(Validate(borderRadius, 10)),
            Key(DqtStyle.atBackgroundColor).Val(Validate(backgroundColor, RColor.hexWhite)),
            Key(self.pressedBorder).Val(Validate(pressedBorder, RColor.hexBlack)),
            Key(self.pressedBackground).Val(Validate(pressedBackground, clickSkyBlue)),
            Key(self.disabledColor).Val(Validate(disabledColor, RColor.hexGrey)),
            Key(self.disabledBackground).Val(Validate(disabledBackground, RColor.hexWhite)),
            Key(self.disabledBorder).Val(Validate(disabledBorder, RColor.hexLightGrey)),
            Key(self.hoverBackground).Val(Validate(hoverBackground, hoverSkyBlue)),
            Key(self.hoverBorder).Val(Validate(hoverBorder, RColor.hexDarkGrey)),
        ).data
        super().__init__(self._styles)

    def getStyleSheet(self) -> str:
        return DqtStyle(
            fontFamily=self.getStyle(DqtStyle.atFontFamily),
            fontSize=self.getStyle(DqtStyle.atFontSize),
            color=self.getStyle(DqtStyle.atColor),
            appendix=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
            ).data,
            selector=DqtStyle.QPushButton,
        ).appendStyle(
            DqtStyle.QPushButtonHover, styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.hoverBackground)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.hoverBorder),
                )),
            ).data
        ).appendStyle(
            DqtStyle.QPushButtonPressd, styles=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.pressedBorder),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.pressedBackground)),
            ).data
        ).appendStyle(
            DqtStyle.QPushButtonDisabled, styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(self.disabledColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.disabledBorder),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.disabledBackground))
            ).data
        ).style


class BorderedButton(Button):
    MaxRadiusRatio, MinRadiusRatio = 0.5, 0.001

    def __init__(
            self,
            size: QSize = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            text: RState[str] = None,
            parent: QWidget = None,
            onClick: Callable = None,
            enable: RState[bool] = True,
            fixedAspectRatio: float = None,
            fixedRadiusRatio: float = None,
            shortCut: QKeySequence = None,
            shortCuts: List[QKeySequence] = None,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: ButtonStyle = None
    ):
        super().__init__(
            size=size,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            text=text,
            parent=parent,
            fixedAspectRatio=fixedAspectRatio,
            onClick=onClick,
            enable=enable,
            shortCut=shortCut,
            shortCuts=shortCuts,
            triggers=triggers
        )
        self._styleEditor = styleEditor if styleEditor else ButtonStyle()
        self._fixedRadiusRatio = NxLimitVal(fixedRadiusRatio, self.MinRadiusRatio, self.MaxRadiusRatio)
        self.updateStyle()
        self.updateBorderRadius()
        for v in self._styleEditor.styles.values():
            if isinstance(v, Remember):
                v.connect(partial(self.updateStyle), host=self)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.updateBorderRadius()
        return None

    @private
    def updateStyle(self) -> None:
        self.setStyleSheet(self._styleEditor.getStyleSheet())
        return None

    @private
    def updateBorderRadius(self) -> None:
        if self._fixedRadiusRatio:
            radius = int(self._fixedRadiusRatio * min(self.width(), self.height()))
            self._styleEditor.setStyle(DqtStyle.atBorderRadius, radius)
            self.updateStyle()
        return None
