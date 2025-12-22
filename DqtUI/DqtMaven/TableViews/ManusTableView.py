from functools import partial
from typing import Callable, Union, Dict, List, Optional, Iterable

from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, Trigger, Run, InputRequest, ReferState, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import SeqToState, ValToState, Execute
from DeclarativeQt.DqtUI.DqtLayouts.Layout import Column, Row
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.Dialogs.MetaDialogs.NoteDialog import NoteDialog
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabel, IndicatorLabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Layouts.LazyLayout import LazyColumn
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import HorizontalSpacer
from DeclarativeQt.DqtUI.DqtMaven.TableViews.BaseTableView.TableView import TableData, TableFields, \
    CellArea, CellAt, RowData, RowIndex, TableFieldMap
from DeclarativeQt.DqtUI.DqtMaven.TableViews.ColoredTableView import TableViewStyle, ColoredTableView
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BorderedTextField import TextFieldStyle
from DeclarativeQt.DqtUI.DqtMaven.TextFields.DataEditor.DataEditor import DataEditor
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import GList, Validate, ReferList, FixListLength, SumNestedList, \
    Key, DictData, Equal, GTuple, inRange, KeywordArgs, AnyArgs, EnumList, isEmpty, ConditionList, LimitVal
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Images.RImage import LutPixel
from DeclarativeQt.Resource.Strings.RString import RString

RowOptCallback = Union[Callable[[RowIndex, KeywordArgs], AnyArgs], Callable]


class ManusTableView(Column):
    MaxLocateRows: int = int(300)
    DefaultSize: QSize = QSize(480, 380)

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
            styleEditor: TableViewStyle = None,
            parent: QWidget = None,
            onActivated: Callable = None,
            wheelRate: float = None,
            areaSelection: RState[CellArea] = None,
            cellSelection: RState[CellAt] = None,
            retainFocus: RState[bool] = False,
            contentRemain: LutPixel = None,
            viewportMargin: LutPixel = None,
            autoColumnResize: RState[bool] = False,
            triggers: Dict[Remember, Callable] = None,
            buttonSize: QSize = None,
            buttonRadiusRatio: float = 0.15,
            rowEditDialog: InputRequest = None,
            refreshMethod: Callable = None,
            deleteRowWarning: str = None,
            deleteRowsWarning: str = None,
            warningTitle: str = None,
            insertDataMethod: RowOptCallback = None,
            deleteDataMethod: RowOptCallback = None,
            moveDataMethod: RowOptCallback = None,
            editDataMethod: RowOptCallback = None
    ):
        size = Validate(size, QSize(self.DefaultSize))
        dataModel = SeqToState(dataModel)
        if fields is None:
            fields = ReferState(dataModel, referExp=lambda a0: ColoredTableView.deriveMockFields(a0))
        fields = ValToState(fields)
        buttonSize = Validate(buttonSize, QSize(30, 30))
        adjustTableTrig = Trigger()
        locateRowTrig = Trigger()
        locateRowsTrig = Trigger()
        clearSelectionTrig = Trigger()
        locateCellTrig = Trigger()
        copyCellsTrig = Trigger()
        editorDialogOffset = lambda: QPoint(self.width(), 0)
        cellSelection = ValToState(cellSelection)
        areaSelection = ValToState(areaSelection)
        validateRow = lambda row: LimitVal(row, int(0), finalRow())
        currentRow = lambda: cellSelection.value().x()
        currentRows = lambda: list(set(ReferList(areaSelection.value(), lambda a0: a0.x())))
        aboveRows = lambda: ReferList(currentRows(), lambda a0: a0 - int(1))
        nextRow = lambda: cellSelection.value().x() + int(1)
        nextRows = lambda: ReferList(currentRows(), lambda a0: a0 + int(1))
        finalRow = lambda: len(dataModel.value()) - int(1)
        anchorAtRow = lambda row: cellSelection.setValue(QPoint(validateRow(row), int(0)))
        anchorAtRows = lambda rows: areaSelection.setValue(ReferList(rows, lambda a0: QPoint(a0, int(0))))
        tooManyRows = lambda: not isEmpty(areaSelection.value()) and len(currentRows()) > self.MaxLocateRows
        locateRows = lambda: locateRowTrig.trig() if tooManyRows() else locateRowsTrig.trig()
        super().__init__(
            padding=int(0),
            horizontalPadding=int(0),
            autoExpandToMaxCross=GList(0),
            autoExpandContentAt=int(1),
            options=GList(Column.AutoSizeNoRemain),
            autoContentResize=True,
            alignment=Column.Align.Left,
            content=GList(
                Row(
                    options=GList(Row.AutoSizeNoRemain),
                    autoContentResize=False,
                    fixHeight=True,
                    arrangement=Row.Align.Left,
                    padding=int(0),
                    spacing=int(5),
                    content=GList(
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.content_copy_fill_lightblue),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: copyCellsTrig.trig()
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.refresh),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                refreshMethod(), cellSelection.setValue(None), areaSelection.setValue(None)
                            ) if refreshMethod else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.auto_awesome_mosaic),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: adjustTableTrig.trig()
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.point_scan),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: locateRows()
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.edit_square_darkblue),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowTrig.trig(), self.editRowData(
                                    dataModel=dataModel, editAt=currentRow(),
                                    fields=fields, fieldMap=fieldMap,
                                    parent=self, dialogOffset=editorDialogOffset(),
                                    inputDialog=rowEditDialog, editDataMethod=editDataMethod,
                                ), locateRowTrig.trig()
                            ) if cellSelection.value() is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.add_circle),
                            size=buttonSize,
                            enable=ReferState(
                                fields, referExp=lambda a0: False if isEmpty(a0) else True
                            ),
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                anchorAtRow(finalRow()), locateRowTrig.trig()
                            ) if self.insertRowData(
                                dataModel=dataModel, insertAt=int(-1),
                                fields=fields, fieldMap=fieldMap,
                                parent=self, dialogOffset=editorDialogOffset(),
                                inputDialog=rowEditDialog, insertDataMethod=insertDataMethod,
                            ) is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.add_row_below),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowTrig.trig(), Run(
                                    anchorAtRow(nextRow()), locateRowTrig.trig(),
                                ) if self.insertRowData(
                                    dataModel=dataModel, insertAt=nextRow(),
                                    insertDataMethod=insertDataMethod, fields=fields,
                                    parent=self, dialogOffset=editorDialogOffset(),
                                    inputDialog=rowEditDialog, fieldMap=fieldMap,
                                ) is not None else None,
                            ) if cellSelection.value() is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.switch_access_shortcut_add),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowTrig.trig(), locateRowTrig.trig() if self.insertRowData(
                                    dataModel=dataModel, insertAt=cellSelection.value().x(),
                                    fields=fields, fieldMap=fieldMap,
                                    parent=self, dialogOffset=editorDialogOffset(),
                                    insertDataMethod=insertDataMethod, inputDialog=rowEditDialog,
                                ) is not None else None,
                            ) if cellSelection.value() is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.move_up),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowsTrig.trig(), Run(
                                    anchorAtRows(aboveRows()), locateRowsTrig.trig(),
                                ) if self.moveTableRows(
                                    dataModel=dataModel, fromRows=currentRows(),
                                    step=int(-1), fields=fields, moveDataMethod=moveDataMethod,
                                ) is True else None
                            ) if cellSelection.value() is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.move_down),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowsTrig.trig(), Run(
                                    anchorAtRows(nextRows()), locateRowsTrig.trig(),
                                ) if self.moveTableRows(
                                    dataModel=dataModel, fromRows=currentRows(),
                                    step=int(+1), fields=fields, moveDataMethod=moveDataMethod,
                                ) is True else None
                            ) if cellSelection.value() is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.backspace),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowTrig.trig(), Run(
                                    self.deleteRowData(
                                        dataModel=dataModel, deleteAt=cellSelection.value().x(),
                                        deleteDataMethod=deleteDataMethod, fields=fields
                                    ), cellSelection.setValue(None), areaSelection.setValue(None)
                                ) if NoteDialog.warning(
                                    parent=self, title=warningTitle,
                                    text=Validate(deleteRowWarning, RString.pEmpty),
                                    buttonHint=NoteDialog.StandardRequire
                                ) in GList(NoteDialog.Yes) else None
                            ) if cellSelection.value() is not None else None
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.delete_forever),
                            size=buttonSize,
                            fixedRadiusRatio=buttonRadiusRatio,
                            onClick=lambda: Run(
                                locateRowsTrig.trig(), Run(
                                    self.deleteTableRows(
                                        dataModel=dataModel, targetRows=currentRows(),
                                        deleteDataMethod=deleteDataMethod, fields=fields
                                    ), cellSelection.setValue(None), areaSelection.setValue(None)
                                ) if NoteDialog.warning(
                                    parent=self, title=warningTitle,
                                    text=Validate(deleteRowsWarning, RString.pEmpty),
                                    buttonHint=NoteDialog.StandardRequire
                                ) in GList(NoteDialog.Yes) else None
                            ) if cellSelection.value() is not None else None
                        ),
                    )
                ),
                ColoredTableView(
                    size=size,
                    fixedWidth=fixedWidth,
                    fixedHeight=fixedHeight,
                    dataModel=dataModel,
                    fields=fields,
                    fieldMap=fieldMap,
                    hiddenFields=hiddenFields,
                    decimalRound=decimalRound,
                    horizontalHeaderMinHeight=horizontalHeaderMinHeight,
                    verticalHeaderMinWidth=verticalHeaderMinWidth,
                    styleEditor=styleEditor,
                    parent=parent,
                    wheelRate=wheelRate,
                    onActivated=onActivated,
                    areaSelection=areaSelection,
                    cellSelection=cellSelection,
                    contentRemain=contentRemain,
                    viewportMargin=viewportMargin,
                    autoColumnResize=autoColumnResize,
                    retainFocus=retainFocus,
                    triggers=triggers,
                    locateCellTrig=locateCellTrig,
                    copyCellsTrig=copyCellsTrig,
                    adjustTableTrig=adjustTableTrig,
                    locateRowTrig=locateRowTrig,
                    locateRowsTrig=locateRowsTrig,
                    clearSelectionTrig=clearSelectionTrig,
                )
            )
        )

    @staticmethod
    def moveTableRows(
            dataModel: TableData = None,
            fromRows: List[int] = None,
            step: int = None,
            fields: TableFields = None,
            moveDataMethod: RowOptCallback = None,
    ) -> bool:
        rows = Remember.getValue(dataModel)
        if not rows or not step:
            return False
        fromRows = ConditionList(Validate(fromRows, list()), lambda a0: inRange(a0, int(0), len(rows)))
        step = max(min(step, len(rows) - int(1) - max(fromRows)), int(0) - min(fromRows))
        if isEmpty(fromRows) or Equal(step, int(0)):
            return False
        fromRows.sort(reverse=bool(step > int(0)))
        for row in fromRows:
            ManusTableView.moveRowData(dataModel, row, row + step, fields, moveDataMethod)
        return True

    @staticmethod
    def moveRowData(
            dataModel: TableData = None,
            fromAt: int = int(-1),
            moveTo: int = None,
            fields: TableFields = None,
            moveDataMethod: RowOptCallback = None,
    ) -> bool:
        rows = Remember.getValue(dataModel)
        if not rows or not inRange(fromAt, int(0), len(rows)) or moveTo is None:
            return False
        moveTo = min(max(moveTo, int(0)), len(rows) - int(1))
        if Equal(fromAt, moveTo):
            return False
        if moveTo > fromAt:
            moved = rows[:fromAt] + rows[int(fromAt + 1):int(moveTo + 1)]
            moved += GList(rows[fromAt]) + rows[int(moveTo + 1):]
        else:
            moved = rows[:moveTo] + GList(rows[fromAt])
            moved += rows[moveTo:fromAt] + rows[int(fromAt + 1):]
        if isinstance(dataModel, Remember):
            dataModel.setValue(moved)
        rowArgs = Remember.getValue(rows[fromAt])
        if moveDataMethod:
            moveDataMethod(moveTo, **dict(zip(Remember.getValue(fields), rowArgs)))
        return True

    @staticmethod
    def deleteTableRows(
            dataModel: TableData = None,
            targetRows: List[int] = None,
            deleteDataMethod: RowOptCallback = None,
            fields: TableFields = None
    ) -> None:
        targetRows = Validate(targetRows, list())
        targetRows = EnumList(sorted(targetRows), lambda i, a0: a0 - i)
        for row in targetRows:
            ManusTableView.deleteRowData(dataModel, row, deleteDataMethod, fields)
        return None

    @staticmethod
    def deleteRowData(
            dataModel: TableData = None,
            deleteAt: int = int(-1),
            deleteDataMethod: RowOptCallback = None,
            fields: TableFields = None
    ) -> bool:
        rows = Remember.getValue(dataModel)
        if not rows or not inRange(deleteAt, int(0), len(rows)):
            return False
        rowArgs = Remember.getValue(rows[deleteAt])
        if isinstance(dataModel, Remember):
            dataModel.setValue(rows[:deleteAt] + rows[int(deleteAt + 1):])
        if deleteDataMethod is not None:
            deleteDataMethod(deleteAt, **dict(zip(Remember.getValue(fields), rowArgs)))
        return True

    @staticmethod
    def insertRowData(
            dataModel: TableData = None,
            insertAt: int = int(-1),
            fields: TableFields = None,
            fieldMap: TableFieldMap = None,
            parent: QWidget = None,
            requestTitle: str = None,
            dialogOffset: QPoint = None,
            inputDialog: InputRequest = None,
            insertDataMethod: RowOptCallback = None,
    ) -> Optional[Iterable]:
        if dataModel is None:
            return None
        request = partial(ManusTableView.executeRowInputRequest, None)
        args = GTuple(fields, fieldMap, parent, requestTitle, dialogOffset, inputDialog)
        result = request(*args)
        if result is None:
            return None
        rows = Validate(Remember.getValue(dataModel), list())
        count = len(rows)
        index = insertAt % (count + 1) if insertAt < 0 else insertAt if insertAt < count else count
        if isinstance(dataModel, Remember):
            dataModel.setValue(rows[:index] + GList(Remember(result)) + rows[index:])
        if insertDataMethod is not None:
            insertDataMethod(index, **dict(zip(Remember.getValue(fields), result)))
        return result

    @staticmethod
    def editRowData(
            dataModel: TableData = None,
            editAt: int = int(-1),
            fields: TableFields = None,
            fieldMap: TableFieldMap = None,
            parent: QWidget = None,
            requestTitle: str = None,
            dialogOffset: QPoint = None,
            inputDialog: InputRequest = None,
            editDataMethod: RowOptCallback = None
    ) -> Optional[Iterable]:
        dataModel = Remember.getValue(dataModel)
        if not dataModel or not inRange(editAt, int(0), len(dataModel)):
            return None
        args = GTuple(dataModel[editAt], fields, fieldMap, parent, requestTitle, dialogOffset, inputDialog)
        result = ManusTableView.executeRowInputRequest(*args)
        if result is None:
            return None
        if editDataMethod is not None:
            editDataMethod(editAt, **dict(zip(Remember.getValue(fields), result)))
        return result

    @staticmethod
    def executeRowInputRequest(
            rowData: RowData = None,
            fields: TableFields = None,
            fieldMap: TableFieldMap = None,
            parent: QWidget = None,
            requestTitle: str = None,
            dialogOffset: QPoint = None,
            inputDialog: InputRequest = None,
    ) -> Optional[Iterable]:
        args = GTuple(rowData, fields, fieldMap, parent, requestTitle, dialogOffset)
        request = Validate(inputDialog, partial(ManusTableView.sampleRowEditDialog))
        result = request(*args)
        if result is None:
            return None
        if isinstance(rowData, Remember):
            rowData.setValue(result)
        return result

    @staticmethod
    def sampleRowEditDialog(
            rowData: RowData = None,
            fields: TableFields = None,
            fieldMap: TableFieldMap = None,
            parent: QWidget = None,
            dialogTitle: str = None,
            dialogOffset: QPoint = None,
            dialogWidth: int = int(480),
            labelWidth: int = int(100),
            textFieldWidth: int = int(270),
            lineHeight: int = int(30),
            scrollAreaHeight: int = int(460),
            editorBorderRadius: int = int(3)
    ) -> Optional[Iterable]:
        fields = Remember.getValue(fields)
        count = len(fields)
        fieldNames = ColoredTableView.fieldsName(fields, fieldMap)
        defaultInputs = Validate(Remember.getValue(rowData), list())
        defaultInputs = FixListLength(defaultInputs, count, RString.pEmpty)
        acceptor = Trigger()
        itemSpace = int(7)
        data = SeqToState(defaultInputs)
        result = Execute(
            Dialog(
                parent=parent,
                title=dialogTitle,
                fixedWidth=dialogWidth,
                offset=dialogOffset,
                acceptTrig=acceptor,
                style=DqtStyle(
                    appendix=DictData(
                        Key(DqtStyle.atBackgroundColor).Val(RColor.hexLightWhite)
                    ).data,
                    selector=DqtStyle.QWidget
                ).style,
                content=Column(
                    autoContentResize=False,
                    spacing=int(30),
                    padding=int(20),
                    content=GList(
                        LazyColumn(
                            autoContentResize=False,
                            scrollAreaHeight=scrollAreaHeight,
                            style=DqtStyle(
                                appendix=DictData(
                                    Key(DqtStyle.atBackgroundColor).Val(RColor.hexLightWhite)
                                ).data,
                                selector=DqtStyle.QWidget
                            ).style,
                            alignment=Column.Align.HCenter,
                            padding=int(20),
                            spacing=int(10),
                            arrangement=Column.Align.Top,
                            content=SumNestedList(
                                ReferList(
                                    range(count), lambda i: GList(
                                        Row(
                                            autoContentResize=True,
                                            alignment=Row.Align.VCenter,
                                            content=GList(
                                                IndicatorLabel(
                                                    size=QSize(labelWidth, lineHeight),
                                                    alignment=IndicatorLabel.Align.Center,
                                                    indicatorStyle=IndicatorLabelStyle(
                                                        normalBackground=RColor.hexIceBlue,
                                                        borderRadius=editorBorderRadius,
                                                    ),
                                                    fixedHeight=lineHeight,
                                                    text=fieldNames[i]
                                                ),
                                                HorizontalSpacer(width=itemSpace, fixed=True),
                                                DataEditor(
                                                    size=QSize(textFieldWidth, lineHeight),
                                                    fixedHeight=lineHeight,
                                                    styleEditor=TextFieldStyle(
                                                        borderRadius=editorBorderRadius
                                                    ),
                                                    data=Remember.getValue(data)[i]
                                                ),
                                            )
                                        ),
                                        HorizontalDivider(
                                            fixedLength=textFieldWidth + labelWidth + itemSpace,
                                            color=RColor().setQStyleAlpha(RColor.hexSoftStone, 0.4)
                                        )
                                    )
                                )
                            )
                        ),
                        IconButton(
                            icon=RIcon().loadIconPixmap(RIcon.Src.select_check_box),
                            fixedWidth=textFieldWidth + labelWidth,
                            fixedHeight=int(40),
                            fixedRadiusRatio=0.15,
                            onClick=lambda: acceptor.trig(),
                            shortCut=Qt.Key_Return
                        ),
                    )
                )
            )
        )
        if Equal(result, Dialog.Accepted):
            dataWash = lambda x: x.strip() if isinstance(x, str) else x
            return ReferList(Remember.getListValue(data), dataWash)
        return None
