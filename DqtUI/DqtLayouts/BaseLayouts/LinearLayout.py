from typing import List, Iterable

from PyQt5.QtCore import QSize, QSizeF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QSizePolicy, QStyleOption, QStyle

from DeclarativeQt.DqtCore.DqtBase import Remember, OptionKey, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtAlign import DqtAlign
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import DataBox, ReferList, Equal, Validate, PureList, isValid, GTuple
from DeclarativeQt.Resource.Images.RImage import LutPixel
from DeclarativeQt.Resource.Strings.RString import RString


class LinearLayout(QWidget):
    Align = DqtAlign
    Horizontal: OptionKey = "Hrizontal"
    Vertical: OptionKey = "Vertical"

    def __init__(
            self,
            size: QSize = None,
            direction: str = None,
            options: Iterable = None,
            alignment: int = None,
            arrangement: int = None,
            spacing: int = None,
            linePadding: int = None,
            crossPadding: int = None,
            fixWidth: bool = False,
            fixHeight: bool = False,
            style: RState[str] = None,
            content: List[QWidget] = None,
            autoContentResize: bool = False,
            autoExpandContentAt: int = None,
            autoExpandToMaxCross: List[int] = None,
            autoUniformDistribute: bool = False,
    ):
        super().__init__()
        self._spacing = Validate(spacing, self.DefaultSpacing)
        self._linePadding = Validate(linePadding, self.DefaultPadding)
        self._crossPadding = Validate(crossPadding, self.DefaultPadding)
        self._options = set(Validate(options, list()))
        if self.NoPadding in self._options:
            self._linePadding, self._crossPadding = GTuple(0, 0)
            self._options.add(self.AutoSizeNoRemain)
        self._autoUniformDistribute = autoUniformDistribute
        self._direction = Validate(direction, self.Vertical)
        self._isHorizontal = Equal(self._direction, self.Horizontal)
        self._alignment = Validate(alignment, self.Align.HCenter)
        self._arrangement = Validate(arrangement, self.Align.VCenter)
        self._content = PureList(Validate(content, list()))
        self._fixWidth = fixWidth
        self._fixHeight = fixHeight
        self._initialSize = None
        for ct in self._content:
            ct.setParent(self)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.initCanvasSize(size)
        refuseParentStyle = bool(self.RefuseParentStyle in self._options)
        self._style = Validate(style, DqtStyle.emptyStyle(DqtStyle.QWidget) if refuseParentStyle else RString.pEmpty)
        self.setStyleSheet(self._style)
        if isinstance(self._style, Remember):
            self._style.connect(lambda value: self.setStyleSheet(value), host=self)
        self._contentSizeRatio = None
        self._autoContentResize = autoContentResize
        self._autoExpandContentAt = autoExpandContentAt
        self._autoExpandToMaxCross = Validate(autoExpandToMaxCross, list())
        self._initContents = False

    @property
    def contents(self):
        return self._content

    @property
    def direction(self) -> OptionKey:
        return self._direction

    def contentWidths(self) -> List[int]:
        return ReferList(self._content, lambda ct: ct.width())

    def contentHeights(self) -> List[int]:
        return ReferList(self._content, lambda ct: ct.height())

    @private
    def initCanvasSize(self, size: QSize = None):
        if size:
            self.setFixedSize(size)
        elif len(self._content) > 0:
            line_blank = self._linePadding * 2 + self._spacing * int(len(self._content) - 1)
            cross_blank = self._crossPadding * 2
            content_widths: list = self.contentWidths()
            content_heights: list = self.contentHeights()
            no_remain = bool(self.AutoSizeNoRemain in self._options)
            remain_ratio = DqtCanvasBase.NoRemainRatio if no_remain else DqtCanvasBase.LayoutRemainRatio
            width = int((max(content_widths) + cross_blank) * remain_ratio)
            height = int((sum(content_heights) + line_blank) * remain_ratio)
            if self._isHorizontal:
                width = int((sum(content_widths) + line_blank) * remain_ratio)
                height = int((max(content_heights) + cross_blank) * remain_ratio)
            self.setFixedSize(width, height)
        else:
            self.setFixedSize(self.DefaultSize)
        self._initialSize = self.size()
        return None

    def paintEvent(self, a0):
        super().paintEvent(a0)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        if not self._initContents:
            self.rebuildCanvas()
            self._initContents = True
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def setStyleSheet(self, styleSheet):
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        if isValid(self._initialSize):
            if self._fixHeight:
                self.setFixedHeight(self._initialSize.height())
            if self._fixWidth:
                self.setFixedWidth(self._initialSize.width())
        self.rebuildCanvas()
        return None

    @private
    def rebuildCanvas(self):
        self.setFixedSize(self.size())
        if self._autoContentResize:
            self.resizeContent()
        self.placeContent()
        return None

    @private
    def resizeContent(self):
        if self._contentSizeRatio is None:
            ratioSize = lambda ct: QSizeF(ct.width() / self.width(), ct.height() / self.height())
            self._contentSizeRatio: list = ReferList(self._content, ratioSize)
            return None
        itemCount = len(self._content)
        itemTotalWidth, itemTotalHeight = int(0), int(0)
        expandItem, expandSize = None, None
        for i, item in enumerate(self._content):
            itemSizeRatio: QSizeF = self._contentSizeRatio[i]
            item_width = int(self.width() * itemSizeRatio.width())
            item_height = int(self.height() * itemSizeRatio.height())
            item_size = QSize(item_width, item_height)
            if i in self._autoExpandToMaxCross:
                cross_blank = int(2) * self._crossPadding
                if self._isHorizontal:
                    item_size.setHeight(int(self.height() - cross_blank))
                else:
                    item_size.setWidth(int(self.width() - cross_blank))
            if Equal(i, self._autoExpandContentAt):
                expandItem, expandSize = item, item_size
                continue
            item.setFixedSize(item_size)
            itemTotalHeight += item.height()
            itemTotalWidth += item.width()
        if isValid(expandItem):
            blank_space = int(self._spacing * int(itemCount - 1) + self._linePadding * int(2))
            if self._isHorizontal:
                remain_width = self.width() - itemTotalWidth - blank_space
                expandSize.setWidth(remain_width)
            else:
                remain_height = self.height() - itemTotalHeight - blank_space
                expandSize.setHeight(remain_height)
            expandItem.setFixedSize(expandSize)
        return None

    @private
    def placeContent(self):
        return DataBox(DqtCanvas.linearContentLayout(
            canvas=self, contents=self._content, uniformDistribute=self._autoUniformDistribute,
            isHorizontal=self._isHorizontal, alignment=self._alignment, arrangement=self._arrangement,
            linePadding=self._linePadding, crossPadding=self._crossPadding, spacing=self._spacing,
        )).data

    AutoSizeNoRemain: OptionKey = "AutoSizeNoRemain"
    RefuseParentStyle: OptionKey = "RefuseParentStyle"
    NoPadding: OptionKey = "NoPadding"
    DefaultSpacing: LutPixel = int(1)
    DefaultPadding: LutPixel = int(1)
    DefaultSize: QSize = QSize(40, 40)
