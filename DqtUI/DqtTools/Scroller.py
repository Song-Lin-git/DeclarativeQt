from typing import Dict, Any

from DeclarativeQt.DqtCore.DqtBase import RState, Remember
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key

ScrollRate = float


class ScrollerStyle(DqtStyleEditor):
    scrollBarBackground = "scrollBarBackground"
    scrollBarBorderColor = "scrollBarBorderColor"
    scrollBarBorderWidth = "scrollBarBorderWidth"
    scrollBarBorderStyle = "scrollBarBorderStyle"
    scrollBarBorderRadius = "scrollBarBorderRadius"
    scrollBarHorizontalHeight = "scrollBarHorizontalHeight"
    scrollBarVerticalWidth = "scrollBarVerticalWidth"
    scrollHandleBackground = "scrollHandleBackground"
    scrollHandleBorderRadius = "scrollHandleBorderRadius"
    scrollHandleHorizontalMinWidth = "scrollHandleHorizontalMinWidth"
    scrollHandleVerticalMinHeight = "scrollHandleVerticalMinHeight"
    scrollHandleHoverBackground = "scrollHandleHoverBackground"
    scrollHandlePressedBackground = "scrollHandlePressedBackground"

    def __init__(
            self,
            scrollBarBackground: RState[str] = None,
            scrollBarBorderColor: RState[str] = None,
            scrollBarBorderWidth: RState[int] = None,
            scrollBarBorderStyle: RState[str] = None,
            scrollBarBorderRadius: RState[int] = None,
            scrollBarHorizontalHeight: RState[int] = None,
            scrollBarVerticalWidth: RState[int] = None,
            scrollHandleBackground: RState[str] = None,
            scrollHandleBorderRadius: RState[str] = None,
            scrollHandleHorizontalMinWidth: RState[int] = None,
            scrollHandleVerticalMinHeight: RState[int] = None,
            scrollHandleHoverBackground: RState[str] = None,
            scrollHandlePressedBackground: RState[str] = None
    ):
        scrollHandleHoverBackground = Remember.toValid(scrollHandleHoverBackground, RColor.hexCloudTouch)
        scrollHandlePressedBackground = Remember.toValid(scrollHandlePressedBackground, RColor.hexUrbanShadow)
        self._styles: Dict[str, RState[Any]] = DictData(
            Key(self.scrollBarBackground).Val(Remember.toValid(scrollBarBackground, RColor.qtTransparent)),
            Key(self.scrollBarBorderColor).Val(Remember.toValid(scrollBarBorderColor, RColor.hexGrey)),
            Key(self.scrollBarBorderStyle).Val(Remember.toValid(scrollBarBorderStyle, DqtStyle.valBorderSolid)),
            Key(self.scrollBarBorderWidth).Val(Remember.toValid(scrollBarBorderWidth, int(0))),
            Key(self.scrollBarBorderRadius).Val(Remember.toValid(scrollBarBorderRadius, int(0))),
            Key(self.scrollBarHorizontalHeight).Val(Remember.toValid(scrollBarHorizontalHeight, int(4))),
            Key(self.scrollBarVerticalWidth).Val(Remember.toValid(scrollBarVerticalWidth, int(4))),
            Key(self.scrollHandleBackground).Val(Remember.toValid(scrollHandleBackground, RColor.hexSoftStone)),
            Key(self.scrollHandleBorderRadius).Val(Remember.toValid(scrollHandleBorderRadius, int(2))),
            Key(self.scrollHandleHorizontalMinWidth).Val(Remember.toValid(scrollHandleHorizontalMinWidth, int(5))),
            Key(self.scrollHandleVerticalMinHeight).Val(Remember.toValid(scrollHandleVerticalMinHeight, int(5))),
            Key(self.scrollHandleHoverBackground).Val(scrollHandleHoverBackground),
            Key(self.scrollHandlePressedBackground).Val(scrollHandlePressedBackground)
        ).data
        super(ScrollerStyle, self).__init__(self._styles)

    def getStyleSheet(self):
        return DqtStyle(
            appendix=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.scrollBarBackground)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.scrollBarBorderRadius))),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.scrollBarBorderWidth)),
                    self.getStyle(self.scrollBarBorderStyle), self.getStyle(self.scrollBarBorderColor)
                )),
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(self.getStyle(self.scrollBarVerticalWidth)))
            ).data,
            selector=DqtStyle.QScrollBarVertical
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.scrollBarBackground)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.scrollBarBorderRadius))),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(self.getStyle(self.scrollBarHorizontalHeight)))
            ).data,
            apply=DqtStyle.QScrollBarHorizontal
        ).appendStyle(
            apply=DqtStyle.QScrollBarHandleVertical,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.scrollHandleBackground)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.scrollHandleBorderRadius))),
                Key(DqtStyle.atMinHeight).Val(DqtStyle.Px(self.getStyle(self.scrollHandleVerticalMinHeight)))
            ).data
        ).appendStyle(
            apply=DqtStyle.QScrollBarHandleHorizontal,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.scrollHandleBackground)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.scrollHandleBorderRadius))),
                Key(DqtStyle.atMinWidth).Val(DqtStyle.Px(self.getStyle(self.scrollHandleHorizontalMinWidth)))
            ).data
        ).appendStyle(
            apply=DqtStyle.QScrollBarHandleHover,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.scrollHandleHoverBackground))
            ).data
        ).appendStyle(
            apply=DqtStyle.QScrollBarHandlePressed,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.scrollHandlePressedBackground))
            ).data
        ).appendStyle(
            apply=DqtStyle.QScrollAddSubLine,
            styles=DictData(
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(0)),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(0))
            ).data
        ).appendStyle(
            apply=DqtStyle.QScrollAddSubPage,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(DqtStyle.valNone)
            ).data
        ).style
