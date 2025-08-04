import calendar
from abc import ABC
from datetime import datetime
from typing import Callable

from PyQt5.QtCore import QSize

from DeclarativeQt.DqtCore.DqtBase import Remember, LambdaRemember, Run, Trigger, RState
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember
from DeclarativeQt.DqtUI.DqtLayouts.Layout import Row, Column
from DeclarativeQt.DqtUI.DqtMaven.ComboBoxes.BorderedComboBox import BorderedComboBox, ComboBoxStyle
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabel, IndicatorLabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import HorizontalSpacer
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, DictData, Key, LambdaList, GList, isAllValid, \
    GInt, Equal, Countable, isValid
from DeclarativeQt.Resource.Grammars.RGrmBase.RGrmObject import DataBox, GTuple
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex

EditorMode = str


class TimeEditorCanvas(object):
    DefaultItemSpacing: int = int(1)
    DefaultItemPadding: int = int(1)
    DefaultLabelSpacing: int = int(3)
    DefaultDateTimeSpacing: int = int(14)
    DefaultYearEditorWidth: int = int(104)
    DefaultBaseWidth: int = int(80)
    DefaultVerticalPadding: int = int(1)
    DefaultEditorHeight: int = int(30)

    def __init__(
            self,
            itemSpacing: int = None,
            itemPadding: int = None,
            labelSpacing: int = None,
            dateTimeSpacing: int = None,
            verticalPadding: int = None,
            baseWidth: int = None,
            yearEditorWidth: int = None,
            editorHeight: int = None,
    ):
        self.itemSpacing = Validate(itemSpacing, self.DefaultItemSpacing)
        self.itemPadding = Validate(itemPadding, self.DefaultItemPadding)
        self.labelSpacing = Validate(labelSpacing, self.DefaultLabelSpacing)
        self.dateTimeSpacing = Validate(dateTimeSpacing, self.DefaultDateTimeSpacing)
        self.verticalPadding = Validate(verticalPadding, self.DefaultVerticalPadding)
        self.baseWidth = Validate(baseWidth, self.DefaultBaseWidth)
        self.yearEditorWidth = Validate(yearEditorWidth, self.DefaultYearEditorWidth)
        self.editorHeight = Validate(editorHeight, self.DefaultEditorHeight)


class TimeEditorBase(ABC):
    MinHour: int = int(0)
    MaxHour: int = int(23)
    MinMinute: int = int(0)
    MaxMinute: int = int(59)
    MinSecond: int = int(0)
    MaxSecond: int = int(59)
    MinDay: int = int(1)
    MaxDay = int(31)
    MinYear: int = int(1970)
    MaxYear: int = datetime.now().year + int(10)
    MinMonth: int = int(1)
    MaxMonth: int = int(12)


class TimeEditor(Row):
    Base = TimeEditorBase
    Canvas = TimeEditorCanvas
    DefaultSize: QSize = QSize(240, 30)
    Time: EditorMode = "Time"
    Date: EditorMode = "Date"
    DateTime: EditorMode = "DateTime"
    DateTimeParts: Countable = int(6)

    def __init__(
            self,
            editorMode: EditorMode = None,
            timeValue: RState[str] = None,
            onAnyActivated: Callable = None,
            allValidCheck: Remember[bool] = None,
            comboBoxStyle: ComboBoxStyle = None,
            labelBorderRadius: int = int(4),
            dateLabelBackground: str = None,
            labelFontSize: float = float(9.2),
            language: RState[NLIndex] = None,
            timeLabelBackground: str = None,
            invalidBackground: str = None,
            canvasModifier: TimeEditorCanvas = None
    ):
        canvasModifier = Validate(canvasModifier, TimeEditorCanvas())
        allValidCheck = Validate(allValidCheck, Remember(True))
        onAnyActivated = Validate(onAnyActivated, lambda *az: None)
        language = Validate(language, RString.EnglishIndex)
        comboBoxStyle = Validate(comboBoxStyle, self.DefaultComboBoxStyle)
        dateLabelBackground = Validate(dateLabelBackground, RColor.setQStyleAlpha(RColor.hexCyanBlue, 0.18))
        timeLabelBackground = Validate(timeLabelBackground, RColor.setQStyleAlpha(RColor.hexSteelBlue, 0.24))
        invalidBackground = Validate(invalidBackground, RColor.setQStyleAlpha(RColor.hexSoftRose, 0.7))
        editorMode = Validate(editorMode, self.DateTime)
        dtime = RString.datetimeToStandard(Remember.getValue(timeValue))
        dtime = Validate(dtime, RString.datetimeToStandard(None))
        timeValue = ValToRemember(timeValue)
        dtime = Remember(dtime)
        dtimeVal = lambda: RString.toDatetime(dtime.value())
        fixItem = lambda a0: str(0) + a0 if len(a0) < 2 else a0
        boxItems = lambda a0, a1: LambdaList(range(a0, int(a1 + 1)), lambda b0: fixItem(str(b0)))
        maxDays = lambda a0, a1: calendar.monthrange(a0, a1)[1] if isAllValid(a0, a1) else self.Base.MaxDay
        divideDateTime = lambda a0: GTuple(a0.year, a0.month, a0.day, a0.hour, a0.minute, a0.second)
        dtimeParts = list()
        dtimePartValue = lambda idx: fixItem(str(divideDateTime(dtimeVal())[idx]))
        syncParts = Trigger()
        for i in range(self.DateTimeParts):
            dtimePart = LambdaRemember(dtime, syncParts, lambdaExp=lambda *az, idx=i: dtimePartValue(idx))
            dtimeParts.append(dtimePart)
        yearVal, monthVal, dayVal, hourVal, minuteVal, secondVal = dtimeParts
        combineParts = lambda *az: datetime(*LambdaList(az, lambda b0: GInt(Remember.getValue(b0))))
        updateDTime = lambda *az: dtime.setValue(RString.datetimeToStandard(combineParts(*az)))
        isPartsValid = lambda: isAllValid(*LambdaList(dtimeParts, lambda b0: Remember.getValue(b0)))
        onPartActivated = lambda: Run(
            updateDTime(*dtimeParts) if isPartsValid() else None,
            allValidCheck.setValue(isPartsValid()), onAnyActivated()
        ).result
        super().__init__(
            padding=int(0),
            spacing=canvasModifier.itemSpacing,
            verticalPadding=canvasModifier.verticalPadding,
            options=GList(Row.AutoSizeNoRemain),
            fixHeight=True,
            fixWidth=True,
            content=GList(
                Column(
                    padding=int(0),
                    spacing=canvasModifier.labelSpacing,
                    horizontalPadding=canvasModifier.itemPadding,
                    options=GList(Column.AutoSizeNoRemain),
                    content=GList(
                        IndicatorLabel(
                            text=LambdaRemember(language, lambdaExp=lambda a0: RString.stYear[a0]),
                            alignment=IndicatorLabel.Align.Center,
                            size=QSize(canvasModifier.yearEditorWidth, canvasModifier.editorHeight),
                            indicatorStyle=IndicatorLabelStyle(
                                borderRadius=labelBorderRadius,
                                fontSize=labelFontSize,
                                normalBackground=LambdaRemember(
                                    yearVal, lambdaExp=lambda a0:
                                    dateLabelBackground if a0 is not None else invalidBackground
                                )
                            )
                        ),
                        BorderedComboBox(
                            placeholder=RString.pOmit,
                            size=QSize(canvasModifier.yearEditorWidth, canvasModifier.editorHeight),
                            styleEditor=comboBoxStyle,
                            wheelEnable=True,
                            wheelCycle=False,
                            scrollStep=int(8),
                            onSelected=lambda: onPartActivated(),
                            selection=yearVal,
                            dataModel=boxItems(self.Base.MinYear, self.Base.MaxYear),
                        ),
                    )
                ) if editorMode in GList(self.DateTime, self.Date) else None,
                Column(
                    padding=int(0),
                    spacing=canvasModifier.labelSpacing,
                    horizontalPadding=canvasModifier.itemPadding,
                    options=GList(Column.AutoSizeNoRemain),
                    content=GList(
                        IndicatorLabel(
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            alignment=IndicatorLabel.Align.Center,
                            text=LambdaRemember(language, lambdaExp=lambda a0: RString.stMonth[a0]),
                            indicatorStyle=IndicatorLabelStyle(
                                borderRadius=labelBorderRadius,
                                fontSize=labelFontSize,
                                normalBackground=LambdaRemember(
                                    monthVal, lambdaExp=lambda a0:
                                    dateLabelBackground if a0 is not None else invalidBackground
                                )
                            )
                        ),
                        BorderedComboBox(
                            placeholder=RString.pOmit,
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            wheelEnable=True,
                            scrollStep=int(8),
                            styleEditor=comboBoxStyle,
                            onSelected=lambda: onPartActivated(),
                            selection=monthVal,
                            dataModel=boxItems(self.Base.MinMonth, self.Base.MaxMonth),
                        ),
                    )
                ) if editorMode in GList(self.DateTime, self.Date) else None,
                Column(
                    padding=int(0),
                    spacing=canvasModifier.labelSpacing,
                    horizontalPadding=canvasModifier.itemPadding,
                    options=GList(Column.AutoSizeNoRemain),
                    content=GList(
                        IndicatorLabel(
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            text=LambdaRemember(language, lambdaExp=lambda a0: RString.stDay[a0]),
                            alignment=IndicatorLabel.Align.Center,
                            indicatorStyle=IndicatorLabelStyle(
                                borderRadius=labelBorderRadius,
                                fontSize=labelFontSize,
                                normalBackground=LambdaRemember(
                                    dayVal, lambdaExp=lambda a0:
                                    dateLabelBackground if a0 is not None else invalidBackground
                                )
                            )
                        ),
                        BorderedComboBox(
                            placeholder=RString.pOmit,
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            styleEditor=comboBoxStyle,
                            selection=dayVal,
                            wheelEnable=True,
                            onSelected=lambda: onPartActivated(),
                            scrollStep=int(20),
                            dataModel=LambdaRemember(
                                yearVal, monthVal, lambdaExp=lambda a0, a1:
                                boxItems(self.Base.MinDay, maxDays(GInt(a0), GInt(a1)))
                            ),
                        ),
                    )
                ) if editorMode in GList(self.DateTime, self.Date) else None,
                HorizontalSpacer(
                    width=canvasModifier.dateTimeSpacing,
                ) if editorMode in GList(self.DateTime) else None,
                Column(
                    padding=int(0),
                    spacing=canvasModifier.labelSpacing,
                    horizontalPadding=canvasModifier.itemPadding,
                    options=GList(Column.AutoSizeNoRemain),
                    content=GList(
                        IndicatorLabel(
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            alignment=IndicatorLabel.Align.Center,
                            text=LambdaRemember(language, lambdaExp=lambda a0: RString.stHour[a0]),
                            indicatorStyle=IndicatorLabelStyle(
                                borderRadius=labelBorderRadius,
                                fontSize=labelFontSize,
                                normalBackground=LambdaRemember(
                                    hourVal, lambdaExp=lambda a0:
                                    timeLabelBackground if a0 is not None else invalidBackground
                                )
                            )
                        ),
                        BorderedComboBox(
                            placeholder=RString.pOmit,
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            styleEditor=comboBoxStyle,
                            selection=hourVal,
                            wheelEnable=True,
                            onSelected=lambda: onPartActivated(),
                            scrollStep=int(18),
                            dataModel=boxItems(self.Base.MinHour, self.Base.MaxHour),
                        ),
                    )
                ) if editorMode in GList(self.DateTime, self.Time) else None,
                Column(
                    padding=int(0),
                    spacing=canvasModifier.labelSpacing,
                    horizontalPadding=canvasModifier.itemPadding,
                    options=GList(Column.AutoSizeNoRemain),
                    content=GList(
                        IndicatorLabel(
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            alignment=IndicatorLabel.Align.Center,
                            text=LambdaRemember(language, lambdaExp=lambda a0: RString.stMinute[a0]),
                            indicatorStyle=IndicatorLabelStyle(
                                borderRadius=labelBorderRadius,
                                fontSize=labelFontSize,
                                normalBackground=LambdaRemember(
                                    minuteVal, lambdaExp=lambda a0:
                                    timeLabelBackground if a0 is not None else invalidBackground
                                )
                            )
                        ),
                        BorderedComboBox(
                            placeholder=RString.pOmit,
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            styleEditor=comboBoxStyle,
                            onSelected=lambda: onPartActivated(),
                            wheelEnable=True,
                            selection=minuteVal,
                            scrollStep=int(22),
                            dataModel=boxItems(self.Base.MinMinute, self.Base.MaxMinute),
                        ),
                    )
                ) if editorMode in GList(self.DateTime, self.Time) else None,
                Column(
                    padding=int(0),
                    spacing=canvasModifier.labelSpacing,
                    horizontalPadding=canvasModifier.itemPadding,
                    options=GList(Column.AutoSizeNoRemain),
                    content=GList(
                        IndicatorLabel(
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            alignment=IndicatorLabel.Align.Center,
                            text=LambdaRemember(language, lambdaExp=lambda a0: RString.stSecond[a0]),
                            indicatorStyle=IndicatorLabelStyle(
                                borderRadius=labelBorderRadius,
                                fontSize=labelFontSize,
                                normalBackground=LambdaRemember(
                                    secondVal, lambdaExp=lambda a0:
                                    timeLabelBackground if a0 is not None else invalidBackground
                                ),
                            )
                        ),
                        BorderedComboBox(
                            placeholder=RString.pOmit,
                            size=QSize(canvasModifier.baseWidth, canvasModifier.editorHeight),
                            wheelEnable=True,
                            styleEditor=comboBoxStyle,
                            onSelected=lambda: onPartActivated(),
                            selection=secondVal,
                            scrollStep=int(34),
                            dataModel=boxItems(self.Base.MinSecond, self.Base.MaxSecond),
                        ),
                    )
                ) if editorMode in GList(self.DateTime, self.Time) else None,
            )
        )
        dtime.connect(lambda value: timeValue.setValue(self.FixMethodMap[editorMode](value)), host=self)
        syncMethod = lambda a0, a1: self.updateDateTime(RString.toDatetime(a0), RString.toDatetime(a1), editorMode)
        isTimeEqual = lambda a0, a1: self.isDateTimeEqual(RString.toDatetime(a0), RString.toDatetime(a1), editorMode)
        syncDTime = lambda a0: dtime.setValue(RString.datetimeToStandard(syncMethod(dtime.value(), a0)))
        onTimeValueChange = lambda a0: syncDTime(a0) if not isTimeEqual(dtime.value(), a0) else syncParts.trig()
        timeValue.connect(lambda value: onTimeValueChange(value) if isValid(value) else None, host=self)

    @staticmethod
    def sizeMetric(
            editorMode: EditorMode = None,
            withinGraphic: bool = True,
            sidePadding: bool = False,
            canvasModifier: TimeEditorCanvas = None
    ) -> QSize:
        cvm = Validate(canvasModifier, TimeEditorCanvas())
        dateWidth = int(cvm.baseWidth * 2.0 + cvm.yearEditorWidth + cvm.itemSpacing * 2.0 + cvm.itemPadding * 6.0)
        timeWidth = int(cvm.baseWidth * 3.0 + cvm.itemSpacing * 2.0 + cvm.itemPadding * 6.0)
        dateTimeWidth = dateWidth + timeWidth + cvm.dateTimeSpacing + int(2.0 * cvm.itemSpacing)
        height = int(cvm.editorHeight * 2.0 + cvm.labelSpacing)
        if not withinGraphic:
            height += int(cvm.verticalPadding * 2.0)
        else:
            ratio = 1.0 if sidePadding else 2.0
            dateWidth += -int(cvm.itemPadding * ratio)
            timeWidth += -int(cvm.itemPadding * ratio)
            dateTimeWidth += -int(cvm.itemPadding * ratio)
        if editorMode in GList(TimeEditor.Date):
            return QSize(dateWidth, height)
        elif editorMode in GList(TimeEditor.Time):
            return QSize(timeWidth, height)
        return QSize(dateTimeWidth, height)

    @staticmethod
    def isDateTimeEqual(dtime: datetime, source: datetime, mode: EditorMode) -> bool:
        if source is None or dtime is None:
            return False
        yearEqual = Equal(dtime.year, source.year)
        monthEqual = Equal(dtime.month, source.month)
        dayEqual = Equal(dtime.day, source.day)
        hourEqual = Equal(dtime.hour, source.hour)
        minuteEqual = Equal(dtime.minute, source.minute)
        secondEqual = Equal(dtime.second, source.second)
        dateEqual = yearEqual and monthEqual and dayEqual
        timeEqual = hourEqual and minuteEqual and secondEqual
        if Equal(mode, TimeEditor.Date):
            return dateEqual
        elif Equal(mode, TimeEditor.Time):
            return timeEqual
        return dateEqual and timeEqual

    @staticmethod
    def updateDateTime(dtime: datetime, source: datetime, mode: EditorMode) -> datetime:
        if source is None:
            return dtime
        if Equal(mode, TimeEditor.Date):
            return dtime.replace(year=source.year, month=source.month, day=source.day)
        elif Equal(mode, TimeEditor.Time):
            return dtime.replace(hour=source.hour, minute=source.minute, second=source.second)
        return DataBox(dtime.replace(
            year=source.year, month=source.month, day=source.day,
            hour=source.hour, minute=source.minute, second=source.second
        )).data

    DefaultComboBoxStyle = DataBox(ComboBoxStyle(
        borderRadius=int(3),
        borderColor=RColor.hexLightGrey,
        upArrowIcon=RIcon.loadIconPath(RIcon.Src.arrow_drop_up_light),
        downArrowIcon=RIcon.loadIconPath(RIcon.Src.arrow_drop_down_light)
    )).data
    FixMethodMap = DictData(
        Key(Date).Val(RString.dateToStandard),
        Key(Time).Val(RString.timeToStandard),
        Key(DateTime).Val(RString.datetimeToStandard),
    ).data
