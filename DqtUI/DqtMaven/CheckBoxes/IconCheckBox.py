from typing import Callable, Dict

from PyQt5.QtCore import QSize, QSizeF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.CheckBoxes.BaseCheckBox.CheckBox import CheckBox
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate
from DeclarativeQt.Resource.Images.RIcon import RIcon


class CheckBoxStyle(DqtStyleEditor):
    checkedIcon = "checkedIcon"
    uncheckedIcon = "uncheckedIcon"
    iconSizeRatio = "iconSizeRatio"
    hoverColor = "hoverColor"
    pressedColor = "pressedColor"

    def __init__(
            self,
            textFont: RState[str] = None,
            fontSize: RState[float] = None,
            textColor: RState[str] = None,
            hoverColor: RState[str] = None,
            pressedColor: RState[str] = None,
            checkedIcon: RState[str] = None,
            uncheckedIcon: RState[str] = None,
            iconSizeRatio: QSizeF = None
    ):
        self._styles = DictData(
            Key(DqtStyle.atFontSize).Val(Remember.toValid(fontSize, RFont.fzSmallSize)),
            Key(DqtStyle.atColor).Val(Remember.toValid(textColor, RColor.hexBlack)),
            Key(DqtStyle.atFontFamily).Val(Remember.toValid(textFont, RFont.YaHei)),
            Key(self.checkedIcon).Val(Remember.toValid(checkedIcon, self.DefaultCheckedIcon)),
            Key(self.uncheckedIcon).Val(Remember.toValid(uncheckedIcon, self.DefaultUncheckedIcon)),
            Key(self.iconSizeRatio).Val(Remember.toValid(iconSizeRatio, self.DefaultIconSizeRatio)),
            Key(self.hoverColor).Val(Remember.toValid(hoverColor, self.DefaultHoverColor)),
            Key(self.pressedColor).Val(Remember.toValid(pressedColor, self.DefaultPressedColor))
        ).data
        super().__init__(self._styles)

    def getStyleSheet(self, size: QSize, checked: bool):
        iconRatio = self.getStyle(self.iconSizeRatio)
        checkedIcon = self.getStyle(self.checkedIcon)
        uncheckedIcon = self.getStyle(self.uncheckedIcon)
        iconSize = DqtCanvas.scaleIconSize(QPixmap(checkedIcon if checked else uncheckedIcon), size, iconRatio)
        return DqtStyle(
            color=self.getStyle(DqtStyle.atColor),
            fontFamily=self.getStyle(DqtStyle.atFontFamily),
            fontSize=self.getStyle(DqtStyle.atFontSize),
            selector=DqtStyle.QCheckBox
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(iconSize.width())),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(iconSize.height())),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(0), DqtStyle.valBorderSolid, RColor.hexBlack
                )),
            ).data,
            apply=DqtStyle.QCheckBoxIndicator
        ).appendStyle(
            apply=DqtStyle.QCheckBoxIndicatorHover,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.hoverColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QCheckBoxIndicatorPressed,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.pressedColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QCheckBoxIndicatorChecked,
            styles=DictData(
                Key(DqtStyle.atImage).Val(DqtStyle.Url(checkedIcon))
            ).data
        ).appendStyle(
            apply=DqtStyle.QCheckBoxIndicatorUnchecked,
            styles=DictData(
                Key(DqtStyle.atImage).Val(DqtStyle.Url(uncheckedIcon))
            ).data
        ).style

    DefaultIconSizeRatio = QSizeF(0.80, 0.80)
    DefaultHoverColor = RColor().setQStyleAlpha(RColor.hexTealGreen, 0.1)
    DefaultPressedColor = RColor().setQStyleAlpha(RColor.hexSlateGreen, 0.3)
    DefaultCheckedIcon = RIcon().loadIconPath(RIcon.Src.select_check_box)
    DefaultUncheckedIcon = RIcon().loadIconPath(RIcon.Src.check_box_outline_blank_light)


class IconCheckBox(CheckBox):
    def __init__(
            self,
            size: QSize = None,
            fixedHeight: int = None,
            description: RState[str] = None,
            checked: RState[bool] = False,
            parent: QWidget = None,
            onValueChange: Callable = None,
            onClick: Callable = None,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: CheckBoxStyle = None,
    ):
        super().__init__(
            size=size,
            fixedHeight=fixedHeight,
            description=description,
            checked=checked,
            parent=parent,
            onValueChange=onValueChange,
            onClick=onClick,
            triggers=triggers
        )
        self._styleEditor = Validate(styleEditor, CheckBoxStyle())
        for v in self._styleEditor.styles.values():
            if isinstance(v, Remember):
                v.connect(lambda: self.updateStyle(), host=self)

    @private
    def updateStyle(self):
        self.setStyleSheet(self._styleEditor.getStyleSheet(self.size(), self.isChecked()))
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.updateStyle()
        return None
