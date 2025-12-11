from functools import partial
from typing import Callable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QTableView

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.TableViews.BaseTableView.TableView import TableView, TableData, \
    TableFields, CellArea, CellAt, TableFieldMap
from DeclarativeQt.DqtUI.DqtTools.Scroller import ScrollerStyle
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate, DataBox
from DeclarativeQt.Resource.Images.RImage import LutPixel


class HeaderViewStyle(DqtStyleEditor):
    borderColor = "borderColor"
    borderStyle = "borderStyle"
    borderWidth = "borderWidth"
    selectedBackgroundColor = "selectedBackgroundColor"
    selectedFontFamily = "selectedFontFamily"
    hoverBackgroundColor = "hoverBackgroundColor"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            textColor: RState[str] = None,
            borderColor: RState[str] = None,
            borderStyle: RState[str] = None,
            borderWidth: RState[int] = None,
            backgroundColor: RState[str] = None,
            selectedBackgroundColor: RState[str] = None,
            selectedFontFamily: RState[str] = None,
            hoverBackgroundColor: RState[str] = None,
    ):
        headerColor = RColor().setQStyleAlpha(RColor.hexMistBlue, 0.36)
        hoverColor = RColor().setQStyleAlpha(RColor.hexCyanBlue, 0.16)
        selectedColor = RColor().setQStyleAlpha(RColor.hexCyanBlue, 0.34)
        self._styles = DictData(
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, headerColor)),
            Key(DqtStyle.atColor).Val(Remember.toValid(textColor, RColor.hexBlack)),
            Key(DqtStyle.atFontFamily).Val(Remember.toValid(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atFontSize).Val(Remember.toValid(fontSize, RFont.fzTinySize)),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
            Key(self.borderColor).Val(Remember.toValid(borderColor, RColor.hexGrey)),
            Key(self.selectedBackgroundColor).Val(Remember.toValid(selectedBackgroundColor, selectedColor)),
            Key(self.hoverBackgroundColor).Val(Remember.toValid(hoverBackgroundColor, hoverColor)),
            Key(self.selectedFontFamily).Val(Remember.toValid(selectedFontFamily, RFont.JhengHei))
        ).data
        super().__init__(self._styles)

    @property
    def borderStyleSheet(self):
        return DataBox(DqtStyle.valueCat(
            DqtStyle.Px(self.getStyle(self.borderWidth)),
            self.getStyle(self.borderStyle), self.getStyle(self.borderColor),
        )).data

    def getStyleSheet(self):
        return DqtStyle(
            color=self.getStyle(DqtStyle.atColor),
            fontSize=self.getStyle(DqtStyle.atFontSize),
            fontFamily=self.getStyle(DqtStyle.atFontFamily),
            appendix=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
                Key(DqtStyle.atBorderRight).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle), self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBorderBottom).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle), self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(0)),
                Key(DqtStyle.atFontWeight).Val(DqtStyle.valFontNormal),
                Key(DqtStyle.atPaddingLeft).Val(DqtStyle.Px(int(2)))
            ).data,
            selector=DqtStyle.QHeaderViewSection
        ).appendStyle(
            apply=DqtStyle.QHeaderViewSectionHover,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.hoverBackgroundColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QHeaderViewSectionChecked,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.selectedBackgroundColor)),
                Key(DqtStyle.atFontFamily).Val(self.getStyle(self.selectedFontFamily)),
                Key(DqtStyle.atFontSize).Val(DqtStyle.Pt(self.getStyle(DqtStyle.atFontSize))),
                Key(DqtStyle.atFontWeight).Val(DqtStyle.valFontNormal)
            ).data
        ).style


class TableViewStyle(DqtStyleEditor):
    borderColor = "borderColor"
    borderStyle = "borderStyle"
    borderWidth = "borderWidth"
    selectedBackgroundColor = "selectedBackgroundColor"
    selectedBorderColor = "selectedBorderColor"
    selectedBorderStyle = "selectedBorderStyle"
    selectedBorderRadius = "selectedBorderRadius"
    hoverBackgroundColor = "hoverBackgroundColor"
    focusOutlineColor = "focusOutlineColor"
    focusOutlineStyle = "focusOutlineStyle"
    cornerButtonColor = "cornerButtonColor"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            textColor: RState[str] = None,
            fontSize: RState[float] = None,
            backgroundColor: RState[str] = None,
            alternateBackgroundColor: RState[str] = None,
            gridlineColor: RState[str] = None,
            borderColor: RState[str] = None,
            borderStyle: RState[str] = None,
            borderWidth: RState[int] = None,
            selectedBackgroundColor: RState[str] = None,
            selectedBorderColor: RState[str] = None,
            selectedBorderStyle: RState[str] = None,
            selectedBorderRadius: RState[int] = None,
            hoverBackgroundColor: RState[str] = None,
            focusOutlineColor: RState[str] = None,
            focusOutlineStyle: RState[str] = None,
            cornerButtonColor: RState[str] = None,
            hearderStyle: HeaderViewStyle = None,
            scrollerStyle: ScrollerStyle = None,
    ):
        hoverColor = RColor().setQStyleAlpha(RColor.hexIceBlue, 0.84)
        selectedColor = RColor().setQStyleAlpha(RColor.hexDodgerBlue, 0.24)
        alternateColor = RColor().setQStyleAlpha(RColor.hexIceBlue, 0.34)
        cornerColor = RColor().setQStyleAlpha(RColor.hexMistBlue, 0.92)
        self._styles = DictData(
            Key(DqtStyle.atFontFamily).Val(Remember.toValid(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atFontSize).Val(Remember.toValid(fontSize, RFont.fzTinySize)),
            Key(DqtStyle.atColor).Val(Remember.toValid(textColor, RColor.hexBlack)),
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, RColor.hexWhite)),
            Key(DqtStyle.atAlternateBackgroundColor).Val(Remember.toValid(alternateBackgroundColor, alternateColor)),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
            Key(DqtStyle.atGridlineColor).Val(Remember.toValid(gridlineColor, RColor.hexLightGrey)),
            Key(self.borderColor).Val(Remember.toValid(borderColor, RColor.hexDarkGrey)),
            Key(self.selectedBackgroundColor).Val(Remember.toValid(selectedBackgroundColor, selectedColor)),
            Key(self.selectedBorderColor).Val(Remember.toValid(selectedBorderColor, RColor.hexGrey)),
            Key(self.selectedBorderStyle).Val(Remember.toValid(selectedBorderStyle, DqtStyle.valBorderSolid)),
            Key(self.selectedBorderRadius).Val(Remember.toValid(selectedBorderRadius, int(0))),
            Key(self.hoverBackgroundColor).Val(Remember.toValid(hoverBackgroundColor, hoverColor)),
            Key(self.focusOutlineColor).Val(Remember.toValid(focusOutlineColor, RColor.hexDeepStoneBlue)),
            Key(self.focusOutlineStyle).Val(Remember.toValid(focusOutlineStyle, DqtStyle.valBorderSolid)),
            Key(self.cornerButtonColor).Val(Remember.toValid(cornerButtonColor, cornerColor)),
        ).data
        super().__init__(self._styles)
        self._hearderStyle = Validate(hearderStyle, HeaderViewStyle())
        self._scrollerStyle = Validate(scrollerStyle, ScrollerStyle(scrollBarBackground=RColor.hexPureMist))

    @property
    def styleValues(self):
        styles = list(self._styles.values()) + list(self._hearderStyle.styles.values())
        styles += list(self._scrollerStyle.styles.values())
        return styles

    def getStyleSheet(self):
        headerBorder: str = self._hearderStyle.borderStyleSheet
        return DqtStyle(
            fontSize=self.getStyle(DqtStyle.atFontSize),
            fontFamily=self.getStyle(DqtStyle.atFontFamily),
            color=self.getStyle(DqtStyle.atColor),
            appendix=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle), self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(0)),
                Key(DqtStyle.atOutline).Val(DqtStyle.valueCat(
                    DqtStyle.Px(int(1)), self.getStyle(self.focusOutlineStyle),
                    self.getStyle(self.focusOutlineColor),
                )),
                Key(DqtStyle.atAlternateBackgroundColor).Val(self.getStyle(DqtStyle.atAlternateBackgroundColor)),
                Key(DqtStyle.atGridlineColor).Val(self.getStyle(DqtStyle.atGridlineColor))
            ).data,
            selector=DqtStyle.QTableView
        ).appendStyle(
            apply=DqtStyle.QTableViewQTableCornerButtonSection,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.cornerButtonColor)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(0)),
                Key(DqtStyle.atBorderBottom).Val(headerBorder),
                Key(DqtStyle.atBorderRight).Val(headerBorder),
                Key(DqtStyle.atBorderLeft).Val(DqtStyle.valNoBorder),
                Key(DqtStyle.atBorderTop).Val(DqtStyle.valNoBorder)
            ).data
        ).appendStyle(
            apply=DqtStyle.QTableViewItemHover,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.hoverBackgroundColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QTableViewItemSelected,
            styles=DictData(
                Key(DqtStyle.atColor).Val(self.getStyle(DqtStyle.atColor)),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.selectedBackgroundColor)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(int(1)), self.getStyle(self.selectedBorderStyle),
                    self.getStyle(self.selectedBorderColor),
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(self.selectedBorderRadius)))
            ).data
        ).mergeStyle(
            styleSheet=self._scrollerStyle.getStyleSheet()
        ).mergeStyle(
            styleSheet=self._hearderStyle.getStyleSheet()
        ).style


class ColoredTableView(TableView):
    MinHorizontalHeaderHeight: LutPixel = int(38)
    MinVerticalHeaderWidth: LutPixel = int(26)

    def __init__(
            self,
            size: QSize = None,
            fixedWidth: int = None,
            fixedHeight: int = None,
            dataModel: TableData = None,
            fields: TableFields = None,
            fieldMap: TableFieldMap = None,
            hiddenFields: TableFields = None,
            decimalRound: int = None,
            horizontalHeaderMinHeight: LutPixel = None,
            verticalHeaderMinWidth: LutPixel = None,
            wheelRate: float = None,
            styleEditor: TableViewStyle = None,
            parent: QWidget = None,
            onActivated: Callable = None,
            areaSelection: RState[CellArea] = None,
            cellSelection: RState[CellAt] = None,
            retainFocus: RState[bool] = False,
            locateCellTrig: Remember = None,
            contentRemain: LutPixel = None,
            viewportMargin: LutPixel = None,
            autoColumnResize: RState[bool] = False,
            adjustTableTrig: Remember = None,
            locateRowTrig: Remember = None,
            copyCellsTrig: Remember = None,
            locateRowsTrig: Remember = None,
            clearSelectionTrig: Remember = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__(
            size=size,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            dataModel=dataModel,
            fields=fields,
            hiddenFields=hiddenFields,
            fieldMap=fieldMap,
            parent=parent,
            onActivated=onActivated,
            decimalRound=decimalRound,
            contentRemain=contentRemain,
            areaSelection=areaSelection,
            retainFocus=retainFocus,
            wheelRate=wheelRate,
            cellSelection=cellSelection,
            autoColumnResize=autoColumnResize,
            adjustTableTrig=adjustTableTrig,
            copyCellsTrig=copyCellsTrig,
            locateCellTrig=locateCellTrig,
            viewportMargin=viewportMargin,
            locateRowTrig=locateRowTrig,
            locateRowsTrig=locateRowsTrig,
            clearSelectionTrig=clearSelectionTrig,
            triggers=triggers
        )
        self._styleEditor = Validate(styleEditor, TableViewStyle())
        self.setAlternatingRowColors(True)
        for v in self._styleEditor.styleValues:
            if isinstance(v, Remember):
                v.connect(partial(self.updateStyle), host=self)
        self.setEditTriggers(QTableView.NoEditTriggers)
        self.setCornerButtonEnabled(False)
        horizontalHeaderMinHeight = Validate(horizontalHeaderMinHeight, self.MinHorizontalHeaderHeight)
        verticalHeaderMinWidth = Validate(verticalHeaderMinWidth, self.MinVerticalHeaderWidth)
        self.horizontalHeader().setMinimumHeight(horizontalHeaderMinHeight)
        self.verticalHeader().setMinimumWidth(verticalHeaderMinWidth)
        self.horizontalHeader().setHighlightSections(True)
        self.verticalHeader().setHighlightSections(True)
        self.activateHeaderSelection()
        self.updateStyle()

    # noinspection PyUnresolvedReferences
    def activateHeaderSelection(self):
        self.horizontalHeader().sectionPressed.connect(lambda: self.setAutoScroll(True))
        self.verticalHeader().sectionPressed.connect(lambda: self.setAutoScroll(True))
        self.horizontalHeader().sectionClicked.connect(lambda: self.setAutoScroll(False))
        self.verticalHeader().sectionClicked.connect(lambda: self.setAutoScroll(False))
        return None

    def updateStyle(self):
        self.setStyleSheet(self._styleEditor.getStyleSheet())
        return None

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.setAutoScroll(True)
        return None

    def mouseReleaseEvent(self, e):
        self.setAutoScroll(False)
        super().mouseReleaseEvent(e)
        return None

    def leaveEvent(self, a0):
        self.setAutoScroll(False)
        super().leaveEvent(a0)
        return None
