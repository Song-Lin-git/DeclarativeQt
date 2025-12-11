from functools import partial
from typing import Iterable, Union, List, Self

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QScrollArea

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout
from DeclarativeQt.DqtUI.DqtTools.Scroller import ScrollerStyle, ScrollRate
from DeclarativeQt.DqtUI.DqtWidgets.Container import Column, Row
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import Equal, Validate, Key, DictData, isValid
from DeclarativeQt.Resource.Images.RImage import LutPixel


class ScrollAreaStyle(DqtStyleEditor):
    borderWidth = "borderWidth"
    borderColor = "borderColor"
    borderStyle = "borderStyle"

    def __init__(
            self,
            backgroundColor: RState[str] = None,
            borderWidth: RState[int] = None,
            borderRadius: RState[int] = None,
            borderColor: RState[str] = None,
            borderStyle: RState[str] = None,
            scrollerStyle: ScrollerStyle = None
    ):
        self._styles = DictData(
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, RColor.hexLightWhite)),
            Key(DqtStyle.atBorderRadius).Val(Remember.toValid(borderRadius, int(3))),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.borderColor).Val(Remember.toValid(borderColor, RColor.hexGrey)),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
        ).data
        self._scrollerStyle = Validate(scrollerStyle, ScrollerStyle())
        super(ScrollAreaStyle, self).__init__(self._styles)

    def getStyleSheet(self) -> str:
        return DqtStyle(
            appendix=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius)))
            ).data,
            selector=DqtStyle.QScrollArea
        ).mergeStyle(
            styleSheet=self._scrollerStyle.getStyleSheet()
        ).style


class LazyRow(QScrollArea):
    DefaultRemainSpace: LutPixel = int(20)
    DefaultScrollRate: ScrollRate = float(0.46)

    def __init__(
            self,
            size: QSize = None,
            scrollAreaWidth: int = None,
            parent: QWidget = None,
            options: Iterable = None,
            alignment: int = Row.Align.VCenter,
            arrangement: int = Row.Align.HCenter,
            spacing: int = None,
            padding: int = None,
            fixWidth: bool = False,
            fixHeight: bool = False,
            verticalPadding: int = None,
            wheelRate: float = None,
            autoUniformDistribute: bool = False,
            style: RState[str] = None,
            scrollAreaStyle: ScrollAreaStyle = None,
            content: List[QWidget] = None,
            autoContentResize: bool = False,
            remainSpace: int = None
    ):
        super().__init__(parent)
        row = Row(
            size=size,
            options=options,
            alignment=alignment,
            arrangement=arrangement,
            spacing=spacing,
            padding=padding,
            verticalPadding=verticalPadding,
            autoUniformDistribute=autoUniformDistribute,
            style=style,
            content=content,
            autoContentResize=autoContentResize
        )
        self._remainSpace = Validate(remainSpace, self.DefaultRemainSpace)
        self._wheelRate = Validate(self.DefaultScrollRate, wheelRate)
        self._scrollAreaWidth = scrollAreaWidth
        self._scrollAreaStyle = Validate(scrollAreaStyle, ScrollAreaStyle())
        self._fixWidth = fixWidth
        self._fixHeight = fixHeight
        for v in self._scrollAreaStyle.styles.values():
            if isinstance(v, Remember):
                v.connect(partial(self.updateStyle), host=self)
        self.updateStyle()
        self._initialSize = None
        self.fromRow(row)

    def fromRow(self, row: Union[Row, LinearLayout]) -> Self:
        assert Equal(row.direction, LinearLayout.Horizontal)
        self.setWidget(row)
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setFixedSize(Validate(self._scrollAreaWidth, row.width()), row.height() + self._remainSpace)
        self._initialSize = self.size()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return self

    def updateStyle(self):
        super().setStyleSheet(self._scrollAreaStyle.getStyleSheet())
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if isValid(self._initialSize):
            if self._fixWidth:
                self.setFixedWidth(self._initialSize.width())
            if self._fixHeight:
                self.setFixedHeight(self._initialSize.height())
        return None

    def wheelEvent(self, a0):
        if Equal(a0.modifiers(), Qt.ControlModifier):
            super().wheelEvent(a0)
            return None
        scroll_value = self.horizontalScrollBar().value()
        delta = int(a0.angleDelta().y() * self._wheelRate)
        self.horizontalScrollBar().setValue(scroll_value - delta)
        a0.accept()
        return None


class LazyColumn(QScrollArea):
    DefaultRemainSpace: LutPixel = int(20)
    DefaultScrollRate: ScrollRate = float(0.68)

    def __init__(
            self,
            size: QSize = None,
            scrollAreaHeight: int = None,
            parent: QWidget = None,
            options: Iterable = None,
            alignment: int = Column.Align.HCenter,
            arrangement: int = Column.Align.VCenter,
            spacing: int = None,
            padding: int = None,
            fixWidth: bool = False,
            fixHeight: bool = False,
            wheelRate: float = None,
            horizontalPadding: int = None,
            autoUniformDistribute: bool = False,
            style: RState[str] = None,
            scrollAreaStyle: ScrollAreaStyle = None,
            content: List[QWidget] = None,
            autoContentResize: bool = False,
            remainSpace: int = None
    ):
        super().__init__(parent)
        column = Column(
            size=size,
            options=options,
            alignment=alignment,
            arrangement=arrangement,
            spacing=spacing,
            padding=padding,
            horizontalPadding=horizontalPadding,
            autoUniformDistribute=autoUniformDistribute,
            style=style,
            content=content,
            autoContentResize=autoContentResize
        )
        self._wheelRate = Validate(self.DefaultScrollRate, wheelRate)
        self._remainSpace = Validate(remainSpace, self.DefaultRemainSpace)
        self._scrollAreaHeight = scrollAreaHeight
        self._scrollAreaStyle = Validate(scrollAreaStyle, ScrollAreaStyle())
        self._fixWidth = fixWidth
        self._fixHeight = fixHeight
        for v in self._scrollAreaStyle.styles.values():
            if isinstance(v, Remember):
                v.connect(partial(self.updateStyle), host=self)
        self.updateStyle()
        self._initialSize = None
        self.fromColumn(column)

    def fromColumn(self, column: Union[Column, LinearLayout]) -> Self:
        assert Equal(column.direction, LinearLayout.Vertical)
        self.setWidget(column)
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setFixedSize(column.width() + self._remainSpace, Validate(self._scrollAreaHeight, column.height()))
        self._initialSize = self.size()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        return self

    def updateStyle(self):
        super().setStyleSheet(self._scrollAreaStyle.getStyleSheet())
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if isValid(self._initialSize):
            if self._fixWidth:
                self.setFixedWidth(self._initialSize.width())
            if self._fixHeight:
                self.setFixedHeight(self._initialSize.height())
        return None

    def wheelEvent(self, a0):
        if Equal(a0.modifiers(), Qt.ControlModifier):
            super().wheelEvent(a0)
            return None
        scroll_value = self.verticalScrollBar().value()
        delta = int(a0.angleDelta().y() * self._wheelRate)
        self.verticalScrollBar().setValue(scroll_value - delta)
        a0.accept()
        return None
