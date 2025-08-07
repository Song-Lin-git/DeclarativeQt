from functools import partial
from typing import Dict, Any, Callable

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import RState, Remember, ReferState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.Sliders.BaseSlider.Slider import Slider
from DeclarativeQt.Resource.Colors.RColor import RColor, HexColor
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate, Equal, GStr, isValid, GList
from DeclarativeQt.Resource.Grammars.RGrmBase.RGrmObject import DataBox
from DeclarativeQt.Resource.Images.RImage import LutPixel


class SliderStyle(DqtStyleEditor):
    borderWidth = "borderWidth"
    borderColor = "borderColor"
    borderStyle = "borderStyle"
    grooveLengthRatio = "grooveLengthRatio"
    grooveThickness = "grooveThickness"
    grooveBackground = "grooveBackground"
    grooveBorderWidth = "grooveBorderWidth"
    grooveBorderColor = "grooveBorderColor"
    grooveBorderRadius = "grooveBorderRadius"
    subPageBackground = "subPageBackground"
    addPageBackground = "addPageBackground"
    handleBorderRadius = "handleBorderRadius"
    handleWidthRatio = "handleWidthRatio"
    handleHeightRatio = "handleHeightRatio"
    handleBorderWidth = "handleBorderWidth"
    handleBorderColor = "handleBorderColor"
    handleBackground = "handleBackground"
    handleHoverBorderWidth = "handleHoverBorderWidth"
    handleHoverBorderColor = "handleHoverBorderColor"
    handleHoverBackground = "handleHoverBackground"
    handlePressedBorderWidth = "handlePressedBorderWidth"
    handlePressedBorderColor = "handlePressedBorderColor"
    handlePressedBackground = "handlePressedBackground"

    def __init__(
            self,
            backgroundColor: RState[str] = None,
            borderWidth: RState[int] = None,
            borderColor: RState[str] = None,
            borderRadius: RState[int] = None,
            borderStyle: RState[str] = None,
            grooveLengthRatio: RState[float] = None,
            grooveThickness: RState[int] = None,
            grooveBackground: RState[str] = None,
            grooveBorderWidth: RState[int] = None,
            grooveBorderColor: RState[str] = None,
            grooveBorderRadius: RState[int] = None,
            subPageBackground: RState[str] = None,
            addPageBackground: RState[str] = None,
            themeHexColor: RState[HexColor] = None,
            handleBorderRadius: RState[int] = None,
            handleWidthRatio: RState[float] = None,
            handleHeightRatio: RState[float] = None,
            handleBorderWidth: RState[int] = None,
            handleBorderColor: RState[str] = None,
            handleBackground: RState[str] = None,
            handleHoverBorderWidth: RState[int] = None,
            handleHoverBorderColor: RState[str] = None,
            handleHoverBackground: RState[str] = None,
            handlePressedBorderWidth: RState[int] = None,
            handlePressedBorderColor: RState[str] = None,
            handlePressedBackground: RState[str] = None,
    ):
        themeColor = Validate(themeHexColor, RColor.hexMistyHarborBlue)
        hoverDarkerFactor = int(self.HoverColorDarkerRatio * self.ColorDarkerFactor)
        pressedDarkerFactor = int(self.PressedColorDarkerRatio * self.ColorDarkerFactor)
        darkerColorState = lambda factor: DataBox(ReferState(
            themeColor, lambdaExp=lambda a0:
            RColor.qColorToHexCode(RColor.hexCodeToQColor(a0).darker(factor))
        )).data
        hoverColor = darkerColorState(hoverDarkerFactor)
        pressedColor = darkerColorState(pressedDarkerFactor)
        self._styles: Dict[str, RState[Any]] = DictData(
            Key(DqtStyle.atBackgroundColor).Val(Validate(backgroundColor, RColor.hexLightWhite)),
            Key(DqtStyle.atBorderRadius).Val(Validate(borderRadius, int(3))),
            Key(self.borderColor).Val(Validate(borderColor, RColor.hexSoftStone)),
            Key(self.borderWidth).Val(Validate(borderWidth, int(1))),
            Key(self.borderStyle).Val(Validate(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.grooveLengthRatio).Val(Validate(grooveLengthRatio, 0.94)),
            Key(self.grooveThickness).Val(Validate(grooveThickness, int(4))),
            Key(self.grooveBackground).Val(Validate(grooveBackground, RColor.hexGrey)),
            Key(self.grooveBorderWidth).Val(Validate(grooveBorderWidth, int(0))),
            Key(self.grooveBorderColor).Val(Validate(grooveBorderColor, RColor.hexDarkGrey)),
            Key(self.grooveBorderRadius).Val(Validate(grooveBorderRadius, int(2))),
            Key(self.subPageBackground).Val(Validate(subPageBackground, themeColor)),
            Key(self.addPageBackground).Val(Validate(addPageBackground, RColor.hexUrbanShadow)),
            Key(self.handleBorderRadius).Val(Validate(handleBorderRadius, None)),
            Key(self.handleWidthRatio).Val(Validate(handleWidthRatio, 4.0)),
            Key(self.handleHeightRatio).Val(Validate(handleHeightRatio, 4.0)),
            Key(self.handleBorderWidth).Val(Validate(handleBorderWidth, int(2))),
            Key(self.handleBorderColor).Val(Validate(handleBorderColor, themeColor)),
            Key(self.handleBackground).Val(Validate(handleBackground, RColor.hexWhite)),
            Key(self.handleHoverBorderWidth).Val(Validate(handleHoverBorderWidth, int(0))),
            Key(self.handleHoverBorderColor).Val(Validate(handleHoverBorderColor, hoverColor)),
            Key(self.handleHoverBackground).Val(Validate(handleHoverBackground, hoverColor)),
            Key(self.handlePressedBorderWidth).Val(Validate(handlePressedBorderWidth, int(0))),
            Key(self.handlePressedBorderColor).Val(Validate(handlePressedBorderColor, themeColor)),
            Key(self.handlePressedBackground).Val(Validate(handlePressedBackground, pressedColor)),
        ).data
        super().__init__(self._styles)

    def getStyleSheet(self, size: QSize, direction: int) -> str:
        borderExpand = int(2.0 * self.getStyle(self.handleBorderWidth))
        if Equal(direction, Slider.Horizontal):
            grooveWidth = int(self.getStyle(self.grooveLengthRatio) * size.width())
            grooveHeight = self.getStyle(self.grooveThickness)
            handleWidth = int(grooveHeight * self.getStyle(self.handleWidthRatio))
            handleHeight = min(int(grooveHeight * self.getStyle(self.handleHeightRatio)), size.height())
            handleMargin = -int(float(handleHeight - grooveHeight) / 2.0)
            handleMarginStyle = DqtStyle.valueCat(DqtStyle.Px(handleMargin), DqtStyle.Px(0))
            handleFrameWidth = int(handleWidth)
            handleFrameHeight = int(handleHeight + borderExpand)
            fixedHandleWidth = int(handleWidth - borderExpand)
            fixedHandleHeight = int(handleHeight)
        else:
            grooveHeight = int(self.getStyle(self.grooveLengthRatio) * size.height())
            grooveWidth = self.getStyle(self.grooveThickness)
            handleWidth = min(int(grooveWidth * self.getStyle(self.handleWidthRatio)), size.width())
            handleHeight = int(grooveWidth * self.getStyle(self.handleHeightRatio))
            handleMargin = -int(float(handleWidth - grooveWidth) / 2.0)
            handleMarginStyle = DqtStyle.valueCat(DqtStyle.Px(0), DqtStyle.Px(handleMargin))
            handleFrameWidth = int(handleWidth + borderExpand)
            handleFrameHeight = int(handleHeight)
            fixedHandleWidth = int(handleWidth)
            fixedHandleHeight = int(handleHeight - borderExpand)
        shrinkHover: LutPixel = int(2.0 * self.getStyle(self.handleHoverBorderWidth))
        shrinkPressed: LutPixel = int(2.0 * self.getStyle(self.handlePressedBorderWidth))
        handleRadius = self.getStyle(self.handleBorderRadius)
        if not isValid(handleRadius):
            handleRadius = int(min(handleWidth, handleHeight) / 2.0)
        directionPseudo = DictData(
            Key(Slider.Horizontal).Val(DqtStyle.PseudoHorizontal),
            Key(Slider.Vertical).Val(DqtStyle.PseudoVertical),
        ).data
        pageSelector = GList(DqtStyle.QSliderSubPage, DqtStyle.QSliderAddPage)
        if Equal(direction, Slider.Vertical):
            pageSelector = pageSelector[::-1]
        solid = DqtStyle.valBorderSolid
        return DqtStyle(
            appendix=DictData(
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle), self.getStyle(self.borderColor),
                )),
            ).data,
            selector=DqtStyle.QSlider,
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(grooveWidth)),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(grooveHeight)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.grooveBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.grooveBackground)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.grooveBorderWidth)),
                    GStr(solid), self.getStyle(self.grooveBorderColor),
                ))
            ).data,
            apply=DqtStyle.QSliderGroove + directionPseudo[direction],
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.grooveBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.subPageBackground)),
            ).data,
            apply=pageSelector[0] + directionPseudo[direction],
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.grooveBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.addPageBackground)),
            ).data,
            apply=pageSelector[-1] + directionPseudo[direction],
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(fixedHandleWidth)),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(fixedHandleHeight)),
                Key(DqtStyle.atMargin).Val(handleMarginStyle),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(handleRadius)),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.handleBackground)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.handleBorderWidth)),
                    GStr(solid), self.getStyle(self.handleBorderColor),
                ))
            ).data,
            apply=DqtStyle.QSliderHandle + directionPseudo[direction],
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.handleHoverBackground)),
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(int(handleFrameWidth - shrinkHover))),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(int(handleFrameHeight - shrinkHover))),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(handleRadius)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.handleHoverBorderWidth)),
                    GStr(solid), self.getStyle(self.handleHoverBorderColor),
                ))
            ).data,
            apply=DqtStyle.QSliderHandle + directionPseudo[direction] + DqtStyle.PseudoHover,
        ).appendStyle(
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.handlePressedBackground)),
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(int(handleFrameWidth - shrinkPressed))),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(int(handleFrameHeight - shrinkPressed))),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(handleRadius)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.handlePressedBorderWidth)),
                    GStr(solid), self.getStyle(self.handlePressedBorderColor),
                ))
            ).data,
            apply=DqtStyle.QSliderHandle + directionPseudo[direction] + DqtStyle.PseudoPressed,
        ).style

    ColorDarkerFactor = int(100)
    HoverColorDarkerRatio: float = 1.28
    PressedColorDarkerRatio: float = 2.0


class ColoredSlider(Slider):
    Horizontal = Slider.Horizontal
    Vertical = Slider.Vertical

    def __init__(
            self,
            size: QSize = None,
            parent: QWidget = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            direction: int = Horizontal,
            data: RState[float] = None,
            percision: int = None,
            maxVal: float = None,
            minVal: float = None,
            onValueChange: Callable = None,
            styleEditor: SliderStyle = None,
            triggers: Dict[Remember, Callable] = None,
    ):
        self._styleEditor = Validate(styleEditor, SliderStyle())
        super().__init__(
            size=size,
            parent=parent,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            direction=direction,
            data=data,
            percision=percision,
            maxVal=maxVal,
            minVal=minVal,
            onValueChange=onValueChange,
            triggers=triggers,
        )
        self.updateStyle()
        for val in self._styleEditor.styles.values():
            if isinstance(val, Remember):
                val.connect(partial(self.updateStyle), host=self)

    def updateStyle(self):
        self.setStyleSheet(self._styleEditor.getStyleSheet(self.size(), self.orientation()))
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.updateStyle()
        return None
