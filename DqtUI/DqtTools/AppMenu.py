from typing import Dict, Any

from DeclarativeQt.DqtCore.DqtBase import RState, Remember
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key


class AppMenuStyle(DqtStyleEditor):
    borderStyle = "borderStyle"
    borderColor = "borderColor"
    borderWidth = "borderWidth"
    itemTopPadding = "itemTopPadding"
    itemBottomPadding = "itemBottomPadding"
    itemLeftPadding = "itemLeftPadding"
    itemRightPadding = "itemRightPadding"
    itemBorderRadius = "itemBorderRadius"
    selectedTextColor = "selectedTextColor"
    selectedBackground = "selectedBackground"
    hoverTextColor = "hoverTextColor"
    hoverBackground = "hoverBackground"
    disabledTextColor = "disabledTextColor"
    disabledBackground = "disabledBackground"
    speratorHeight = "speratorHeight"
    speratorColor = "speratorColor"
    speratorHorizontalMargin = "speratorHorizontalMargin"
    speratorVerticalMargin = "speratorVerticalMargin"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            textColor: RState[str] = None,
            backgroundColor: RState[str] = None,
            borderStyle: RState[str] = None,
            borderWidth: RState[int] = None,
            borderColor: RState[str] = None,
            padding: RState[int] = None,
            itemTopPadding: RState[int] = None,
            itemBottomPadding: RState[int] = None,
            itemLeftPadding: RState[int] = None,
            itemRightPadding: RState[int] = None,
            itemBorderRadius: RState[int] = None,
            selectedTextColor: RState[str] = None,
            selectedBackground: RState[str] = None,
            hoverTextColor: RState[str] = None,
            hoverBackground: RState[str] = None,
            disabledTextColor: RState[str] = None,
            disabledBackground: RState[str] = None,
            speratorVerticalMargin: RState[int] = None,
            speratorHorizontalMargin: RState[int] = None,
            speratorColor: RState[str] = None,
            speratorHeight: RState[int] = None,
    ):
        styles: Dict[str, RState[Any]] = DictData(
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, RColor.hexLightWhite)),
            Key(DqtStyle.atFontFamily).Val(Remember.toValid(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atFontSize).Val(Remember.toValid(fontSize, RFont.fzTinySize)),
            Key(DqtStyle.atColor).Val(Remember.toValid(textColor, RColor.hexBlack)),
            Key(self.borderColor).Val(Remember.toValid(borderColor, RColor.hexDeepStoneBlue)),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
            Key(DqtStyle.atPadding).Val(Remember.toValid(padding, int(4))),
            Key(self.itemTopPadding).Val(Remember.toValid(itemTopPadding, int(8))),
            Key(self.itemBottomPadding).Val(Remember.toValid(itemBottomPadding, int(8))),
            Key(self.itemLeftPadding).Val(Remember.toValid(itemLeftPadding, int(14))),
            Key(self.itemRightPadding).Val(Remember.toValid(itemRightPadding, int(16))),
            Key(self.itemBorderRadius).Val(Remember.toValid(itemBorderRadius, int(2))),
            Key(self.selectedTextColor).Val(Remember.toValid(selectedTextColor, RColor.hexBlack)),
            Key(self.selectedBackground).Val(Remember.toValid(selectedBackground, RColor.hexIceBlue)),
            Key(self.hoverTextColor).Val(Remember.toValid(hoverTextColor, RColor.hexBlack)),
            Key(self.hoverBackground).Val(Remember.toValid(hoverBackground, RColor.hexIceBlue)),
            Key(self.disabledTextColor).Val(Remember.toValid(disabledTextColor, RColor.hexDarkGrey)),
            Key(self.disabledBackground).Val(Remember.toValid(disabledBackground, RColor.qtTransparent)),
            Key(self.speratorHeight).Val(Remember.toValid(speratorHeight, int(1))),
            Key(self.speratorColor).Val(Remember.toValid(speratorColor, RColor.hexLightGrey)),
            Key(self.speratorHorizontalMargin).Val(Remember.toValid(speratorHorizontalMargin, int(0))),
            Key(self.speratorVerticalMargin).Val(Remember.toValid(speratorVerticalMargin, int(4))),
        ).data
        super().__init__(styles)

    def getStyleSheet(self):
        return DqtStyle(
            selector=DqtStyle.QMenu,
            appendix=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)), self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(int(0))),
                Key(DqtStyle.atPadding).Val(DqtStyle.Px(self.getStyle(DqtStyle.atPadding))),
                Key(DqtStyle.atBackgroundClip).Val(DqtStyle.valPaddingBox),
                Key(DqtStyle.atMargin).Val(DqtStyle.Px(0))
            ).data
        ).appendStyle(
            apply=DqtStyle.QMenuItem,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(DqtStyle.atColor)),
                Key(DqtStyle.atFontFamily).Val(self.getStyle(DqtStyle.atFontFamily)),
                Key(DqtStyle.atFontSize).Val(DqtStyle.Pt(self.getStyle(DqtStyle.atFontSize))),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.itemBorderRadius))),
                Key(DqtStyle.atPadding).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.itemTopPadding)),
                    DqtStyle.Px(self.getStyle(self.itemRightPadding)),
                    DqtStyle.Px(self.getStyle(self.itemBottomPadding)),
                    DqtStyle.Px(self.getStyle(self.itemLeftPadding)),
                )),
            ).data
        ).appendStyle(
            apply=DqtStyle.QMenuItemSelected,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(self.selectedTextColor)),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.selectedBackground))
            ).data
        ).appendStyle(
            apply=DqtStyle.QMenuItemHover,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(self.hoverTextColor)),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.hoverBackground))
            ).data
        ).appendStyle(
            apply=DqtStyle.QMenuItemDisabled,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(self.disabledTextColor)),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.disabledBackground))
            ).data
        ).appendStyle(
            apply=DqtStyle.QMenuSeparator,
            styles=DictData(
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(self.getStyle(self.speratorHeight))),
                Key(DqtStyle.atMargin).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.speratorVerticalMargin)),
                    DqtStyle.Px(self.getStyle(self.speratorHorizontalMargin))
                )),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.speratorColor)),
            ).data
        ).style
