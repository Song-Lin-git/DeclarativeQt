from typing import List, Iterable

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, ReferState, RState
from DeclarativeQt.DqtUI.DqtMaven.Layouts.LazyLayout import ScrollAreaStyle, LazyRow, LazyColumn
from DeclarativeQt.DqtUI.DqtWidgets.Container import Box, Row, Column


class AdaptiveColumn(Box):
    def __init__(
            self,
            size: QSize = None,
            parent: QWidget = None,
            options: Iterable = None,
            alignment: int = Column.Align.HCenter,
            arrangement: int = Column.Align.VCenter,
            spacing: int = None,
            padding: int = None,
            horizontalPadding: int = None,
            autoUniformDistribute: bool = False,
            style: RState[str] = None,
            content: List[RState[QWidget]] = None,
            autoContentResize: bool = False,
    ):
        super().__init__(
            parent=parent,
            contentPaddingRatio=float(0),
            content=ReferState(
                *content, lambdaExp=lambda *args: Column(
                    size=size,
                    options=options,
                    alignment=alignment,
                    arrangement=arrangement,
                    spacing=spacing,
                    padding=padding,
                    horizontalPadding=horizontalPadding,
                    autoUniformDistribute=autoUniformDistribute,
                    style=style,
                    content=Remember.getListValue(list(args)),
                    autoContentResize=autoContentResize
                )
            )
        )


class AdaptiveRow(Box):
    def __init__(
            self,
            size: QSize = None,
            parent: QWidget = None,
            options: Iterable = None,
            alignment: int = Row.Align.VCenter,
            arrangement: int = Row.Align.HCenter,
            spacing: int = None,
            padding: int = None,
            verticalPadding: int = None,
            autoUniformDistribute: bool = False,
            style: RState[str] = None,
            content: List[RState[QWidget]] = None,
            autoContentResize: bool = False,
    ):
        super().__init__(
            parent=parent,
            contentPaddingRatio=float(0),
            content=ReferState(
                *content, lambdaExp=lambda *args: Row(
                    size=size,
                    options=options,
                    alignment=alignment,
                    arrangement=arrangement,
                    spacing=spacing,
                    padding=padding,
                    verticalPadding=verticalPadding,
                    autoUniformDistribute=autoUniformDistribute,
                    style=style,
                    content=Remember.getListValue(list(args)),
                    autoContentResize=autoContentResize
                )
            )
        )


class AdaptiveLazyColumn(Box):
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
            horizontalPadding: int = None,
            autoUniformDistribute: bool = False,
            style: RState[str] = None,
            scrollAreaStyle: ScrollAreaStyle = None,
            content: List[RState[QWidget]] = None,
            autoContentResize: bool = False,
            remainSpace: int = None
    ):
        super().__init__(
            parent=parent,
            contentPaddingRatio=float(0),
            content=ReferState(
                *content, lambdaExp=lambda *args: LazyColumn(
                    size=size,
                    options=options,
                    alignment=alignment,
                    arrangement=arrangement,
                    spacing=spacing,
                    padding=padding,
                    horizontalPadding=horizontalPadding,
                    autoUniformDistribute=autoUniformDistribute,
                    style=style,
                    content=Remember.getListValue(list(args)),
                    autoContentResize=autoContentResize,
                    scrollAreaStyle=scrollAreaStyle,
                    scrollAreaHeight=scrollAreaHeight,
                    remainSpace=remainSpace
                )
            )
        )


class AdaptiveLazyRow(Box):
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
            verticalPadding: int = None,
            autoUniformDistribute: bool = False,
            style: RState[str] = None,
            scrollAreaStyle: ScrollAreaStyle = None,
            content: List[RState[QWidget]] = None,
            autoContentResize: bool = False,
            remainSpace: int = None
    ):
        super().__init__(
            parent=parent,
            contentPaddingRatio=float(0),
            content=ReferState(
                *content, lambdaExp=lambda *args: LazyRow(
                    size=size,
                    options=options,
                    alignment=alignment,
                    arrangement=arrangement,
                    spacing=spacing,
                    padding=padding,
                    verticalPadding=verticalPadding,
                    autoUniformDistribute=autoUniformDistribute,
                    style=style,
                    content=Remember.getListValue(list(args)),
                    autoContentResize=autoContentResize,
                    scrollAreaStyle=scrollAreaStyle,
                    scrollAreaWidth=scrollAreaWidth,
                    remainSpace=remainSpace
                )
            )
        )
