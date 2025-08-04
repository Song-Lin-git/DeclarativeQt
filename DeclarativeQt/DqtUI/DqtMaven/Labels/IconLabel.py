from typing import Callable, Dict

from PyQt5.QtCore import QSize, QSizeF, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, LambdaRemember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.Labels.BaseLabel.Label import Label
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, DictData, Key


class LabelStyle(DqtStyleEditor):
    borderWidth = "borderWidth"
    borderStyle = "borderStyle"
    borderColor = "borderColor"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            borderWidth: RState[int] = None,
            borderRadius: RState[int] = None,
            borderStyle: RState[str] = None,
            backgroundColor: RState[str] = None,
            borderColor: RState[str] = None,
    ):
        styles = DictData(
            Key(self.borderStyle).Val(Validate(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.borderWidth).Val(Validate(borderWidth, int(0))),
            Key(self.borderColor).Val(Validate(borderColor, RColor.hexLightGrey)),
            Key(DqtStyle.atBackgroundColor).Val(Validate(backgroundColor, RColor.qtTransparent)),
            Key(DqtStyle.atFontSize).Val(Validate(fontSize, RFont.fzTinySize)),
            Key(DqtStyle.atFontFamily).Val(Validate(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atBorderRadius).Val(Validate(borderRadius, int(3))),
        ).data
        super().__init__(styleValues=styles)

    def getStyleSheet(self):
        return DqtStyle(
            fontSize=self.getStyle(DqtStyle.atFontSize),
            fontFamily=self.getStyle(DqtStyle.atFontFamily),
            appendix=DictData(
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)), self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor))
            ).data,
            selector=DqtStyle.QLabel
        ).style


class IconLabel(Label):
    DefaultIconRatio: QSizeF = QSizeF(0.9, 0.9)

    def __init__(
            self,
            size: QSize = None,
            iconPixmap: RState[QPixmap] = None,
            iconSizeRatio: QSizeF = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            style: RState[str] = None,
            styleEditor: LabelStyle = None,
            parent: QWidget = None,
            onClick: Callable = None,
            alignment: RState[int] = None,
            hoverTip: RState[bool] = False,
            tipText: RState[str] = None,
            triggers: Dict[Remember, Callable] = None,
            enable: RState[bool] = True,
    ):
        styleEditor = Validate(styleEditor, LabelStyle())
        super().__init__(
            size=size,
            fixedHeight=fixedHeight,
            fixedWidth=fixedWidth,
            style=Validate(style, LambdaRemember(
                *styleEditor.styles.values(), lambdaExp=lambda *az: styleEditor.getStyleSheet()
            )),
            parent=parent,
            onClick=onClick,
            alignment=Validate(alignment, IconLabel.Align.Center),
            hoverTip=hoverTip,
            triggers=triggers,
            enable=enable,
            tipText=tipText
        )
        self.setScaledContents(False)
        self._iconSizeRatio = Validate(iconSizeRatio, self.DefaultIconRatio)
        self._iconPixmap = iconPixmap
        if self._iconPixmap:
            self.setPixmap(self._iconPixmap)
        if isinstance(self._iconPixmap, Remember):
            self._iconPixmap.connect(lambda value: self.setPixmap(value), host=self)

    def setPixmap(self, a0: RState[QPixmap]):
        pixmap: QPixmap = Remember.getValue(a0)
        width = int(self._iconSizeRatio.width() * self.width())
        height = int(self._iconSizeRatio.height() * self.height())
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super().setPixmap(pixmap)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if self._iconPixmap:
            self.setPixmap(self._iconPixmap)
        return None
