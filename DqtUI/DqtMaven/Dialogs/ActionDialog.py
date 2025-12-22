from typing import Callable

from PyQt5.QtCore import QSize, QSizeF, QPoint
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, Trigger, Run, RState, ReferState
from DeclarativeQt.DqtCore.DqtDevice.DqtKeyboard import DqtKeyboard
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import Execute, ValToState
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.ComboBoxes.ComboBoxGroups.TimeEditor import TimeEditor
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Labels.IconLabel import IconLabel, LabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabelStyle, IndicatorLabel
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import VerticalSpacer
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BorderedTextField import BorderedTextField, \
    TextFieldStyle
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog, Box, Column, Row
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, Equal, GList, GStr, DataBox, Key, DictData
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex


class ActionDialog:
    DefaultDialogSize: QSize = QSize(400, 240)
    DefaultEditorSize: QSize = QSize(240, 34)
    DefaultEditorStyle = TextFieldStyle(fontSize=9.8, fontFamily=RFont.YaHei, focusedBackground=RColor.hexWhite)

    @staticmethod
    def getTextInput(
            parent: QWidget = None,
            dialogTitle: RState[str] = None,
            dialogOffset: QPoint = None,
            dialogVPadding: int = int(30),
            dialogHPadding: int = int(20),
            editorSize: QSize = None,
            editorStyle: TextFieldStyle = None,
            editorSpacing: int = int(4),
            restoreButtonWidth: int = int(30),
            buttonSpacing: int = int(20),
            initial: str = None,
            restore: str = None,
            checkMethod: Callable = None,
            borderRadiusRatio: float = 0.08,
    ) -> str:
        initial = Validate(initial, RString.pEmpty)
        editorStyle = Validate(editorStyle, ActionDialog.DefaultEditorStyle)
        editorSize = Validate(editorSize, ActionDialog.DefaultEditorSize)
        confirmButtonWidth = editorSize.width() + editorSpacing + restoreButtonWidth
        text = Remember[str](initial)
        checkMethod = Validate(checkMethod, lambda a0: True)
        acceptor = Trigger()
        if Equal(Execute(Dialog(
                parent=parent,
                title=dialogTitle,
                offset=dialogOffset,
                fixWidth=True,
                acceptTrig=acceptor,
                style=DqtStyle.widgetLightStyle(RColor.hexLightWhite),
                content=Box(
                    content=Column(
                        arrangement=Column.Align.Top,
                        padding=dialogVPadding,
                        horizontalPadding=dialogHPadding,
                        spacing=buttonSpacing,
                        content=GList(
                            Row(
                                padding=int(0),
                                spacing=editorSpacing,
                                options=GList(Row.AutoSizeNoRemain),
                                content=GList(
                                    BorderedTextField(
                                        styleEditor=editorStyle,
                                        size=editorSize,
                                        fixedRadiusRatio=borderRadiusRatio,
                                        text=text,
                                    ),
                                    IconButton(
                                        size=QSize(restoreButtonWidth, editorSize.height()),
                                        fixedRadiusRatio=borderRadiusRatio,
                                        iconSizeRatio=QSizeF(0.8, 0.8),
                                        icon=RIcon().loadIconPixmap(RIcon.Src.history),
                                        onClick=lambda: Run(
                                            text.setValue(restore) if restore else None
                                        )
                                    )
                                )
                            ),
                            IconButton(
                                size=QSize(confirmButtonWidth, editorSize.height()),
                                fixedRadiusRatio=borderRadiusRatio,
                                iconSizeRatio=QSizeF(0.76, 0.76),
                                icon=RIcon().loadIconPixmap(RIcon.Src.edit_square_darkblue),
                                styleEditor=ButtonStyle(
                                    backgroundColor=RColor.setQStyleAlpha(RColor.hexForestGreen, 0.34),
                                    hoverBackground=RColor.setQStyleAlpha(RColor.hexTealGreen, 0.20),
                                    pressedBackground=RColor.setQStyleAlpha(RColor.hexTealGreen, 0.62),
                                    borderColor=RColor.hexDarkGrey,
                                ),
                                shortCuts=DqtKeyboard.multiShortCuts(
                                    DqtKeyboard.keyEnter, DqtKeyboard.keyReturn
                                ),
                                onClick=lambda: acceptor.trig() if checkMethod(text) else None,
                            )
                        )
                    )
                )
        )), Dialog.Accepted):
            return text.value()
        return GStr(initial)

    @staticmethod
    def getDateTimeInput(
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
    ) -> str:
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
        timeVal = ValToState(timeVal)
        timeVal = Remember.toValid(timeVal, defautlTimeVal[editMode]())
        originVal = timeVal.value()
        acceptor = Trigger()
        if Equal(Execute(Dialog(
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
        )), Dialog.Accepted):
            return timeVal.value()
        timeVal.setValue(originVal)
        return timeVal.value()
