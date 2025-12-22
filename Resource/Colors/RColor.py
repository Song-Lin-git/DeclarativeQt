import random
from typing import Union, Callable, List

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog

from DeclarativeQt.Resource.Grammars.RGrammar import StrFrame, GIters, CheckType, isEmpty, GList, Equal, ConditionList
from DeclarativeQt.Resource.Strings.RStr import RStr, Phrase

HexColor = str
HexPrefix = str
QtStyleColor = str
ColorMode = str
ColorValue = int
AlphaValue = float


class RColor:
    RGB: ColorMode = "RGB"
    RGBA: ColorMode = "RGBA"
    RgbMax: ColorValue = 255
    RgbMin: ColorValue = 0
    RgbLimit: Callable = staticmethod(lambda x: min(255, max(x, 0)))
    AlphaMax: AlphaValue = 1.0
    AlphaMin: AlphaValue = 0.0
    qtRgbFrame: StrFrame = staticmethod(lambda r, g, b: f"rgb({r}, {g}, {b})")
    qtRgbaFrame: StrFrame = staticmethod(lambda r, g, b, alpha: f"rgba({r}, {g}, {b}, {alpha})")
    RgbHexUnit: Phrase = "{:02X}"
    HexDigits: str = "0123456789abcdefABCDEF"
    ValidHexCodeNibbles = GList(6, 8)
    ValidHexPrefix: List[HexPrefix] = GList(RStr.pSharp, RStr.frHexPrefix0x)
    DefaultHexCodePrefix: HexPrefix = RStr.pSharp

    @staticmethod
    def qStyleColor(r: ColorValue, g: ColorValue, b: ColorValue, alpha: AlphaValue = AlphaMax):
        r, g, b = RColor.RgbLimit(r), RColor.RgbLimit(g), RColor.RgbLimit(b)
        alpha = max(min(alpha, RColor.AlphaMax), RColor.AlphaMin)
        return RColor.qtRgbaFrame(r, g, b, alpha)

    @staticmethod
    def qColorToHexCode(qColor: QColor):
        return RColor.RGBtoHexCode(r=qColor.red(), g=qColor.green(), b=qColor.blue())

    @staticmethod
    def hexCodeToRGB(color: HexColor):
        color = color[len(color) - 6:]
        r, g, b = color[:2], color[2:4], color[4:6]
        r, g, b = int(r, 16), int(g, 16), int(b, 16)
        return QColor(r, g, b)

    @staticmethod
    def isHexColor(color: object, nibs: int = None):
        if not CheckType(color, str):
            return False
        if isEmpty(color):
            return False
        nibs = nibs if nibs in RColor.ValidHexCodeNibbles else None
        for val in RColor.ValidHexPrefix:
            if not Equal(val, color[:len(val)]):
                continue
            code = color[len(val):]
            if nibs is not None and len(code) != nibs:
                continue
            elif len(code) not in RColor.ValidHexCodeNibbles:
                continue
            if len(ConditionList(code, lambda a0: a0 not in RColor.HexDigits)) > 0:
                continue
            return True
        return False

    @staticmethod
    def hexCodeToQColor(color: HexColor, alpha: AlphaValue = AlphaMax):
        qcolor = RColor.hexCodeToRGB(color)
        qcolor.setAlphaF(alpha)
        return qcolor

    @staticmethod
    def RGBtoHexCode(r: ColorValue, g: ColorValue, b: ColorValue, prefix: HexPrefix = None):
        if prefix is None:
            prefix = RColor.DefaultHexCodePrefix
        hexCode = RStr.pEmpty
        for value in GIters(r, g, b):
            fix_value = RColor.RgbLimit(value)
            hexCode += RColor.RgbHexUnit.format(fix_value)
        return prefix + hexCode

    @staticmethod
    def setQStyleAlpha(color: Union[QColor, HexColor], alpha: AlphaValue = AlphaMax):
        if isinstance(color, HexColor):
            color = RColor.hexCodeToRGB(color)
        assert isinstance(color, QColor)
        return RColor.qStyleColor(color.red(), color.green(), color.blue(), alpha)

    @staticmethod
    def setQColorAlpha(color: QColor, alpha: AlphaValue):
        color.setAlphaF(alpha)
        return color

    @staticmethod
    def colorBlack(prefix: HexPrefix = None) -> HexColor:
        return RColor.RGBtoHexCode(0, 0, 0, prefix)

    @staticmethod
    def randomColor(prefix: HexPrefix = None) -> HexColor:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return RColor.RGBtoHexCode(r, g, b, prefix)

    @staticmethod
    def getQtColorInput(initial: Union[QColor, HexColor]) -> QColor:
        initial = QColor(initial)
        color = QColorDialog.getColor(initial)
        return color if color.isValid() else initial

    qtTransparent: QtStyleColor = "transparent"
    hexBlack: HexColor = "#000000"
    hexWhite: HexColor = "#FFFFFF"
    hexGrey: HexColor = "#AAAAAA"
    hexLightGrey: HexColor = "#DDDDDD"
    hexDarkGrey: HexColor = "#888888"
    hexDeepGrey: HexColor = "#3A3A3A"
    hexRed: HexColor = "#FF0000"
    hexBlue: HexColor = "#0000FF"
    hexCyanBlue: HexColor = "#119CA7"
    hexSkyBlue: HexColor = "#87CEFA"
    hexSlateGreen: HexColor = "#628470"
    hexLimeGreen: HexColor = "#E6FFb7"
    hexForestGreen: HexColor = "#50884F"
    hexDarkRed: HexColor = "#660000"
    hexTealGreen: HexColor = "#0A5F55"
    hexLightWhite: HexColor = "#FAFAFA"
    hexPureMist: HexColor = "#F2F2F2"
    hexSoftStone: HexColor = "#D8D8D8"
    hexCloudTouch: HexColor = "#C1C1C1"
    hexUrbanShadow: HexColor = "#A8A8A8"
    hexMidnightNavy: HexColor = "#255290"
    hexDarkSlateBlue: HexColor = "#2F4F4F"
    hexMediumMidnightBlue: HexColor = "#1A2B44"
    hexSteelBlue: HexColor = "#4682B4"
    hexLightSteelBlue: HexColor = "#B0C4DE"
    hexRoyalBlue: HexColor = "#4169E1"
    hexNightSkyBlue: HexColor = "#274483"
    hexDodgerBlue: HexColor = "#1E90FF"
    hexIceBlue: HexColor = "#E4F0FF"
    hexMistBlue: HexColor = "#A3B8C1"
    hexTealGrey: HexColor = "#7B9A9D"
    hexDeepStoneBlue: HexColor = "#5A7579"
    hexSoftRose: HexColor = "#E6A9B7"
    hexRustRed: HexColor = "#B7410E"
    hexDeepCrimson: HexColor = "#8A0F0F"
    hexSalmonPink: HexColor = "#FF9679"
    hexAutumnMaple: HexColor = "#DA954B"
    hexPolarHaze: HexColor = "#F8FAFA"
    hexPaleSilver: HexColor = "#EFEFEF"
    hexMistyHarborBlue: HexColor = "#7AA6CB"
    hexMidnightHarbor: HexColor = "#38688F"
