from decimal import Decimal
from functools import partial
from typing import Union, List, Callable, Dict, Optional, Any

import pyperclip
from PyQt5.QtCore import QSize, Qt, QPoint, QTimer, QModelIndex, QItemSelectionModel, QItemSelection
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QWidget, QAbstractItemView

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtUI.DqtTools.Scroller import ScrollRate
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, ReferList, Equal, isEmpty, IndexSubSeq, isValid, \
    ConditionList, DictData, Key, GStr, GList
from DeclarativeQt.Resource.Images.RImage import LutPixel
from DeclarativeQt.Resource.PhyMetrics.PhyMtrBase.PhyMtrBase import PhyMeasure
from DeclarativeQt.Resource.Strings.RString import RString
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import FieldNLMap

CellArea = Optional[List[QPoint]]
CellAt = Optional[QPoint]
CellData = Union[str, float, int, Decimal, bool, Any]
RowData = RState[List[CellData]]
RowIndex = int
TableFields = RState[List[str]]
TableFieldMap = RState[FieldNLMap]
TableData = RState[List[RowData]]


class TableView(QTableView):
    DefaultSize = QSize(400, 200)
    DefaultScrollRate: ScrollRate = 0.32
    DefaultContentRemain: LutPixel = int(8)
    DefaultViewportMargin: LutPixel = int(4)

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
            style: RState[str] = None,
            parent: QWidget = None,
            onActivated: Callable = None,
            wheelRate: float = None,
            cellSelection: RState[CellAt] = None,
            areaSelection: RState[CellArea] = None,
            autoColumnResize: RState[bool] = False,
            retainFocus: RState[bool] = False,
            contentRemain: LutPixel = None,
            viewportMargin: LutPixel = None,
            locateCellTrig: Remember = None,
            locateRowTrig: Remember = None,
            locateRowsTrig: Remember = None,
            adjustTableTrig: Remember = None,
            copyCellsTrig: Remember = None,
            clearSelectionTrig: Remember = None,
            copyLinker: str = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__()
        size = Validate(size, QSize(self.DefaultSize))
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        self._fixedWidth = None if not fixedWidth else max(fixedWidth, DqtCanvasBase.MinWidth)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        if self._fixedWidth:
            size.setWidth(self._fixedWidth)
        self.setFixedSize(size)
        if parent:
            self.setParent(parent)
        if style:
            self.setStyleSheet(Remember.getValue(style))
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        self._autoColumnResize = autoColumnResize
        self._contentRemain = Validate(contentRemain, self.DefaultContentRemain)
        self._viewportMargin = Validate(viewportMargin, self.DefaultViewportMargin)
        self._tableModel: Optional[QStandardItemModel] = None
        self._initAdjust = False
        self._wheelRate = Validate(wheelRate, self.DefaultScrollRate)
        self._focusOn = False
        self._copyLinker = Validate(copyLinker, RString.pLinefeed)
        self._decimalRound = Validate(decimalRound, PhyMeasure.DecimalRound)
        self._retainFocus = retainFocus
        self._areaSelection = Validate(areaSelection, Remember(None))
        self._cellSelection = Validate(cellSelection, Remember(None))
        if isinstance(dataModel, Remember):
            dataModel.connect(lambda value: self.setDataModel(value, fields, fieldMap, hiddenFields), host=self)
        if isinstance(fields, Remember):
            fields.connect(lambda value: self.setColumnLabels(value, fieldMap), host=self)
            fields.connect(lambda value: self.hideTableFields(value, hiddenFields), host=self)
        if isinstance(fieldMap, Remember):
            fieldMap.connect(lambda value: self.setColumnLabels(fields, value), host=self)
        if isinstance(hiddenFields, Remember):
            hiddenFields.connect(lambda value: self.hideTableFields(fields, value), host=self)
        self.setDataModel(dataModel, fields, fieldMap, hiddenFields)
        # noinspection PyUnresolvedReferences
        self.activated.connect(partial(Validate(onActivated, lambda: None)))
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setAutoScroll(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QTableView.ExtendedSelection)
        optionTrigs = DictData(
            Key(adjustTableTrig).Val(self.adjustTableContents),
            Key(locateCellTrig).Val(self.locateCurrentCell),
            Key(locateRowTrig).Val(self.locateCurrentRow),
            Key(locateRowsTrig).Val(self.locateCurrentRows),
            Key(clearSelectionTrig).Val(self.clearSelection),
            Key(copyCellsTrig).Val(self.copyItemTexts)
        ).data
        for k, v in optionTrigs.items():
            if isinstance(k, Remember):
                k.connect(partial(v), host=self)
        triggers = Validate(triggers, dict())
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def copyItemTexts(self):
        indexes = self.currentAreaIndexes()
        if not indexes:
            return None
        texts = list()
        for index in indexes:
            texts.append(str(self.model().data(index)))
        pyperclip.copy(self._copyLinker.join(texts))
        return None

    def paintEvent(self, e):
        if not Remember.getValue(self._retainFocus):
            if self._areaSelection.value() is None:
                self.clearSelection()
        if not self._focusOn:
            self.setFocusPolicy(Qt.StrongFocus)
            self._focusOn = True
        super().paintEvent(e)
        return None

    @private
    def currentCellIndex(self) -> Optional[QModelIndex]:
        cell = self._cellSelection.value()
        return self.model().index(cell.x(), cell.y()) if cell is not None else None

    @private
    def currentAreaIndexes(self) -> Optional[List[QModelIndex]]:
        area = self._areaSelection.value()
        if area is None:
            return None
        toIndex = lambda a0: self.model().index(a0.x(), a0.y())
        area = ReferList(area, toIndex)
        return area

    def clearSelection(self):
        self.selectCellAt(None)
        self.selectionModel().clearSelection()
        self.clearFocus()
        super().clearSelection()
        return None

    def mouseReleaseEvent(self, e):
        if not Remember.getValue(self._retainFocus):
            if self._areaSelection.value() is not None:
                if self._cellSelection.value() not in self._areaSelection.value():
                    self.clearFocus()
                    self._cellSelection.setValue(self._areaSelection.value()[0])
        super().mouseReleaseEvent(e)
        return None

    @private
    def selectCellAt(self, cell: Optional[QPoint]):
        self._cellSelection.setValue(cell)
        if cell is None:
            self._areaSelection.setValue(None)
        return None

    def findRowInViewport(self, row: int) -> int:
        pos = self.rowViewportPosition(row)
        row_height = self.rowHeight(row)
        if pos < 0:
            return int(-1)
        elif pos >= self.viewport().height() - row_height:
            return int(+1)
        return int(0)

    @private
    def visibleColumns(self) -> List[int]:
        return ConditionList(range(self.model().columnCount()), lambda a0: not self.isColumnHidden(a0))

    def selectRows(self, rows: List[int]) -> None:
        if isEmpty(rows):
            return None
        visibleCols = self.visibleColumns()
        if isEmpty(visibleCols):
            return None
        rows = sorted(list(set(rows)))
        rowGroups = list()
        for row in rows:
            if isEmpty(rowGroups):
                rowGroups.append(GList(row))
            elif row > rowGroups[-1][-1] + int(1):
                rowGroups.append(GList(row))
            else:
                rowGroups[-1].append(row)
        for group in rowGroups:
            topLeft = self.model().index(group[0], visibleCols[0])
            bottomRight = self.model().index(group[-1], visibleCols[-1])
            rectArea = QItemSelection(topLeft, bottomRight)
            self.selectionModel().select(rectArea, QItemSelectionModel.Select)
        self.syncAreaSelection()
        self.selectCellAt(self._areaSelection.value()[0])
        return None

    def scrollToRow(self, row: int, col: int = None):
        posAt = self.findRowInViewport(row)
        if not posAt:
            return None
        visibleCols = self.visibleColumns()
        if isEmpty(visibleCols):
            return None
        col = Validate(col, visibleCols[0])
        mode = QAbstractItemView.PositionAtTop if posAt < 0 else QAbstractItemView.PositionAtBottom
        self.scrollTo(self.model().index(row, col), mode)
        return None

    def locateCurrentRows(self):
        indexes = self.currentAreaIndexes()
        if not indexes:
            return None
        rows = list(set(ReferList(indexes, lambda a0: a0.row())))
        self.setSelectionMode(QTableView.MultiSelection)
        self.clearSelection()
        self.selectRows(rows)
        self.scrollToRow(max(rows))
        self.scrollToRow(min(rows))
        self.setSelectionMode(QTableView.ExtendedSelection)
        return None

    def locateCurrentRow(self):
        index = self.currentCellIndex()
        if not index:
            return None
        self.selectRow(index.row())
        self.scrollToRow(index.row())
        return None

    def locateCurrentCell(self):
        index = self.currentCellIndex()
        if not index:
            return None
        self.setCurrentIndex(index)
        self.scrollToRow(index.row(), index.column())
        return None

    @private
    def syncTableSelection(self):
        self.syncAreaSelection()
        self.syncCellSelection()
        return None

    def syncCellSelection(self):
        index = self.selectionModel().currentIndex()
        if index.row() < 0 or index.column() < 0:
            index = None
        cell = QPoint(index.row(), index.column()) if index is not None else None
        self.selectCellAt(cell)
        return None

    def syncAreaSelection(self):
        indexes = self.selectionModel().selectedIndexes()
        if isEmpty(indexes):
            self._areaSelection.setValue(None)
            return None
        indexes = ReferList(indexes, lambda a0: QPoint(a0.row(), a0.column()))
        self._areaSelection.setValue(indexes)
        return None

    def wheelEvent(self, a0):
        if Equal(a0.modifiers(), Qt.ControlModifier):
            scroll_value = self.horizontalScrollBar().value()
            delta = int(a0.angleDelta().y() * self._wheelRate)
            self.horizontalScrollBar().setValue(scroll_value - delta)
        else:
            scroll_value = self.verticalScrollBar().value()
            delta = int(a0.angleDelta().y() * self._wheelRate)
            self.verticalScrollBar().setValue(scroll_value - delta)
        a0.accept()
        return None

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if not self._initAdjust:
            self.adjustTableContents()
            self._initAdjust = True
        self.autoAdjustColumnSize()
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        DqtCanvas.setFixedWidth(self, self._fixedWidth)
        return None

    def resizeColumnsToContents(self):
        super().resizeColumnsToContents()
        model = self.model()
        if not model:
            return None
        content_widths = list()
        for col in range(model.columnCount()):
            width = self.columnWidth(col) + self._contentRemain
            self.setColumnWidth(col, width)
            content_widths.append(width)
        if sum(content_widths) < self.viewportWidth():
            self.distributeColWidth(content_widths)
        return None

    @private
    def distributeColWidth(self, contentWidths: list):
        col_count = self.model().columnCount()
        if col_count <= 0:
            return None
        table_width = self.viewportWidth()
        col_widths = ReferList(contentWidths, lambda w: int(w * table_width / sum(contentWidths)))
        col_widths[-1] = table_width - sum(col_widths[:-1])
        for col in range(col_count):
            self.setColumnWidth(col, col_widths[col])
        return None

    @private
    def viewportWidth(self) -> LutPixel:
        return int(self.viewport().width() - self._viewportMargin)

    def resizeRowsToContents(self):
        super().resizeRowsToContents()
        if not self.model():
            return None
        for row in range(self.model().rowCount()):
            self.setRowHeight(row, self.rowHeight(row) + self._contentRemain)
        return None

    def adjustTableContents(self):
        self.resizeColumnsToContents()
        QTimer.singleShot(int(0), lambda: self.resizeRowsToContents())
        return None

    def autoAdjustColumnSize(self):
        if Remember.getValue(self._autoColumnResize):
            self.resizeColumnsToContents()
        return None

    @staticmethod
    def fieldsName(fields: TableFields, fieldMap: TableFieldMap = None):
        fields = Remember.getValue(fields)
        fieldMap = Remember.getValue(fieldMap)
        if fieldMap is None:
            return fields
        names = ReferList(fields, lambda a0: a0 if a0 not in fieldMap else fieldMap[a0])
        return names

    @staticmethod
    def deriveMockFields(dataModel: TableData):
        rows = Remember.getListValue(dataModel)
        if isEmpty(rows):
            return list()
        colCount = max(ReferList(rows, lambda a0: len(a0) if a0 else int(0)))
        return ReferList(range(colCount), lambda a0: str(a0))

    @staticmethod
    def fieldAtCols(fields: TableFields, hiddenFields: TableFields):
        fields = Remember.getValue(fields)
        hiddenFields = Remember.getValue(hiddenFields)
        if fields and hiddenFields:
            return IndexSubSeq(hiddenFields, fields)
        return list()

    def hideTableFields(self, fields: TableFields, hiddenFields: TableFields):
        hidenCols = self.fieldAtCols(fields, hiddenFields)
        for col in range(self.model().columnCount()):
            self.setColumnHidden(col, bool(col in hidenCols))
        return None

    def updateRowData(self, rowIndex: int, rowData: RowData):
        for col, data in enumerate(Remember.getValue(rowData)):
            self._tableModel.setItem(rowIndex, col, self.tableStandardItem(data))
        self.autoAdjustColumnSize()
        return None

    def setColumnLabels(self, fields: TableFields, fieldMap: TableFieldMap = None):
        labels = Remember.getValue(fields)
        if labels:
            labels = ReferList(labels, lambda x: GStr(x).strip())
            labels = self.fieldsName(labels, fieldMap)
            self._tableModel.setHorizontalHeaderLabels(labels)
        self.autoAdjustColumnSize()
        return None

    def tableStandardItem(self, item: Any) -> QStandardItem:
        if isinstance(item, float) or isinstance(item, Decimal):
            item = RString.decimalRound(float(item), self._decimalRound)
        return QStandardItem(GStr(item))

    def setDataModel(
            self, dataModel: TableData, fields: TableFields = None,
            fieldMap: TableFieldMap = None, hiddenFields: TableFields = None
    ) -> None:
        tableData = Remember.getListValue(dataModel)
        self._tableModel = QStandardItemModel(0, 0)
        if isValid(tableData):
            for row in tableData:
                self._tableModel.appendRow(ReferList(row, lambda item: self.tableStandardItem(item)))
            for i, row in enumerate(Remember.getValue(dataModel)):
                if isinstance(row, Remember):
                    row.uniqueConnect(self.updateRowData, i, host=self)
        self.setModel(self._tableModel)
        self.setColumnLabels(fields, fieldMap)
        self.hideTableFields(fields, hiddenFields)
        self.autoAdjustColumnSize()
        # noinspection PyUnresolvedReferences
        self.selectionModel().selectionChanged.connect(partial(self.syncTableSelection))
        # noinspection PyUnresolvedReferences
        self.selectionModel().currentChanged.connect(partial(self.syncCellSelection))
        return None
