import os.path
from typing import Tuple, Union

from PIL import Image
from PyQt5.QtCore import QSize, QSizeF
from PyQt5.QtGui import QPixmap, QColor

from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import TupleData, Grammar, Validate
from DeclarativeQt.Resource.Strings.RString import RString

LutCm = float
LutPoint = int
LutPixel = int
LutInch = float
LutExact = int
LutRatio = float
ExactSize = Tuple[LutExact, LutExact]
RatioSize = Tuple[LutRatio, LutRatio]
CanvasSize = Tuple[Union[int, float], Union[int, float]]


class RImage:
    TupleToQSize: Grammar = staticmethod(lambda size: QSize(size[0], size[1]))

    def __init__(self):
        self.PlaceholdImage = Image.new(RColor.RGB, self.exDefaultSize, color=RColor.hexWhite)

    @staticmethod
    def createQPixmp(color: str, width: int = None, height: int = None):
        width = Validate(width, RImage.exDefaultWidth)
        height = Validate(height, RImage.exDefaultHeight)
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(color))
        return pixmap

    @staticmethod
    def createImage(width: int, height: int, color: str):
        return Image.new(RColor.RGB, TupleData(width, height).data, color=color)

    @staticmethod
    def limitImageToBox(imageSize: QSizeF, limitBox: QSizeF) -> QSizeF:
        width, height = imageSize.width(), imageSize.height()
        limit_width, limit_height = limitBox.width(), limitBox.height()
        aspect = width / height
        limit_aspect = limit_width / limit_height
        target_width = limit_height * aspect
        target_height = limit_height
        if aspect > limit_aspect:
            target_width = limit_width
            target_height = limit_width / aspect
        return QSizeF(target_width, target_height)

    @staticmethod
    def absolutePathToRelativeUrl(path: str):
        url = os.path.relpath(path)
        url = url.replace(RString.pBlank, RString.pUrlBlank)
        url = url.replace(RString.pBackSlash, RString.pForwardSlash)
        return url

    exDefaultWidth: LutExact = int(300)
    exDefaultHeight: LutExact = int(200)
    exDefaultSize: ExactSize = TupleData(exDefaultWidth, exDefaultHeight).data
    exDefaultQSize: QSize = QSize(exDefaultWidth, exDefaultHeight)
    cmDefaultWidth: LutCm = 14.0
    cmDefaultHeight: LutCm = 7.0
    rtDefaultWidth: LutRatio = 0.4
    rtDefaultHeight: LutRatio = 0.3
    rtDefaultSize: QSizeF = QSizeF(rtDefaultWidth, rtDefaultHeight)
