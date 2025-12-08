from PyQt5.QtCore import QSizeF, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QDialog

from DeclarativeQt.DqtCore.DqtBase import Remember, Trigger, ReferState, RState
from DeclarativeQt.DqtCore.DqtDevice.DqtKeyboard import DqtKeyboard
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.ComboBoxes.ComboBoxGroups.TimeEditor import TimeEditor
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Labels.IconLabel import IconLabel, LabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabel, IndicatorLabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import VerticalSpacer
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog, Column, Row
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate, DataBox, GList, GStr
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex


def DateTimeEditDialog(
        timeVal: RState[str] = None,
        editMode: str = None,
        language: RState[NLIndex] = None,
        baseSpacing: int = int(14),
        editorLabelSpacing: int = int(3),
        editorItemSpacing: int = int(5),
        editorBaseHeight: int = int(30),
        headLabelWidth: int = int(60),
        headLabelSpacing: int = int(10),
        headLabelBackground: str = None,
        headLabelIconSizeRatio: QSizeF = None,
        checkButtonWidth: int = int(300),
        checkButtonHeight: int = int(36),
        infoLabelWidth: int = int(200),
        infoLabelHeight: int = int(30),
        labelFontSize: float = float(9.6),
        borderRadius: int = int(3),
        dialogOffset: QPoint = None,
        dialogTitle: str = None,
        dialogHPadding: int = int(30),
        parent: QWidget = None,
) -> QDialog:
    defautlTimeVal = DictData(
        Key(TimeEditor.Date).Val(lambda: RString.dateToStandard(None)),
        Key(TimeEditor.Time).Val(lambda: RString.timeToStandard(None)),
        Key(TimeEditor.DateTime).Val(lambda: RString.datetimeToStandard(None)),
    ).data
    leadingIcon = DictData(
        Key(TimeEditor.Date).Val(RIcon.loadIconPixmap(RIcon.Src.edit_calendar)),
        Key(TimeEditor.Time).Val(RIcon.loadIconPixmap(RIcon.Src.timer)),
        Key(TimeEditor.DateTime).Val(RIcon.loadIconPixmap(RIcon.Src.timer)),
    ).data
    headLabelBackground = Validate(headLabelBackground, RColor.hexWhite)
    editMode = Validate(editMode, TimeEditor.Date)
    timeEditorSize = DataBox(TimeEditor.sizeMetric(
        editorMode=editMode, canvasModifier=TimeEditor.Canvas(
            itemSpacing=editorItemSpacing, labelSpacing=editorLabelSpacing, editorHeight=editorBaseHeight
        ), withinGraphic=True
    )).data
    headLabelHeight = timeEditorSize.height()
    headLabelIconSizeRatio = Validate(headLabelIconSizeRatio, QSizeF(0.48, 0.48))
    dividerLength = timeEditorSize.width() + headLabelWidth + headLabelSpacing
    language = Remember.toValid(language, RString.EnglishIndex)
    allValid = Remember(True)
    timeVal = ValToRemember(timeVal)
    timeVal = Remember.toValid(timeVal, defautlTimeVal[editMode]())
    acceptor = Trigger()
    return Dialog(
        parent=parent,
        offset=dialogOffset,
        title=dialogTitle,
        acceptTrig=acceptor,
        style=DqtStyle.widgetLightStyle(RColor.hexLightWhite),
        content=Column(
            padding=int(28),
            spacing=baseSpacing,
            horizontalPadding=dialogHPadding,
            options=GList(Column.AutoSizeNoRemain),
            alignment=Column.Align.HCenter,
            content=GList(
                Column(
                    padding=int(0),
                    spacing=baseSpacing,
                    horizontalPadding=int(0),
                    options=GList(Column.AutoSizeNoRemain),
                    alignment=Column.Align.Left,
                    content=GList(
                        HorizontalDivider(length=dividerLength),
                        Row(
                            padding=int(0),
                            spacing=headLabelSpacing,
                            options=GList(Row.AutoSizeNoRemain),
                            content=GList(
                                IconLabel(
                                    alignment=IconLabel.Align.Center,
                                    size=QSize(headLabelWidth, headLabelHeight),
                                    iconPixmap=leadingIcon[editMode],
                                    iconSizeRatio=headLabelIconSizeRatio,
                                    styleEditor=LabelStyle(
                                        backgroundColor=headLabelBackground,
                                        borderRadius=borderRadius,
                                        borderWidth=int(1),
                                        borderColor=RColor.hexGrey
                                    ),
                                ),
                                TimeEditor(
                                    editorMode=editMode,
                                    language=language,
                                    canvasModifier=TimeEditor.Canvas(
                                        editorHeight=editorBaseHeight,
                                        labelSpacing=editorLabelSpacing,
                                        itemSpacing=editorItemSpacing,
                                    ),
                                    labelBorderRadius=borderRadius,
                                    timeValue=timeVal,
                                    allValidCheck=allValid,
                                ),
                            ),
                        ),
                        HorizontalDivider(length=dividerLength),
                        IndicatorLabel(
                            size=QSize(infoLabelWidth, infoLabelHeight),
                            fixedHeight=infoLabelHeight,
                            indicatorStyle=IndicatorLabelStyle(fontSize=labelFontSize),
                            text=ReferState(timeVal, referExp=lambda a0: GStr(
                                RString.pAt + RString.blankRepeat(int(3)) + GStr(a0)
                            )),
                        ),
                    )
                ),
                VerticalSpacer(height=int(1)),
                IconButton(
                    fixedHeight=checkButtonHeight,
                    size=QSize(checkButtonWidth, checkButtonHeight),
                    icon=RIcon.loadIconPixmap(RIcon.Src.check),
                    text=ReferState(language, referExp=lambda a0: RString.stOkConfirm[a0]),
                    styleEditor=ButtonStyle(
                        borderRadius=borderRadius,
                        fontSize=RFont.fzTinySize,
                    ),
                    shortCuts=DqtKeyboard().keyEnterReturn,
                    onClick=lambda: acceptor.trig() if allValid.value() else None
                ), VerticalSpacer(height=int(8)),
            )
        )
    )
