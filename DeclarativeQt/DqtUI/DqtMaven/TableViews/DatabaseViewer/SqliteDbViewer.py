from functools import partial
from typing import Callable, Dict, Union, List

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, LambdaRemember, RState
from DeclarativeQt.DqtUI.DqtMaven.TableViews.BaseTableView.TableView import CellArea, CellAt, \
    TableFields
from DeclarativeQt.DqtUI.DqtMaven.TableViews.ColoredTableView import ColoredTableView, TableViewStyle
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, isEmpty
from DeclarativeQt.Resource.Images.RImage import LutPixel
from DeclarativeQt.Resource.Strings.RString import NLIndex, RString
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import SqlDatabase
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDbMethod import SqlDbMethod, SqlTableData

FetchDbMethod = Union[Callable[[SqlDatabase, List], SqlTableData], Callable]


class SqliteDbViewer(ColoredTableView):
    def __init__(
            self,
            size: QSize = None,
            fixedWidth: int = None,
            fixedHeight: int = None,
            sqlDb: RState[SqlDatabase] = None,
            fetchDataMethod: FetchDbMethod = None,
            language: RState[NLIndex] = None,
            hiddenFields: TableFields = None,
            decimalRound: int = None,
            reloadTrig: Remember = None,
            horizontalHeaderMinHeight: LutPixel = None,
            verticalHeaderMinWidth: LutPixel = None,
            styleEditor: TableViewStyle = None,
            wheelRate: float = None,
            parent: QWidget = None,
            onActivated: Callable = None,
            areaSelection: RState[CellArea] = None,
            cellSelection: RState[CellAt] = None,
            retainFocus: RState[bool] = False,
            autoColumnResize: RState[bool] = False,
            adjustTableTrig: Remember = None,
            locateCellTrig: Remember = None,
            contentRemain: LutPixel = None,
            viewportMargin: LutPixel = None,
            locateRowTrig: Remember = None,
            copyCellsTrig: Remember = None,
            locateRowsTrig: Remember = None,
            clearSelectionTrig: Remember = None,
            triggers: Dict[Remember, Callable] = None
    ):
        language = Validate(language, RString.EnglishIndex)
        dbFieldMap = lambda a0, a1, t0=None: a0.dbFieldNLMap(a1) if a0 else None
        fetchDataMethod = Validate(fetchDataMethod, partial(SqlDbMethod.fetchSqlTable))
        fields = lambda a0, t0=None: a0.dbFields if a0 else list()
        tableData = lambda a0, t0=None: self.tableToDataModel(fetchDataMethod(a0, fields(a0))) if a0 else None
        super().__init__(
            size=size,
            dataModel=LambdaRemember(sqlDb, reloadTrig, lambdaExp=tableData),
            fieldMap=LambdaRemember(sqlDb, language, reloadTrig, lambdaExp=dbFieldMap),
            fields=LambdaRemember(sqlDb, reloadTrig, lambdaExp=fields),
            hiddenFields=hiddenFields,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            horizontalHeaderMinHeight=horizontalHeaderMinHeight,
            verticalHeaderMinWidth=verticalHeaderMinWidth,
            styleEditor=styleEditor,
            parent=parent,
            onActivated=onActivated,
            autoColumnResize=autoColumnResize,
            retainFocus=retainFocus,
            decimalRound=decimalRound,
            areaSelection=areaSelection,
            wheelRate=wheelRate,
            cellSelection=cellSelection,
            adjustTableTrig=adjustTableTrig,
            locateCellTrig=locateCellTrig,
            contentRemain=contentRemain,
            viewportMargin=viewportMargin,
            locateRowTrig=locateRowTrig,
            copyCellsTrig=copyCellsTrig,
            locateRowsTrig=locateRowsTrig,
            clearSelectionTrig=clearSelectionTrig,
            triggers=triggers
        )

    @staticmethod
    def tableToDataModel(table: SqlTableData) -> SqlTableData:
        if isEmpty(table):
            return None
        dataModel = list()
        for row in table.copy():
            row = list(row)
            for i, item in enumerate(row):
                if item is None:
                    row[i] = RString.pEmpty
            dataModel.append(tuple(row))
        return dataModel
