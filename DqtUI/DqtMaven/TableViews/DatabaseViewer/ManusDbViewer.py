from functools import partial
from typing import Callable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, InputRequest, ReferState, Trigger, RState
from DeclarativeQt.DqtUI.DqtMaven.TableViews.BaseTableView.TableView import CellArea, CellAt, \
    TableFields
from DeclarativeQt.DqtUI.DqtMaven.TableViews.ColoredTableView import TableViewStyle
from DeclarativeQt.DqtUI.DqtMaven.TableViews.DatabaseViewer.SqliteDbViewer import FetchDbMethod, \
    SqliteDbViewer
from DeclarativeQt.DqtUI.DqtMaven.TableViews.ManusTableView import ManusTableView, \
    RowOptCallback
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Images.RImage import LutPixel
from DeclarativeQt.Resource.Strings.RStr import NLIndex, RStr
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import SqlDatabase
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDbMethod import SqlDbMethod


class ManusDbViewer(ManusTableView):
    def __init__(
            self,
            size: QSize = None,
            fixedWidth: int = None,
            fixedHeight: int = None,
            sqlDb: RState[SqlDatabase] = None,
            fetchDataMethod: FetchDbMethod = None,
            language: RState[NLIndex] = None,
            hiddenFields: TableFields = None,
            wheelRate: float = None,
            decimalRound: int = None,
            horizontalHeaderMinHeight: LutPixel = None,
            verticalHeaderMinWidth: LutPixel = None,
            styleEditor: TableViewStyle = None,
            parent: QWidget = None,
            onActivated: Callable = None,
            areaSelection: RState[CellArea] = None,
            cellSelection: RState[CellAt] = None,
            retainFocus: RState[bool] = False,
            contentRemain: LutPixel = None,
            viewportMargin: LutPixel = None,
            autoColumnResize: RState[bool] = False,
            triggers: Dict[Remember, Callable] = None,
            reloadTrig: Trigger = None,
            buttonSize: QSize = None,
            buttonRadiusRatio: float = 0.15,
            rowEditDialog: InputRequest = None,
            deleteRowWarning: str = None,
            deleteRowsWarning: str = None,
            warningTitle: str = None,
            insertDataMethod: RowOptCallback = None,
            deleteDataMethod: RowOptCallback = None,
            moveDataMethod: RowOptCallback = None,
            editDataMethod: RowOptCallback = None
    ):
        tableToDataModel = SqliteDbViewer.tableToDataModel
        language = Validate(language, RStr.EN)
        dbFieldMap = lambda a0, a1, t0=None: a0.dbFieldNLMap(a1) if a0 else None
        fetchDataMethod = Validate(fetchDataMethod, partial(SqlDbMethod.fetchSqlTable))
        fields = lambda a0, t0=None: a0.dbFields if a0 else list()
        tableData = lambda a0, t0=None: tableToDataModel(fetchDataMethod(a0, fields(a0))) if a0 else None
        reloadTrig = Validate(reloadTrig, Trigger())
        super().__init__(
            size=size,
            dataModel=ReferState(sqlDb, reloadTrig, referExp=tableData),
            fieldMap=ReferState(sqlDb, language, reloadTrig, referExp=dbFieldMap),
            fields=ReferState(sqlDb, reloadTrig, referExp=fields),
            hiddenFields=hiddenFields,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            horizontalHeaderMinHeight=horizontalHeaderMinHeight,
            verticalHeaderMinWidth=verticalHeaderMinWidth,
            styleEditor=styleEditor,
            parent=parent,
            wheelRate=wheelRate,
            onActivated=onActivated,
            autoColumnResize=autoColumnResize,
            retainFocus=retainFocus,
            areaSelection=areaSelection,
            cellSelection=cellSelection,
            contentRemain=contentRemain,
            viewportMargin=viewportMargin,
            decimalRound=decimalRound,
            triggers=triggers,
            buttonSize=buttonSize,
            buttonRadiusRatio=buttonRadiusRatio,
            rowEditDialog=rowEditDialog,
            refreshMethod=lambda: reloadTrig.trig(),
            deleteRowWarning=deleteRowWarning,
            deleteRowsWarning=deleteRowsWarning,
            warningTitle=warningTitle,
            editDataMethod=editDataMethod,
            deleteDataMethod=deleteDataMethod,
            moveDataMethod=moveDataMethod,
            insertDataMethod=insertDataMethod
        )
