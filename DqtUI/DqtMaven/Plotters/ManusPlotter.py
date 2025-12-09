from typing import Dict, Callable, List, Any

from PyQt5.QtCore import QSize, QSizeF, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QDialog

from DeclarativeQt.DqtCore.DqtBase import Remember, Run, ReferState, Trigger, RState
from DeclarativeQt.DqtCore.DqtDevice.DqtKeyboard import DqtKeyboard
from DeclarativeQt.DqtCore.DqtMethods.DqtMethods import DqtMethods
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember, SeqToRemember, Execute, SemanticRemember
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.Dialogs.MetaDialogs.ColorDialog import ColorDialog
from DeclarativeQt.DqtUI.DqtMaven.Dialogs.MetaDialogs.InputDialog import InputDialog
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabel, IndicatorLabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Layouts.LazyLayout import LazyColumn
from DeclarativeQt.DqtUI.DqtMaven.Plotters.BasePlotter.MultiAxisPlotter import MultiAxisPlotter
from DeclarativeQt.DqtUI.DqtMaven.Plotters.CurvePlotter import CurveData, StringSTox, PlotterStyle, \
    CurvePlotter, BoolSTox, PlotterTrigger
from DeclarativeQt.DqtUI.DqtMaven.Plotters.PlotterAssistant.ExportFigureDialog import ExportOptionArg
from DeclarativeQt.DqtUI.DqtMaven.Plotters.PlotterAssistant.FixCircleShapeDialog import FixCircleShapeDialog
from DeclarativeQt.DqtUI.DqtMaven.Sliders.ColoredSlider import ColoredSlider, SliderStyle
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import HorizontalSpacer
from DeclarativeQt.DqtUI.DqtWidgets.Container import Box, Column, Row, Dialog
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, GList, ReferList, JoinLists, DataBox, DictData, Key, \
    SumNestedList, Equal, isValid, isEmpty, GetDictItem, SwitchListItem, ExpValue
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Images.RImage import RImage
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex


class ManusPlotter(Column):
    def __init__(
            self,
            datas: RState[CurveData] = None,
            xLabel: RState[str] = None,
            yLabels: RState[StringSTox] = None,
            aspectMode: RState[str] = None,
            width: float = 6.0,
            height: float = 4.0,
            dpi: int = 100,
            styleEditor: PlotterStyle = None,
            language: RState[NLIndex] = None,
            topToolSpacing: int = int(3),
            toolButtonSpacing: int = int(5),
            markLimit: RState[bool] = True,
            cursorOff: RState[bool] = False,
            gridOn: RState[bool] = True,
            curveVisibles: RState[BoolSTox] = None,
            triggers: Dict[Remember, Callable] = None,
            refreshMethod: Callable = None,
            exportOptions: Dict[str, ExportOptionArg] = None,
            buttonSize: QSize = None,
            buttonRadiusRatio: float = 0.15,
    ):
        buttonSize = Validate(buttonSize, QSize(30, 30))
        datas = Remember.toValid(datas, dict())
        xLabel = Remember.toValid(xLabel, RString.pEmpty)
        yLabels = Remember.toValid(yLabels, list())
        aspectMode = Remember.toValid(aspectMode, CurvePlotter.aspectEqual)
        curveVisibles = Remember.toValid(curveVisibles, list())
        language = Validate(language, RString.EnglishIndex)
        self._datas = ValToRemember(datas)
        self._xLabel = ValToRemember(xLabel)
        self._yLabels = SeqToRemember(yLabels)
        self._aspectMode = ValToRemember(aspectMode)
        self._curveNames = SeqToRemember(list(Remember.getDictValue(datas).keys()))
        self._styleEditor: PlotterStyle = Validate(styleEditor, PlotterStyle())
        self._styleEditor.lineColors = SeqToRemember(self._styleEditor.lineColors)
        self._styleEditor.annotationColors = SeqToRemember(self._styleEditor.annotationColors)
        self._styleEditor.lineStyles = SeqToRemember(self._styleEditor.lineStyles)
        self._styleEditor.lineWidths = SeqToRemember(self._styleEditor.lineWidths)
        self._styleEditor.pinnerStyles = SeqToRemember(self._styleEditor.pinnerStyles)
        self._styleEditor.pinnerSizes = SeqToRemember(self._styleEditor.pinnerSizes)
        self._styleEditor.cursorColor = ValToRemember(self._styleEditor.cursorColor)
        self._styleEditor.annotationFrame = ValToRemember(self._styleEditor.annotationFrame)
        self._curveVisibles = SeqToRemember(curveVisibles)
        self._cursorOff = ValToRemember(cursorOff)
        self._gridOn = ValToRemember(gridOn)
        self._homeTrigger = Trigger()
        self._clearLastMarkTrigger = Trigger()
        self._clearAllMarkTrigger = Trigger()
        self._circleMarkFixTrigger = Trigger()
        self._exportTrigger = Trigger()
        self._flushTrigger = Trigger()
        self._moveLegendTrigger = Trigger()
        self._expandXLimTrigger = Trigger()
        self._expandYLimTrigger = Trigger()
        self._shrinkXLimTrigger = Trigger()
        self._shrinkYLimTrigger = Trigger()
        self.fixCurvesElements()
        super().__init__(
            options=GList(Column.AutoSizeNoRemain),
            padding=int(0),
            horizontalPadding=int(0),
            spacing=topToolSpacing,
            autoExpandContentAt=int(1),
            autoExpandToMaxCross=GList(0),
            autoContentResize=True,
            alignment=Row.Align.Left,
            content=GList(
                Row(
                    options=GList(Row.AutoSizeNoRemain),
                    autoUniformDistribute=True,
                    padding=int(0),
                    fixHeight=True,
                    verticalPadding=int(0),
                    content=GList(
                        Row(
                            options=GList(Row.AutoSizeNoRemain),
                            autoContentResize=True,
                            arrangement=Row.Align.Left,
                            fixHeight=True,
                            fixWidth=True,
                            padding=int(0),
                            verticalPadding=int(0),
                            spacing=toolButtonSpacing,
                            content=GList(
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.refresh),
                                    onClick=lambda: Run(
                                        self._flushTrigger.trig(),
                                    ) if refreshMethod is None else refreshMethod()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.home_dark),
                                    onClick=lambda: self._homeTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=ReferState(
                                        self._aspectMode, referExp=lambda a0:
                                        RIcon().loadIconPixmap(RIcon.Src.open_in_full)
                                        if Equal(a0, CurvePlotter.aspectEqual) else
                                        RIcon().loadIconPixmap(RIcon.Src.aspect_ratio)
                                    ),
                                    onClick=lambda: Run(
                                        self._aspectMode.setValue(CurvePlotter.aspectAuto)
                                        if Equal(self._aspectMode.value(), CurvePlotter.aspectEqual) else
                                        self._aspectMode.setValue(CurvePlotter.aspectEqual)
                                    )
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.curve_colored),
                                    onClick=lambda a0: Execute(
                                        self.CurveEditorDailog(
                                            parent=a0,
                                            curveNames=self._curveNames,
                                            curveLabels=self._yLabels,
                                            lineColors=self._styleEditor.lineColors,
                                            lineStyles=self._styleEditor.lineStyles,
                                            lineWidths=self._styleEditor.lineWidths,
                                            pinnerSizes=self._styleEditor.pinnerSizes,
                                            pinnerStyles=self._styleEditor.pinnerStyles,
                                            curveVisibles=self._curveVisibles,
                                            annotColors=self._styleEditor.annotationColors,
                                            buttonRadiusRatio=buttonRadiusRatio,
                                            dialogOffset=QPoint(a0.width(), -1),
                                        ) if not isEmpty(Remember.getValue(self._datas)) else None
                                    ),
                                    triggers=DictData(Key(self._datas).Val(
                                        lambda a0: self._curveNames.setValue(SeqToRemember(
                                            list(Remember.getDictValue(self._datas).keys())
                                        )) if isValid(a0) else None
                                    )).data
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=ReferState(
                                        self._gridOn, referExp=lambda a0:
                                        RIcon().loadIconPixmap(RIcon.Src.calendar_view_month)
                                        if a0 else RIcon().loadIconPixmap(RIcon.Src.calendar_view_month_grey)
                                    ),
                                    onClick=lambda: self._gridOn.setValue(not self._gridOn.value())
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=ReferState(
                                        self._cursorOff, referExp=lambda a0:
                                        RIcon().loadIconPixmap(RIcon.Src.cursor_on) if not a0 else
                                        RIcon().loadIconPixmap(RIcon.Src.border_inner_grey)
                                    ),
                                    onClick=lambda: self._cursorOff.setValue(not self._cursorOff.value())
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.border_color),
                                    onClick=lambda a0: Run(
                                        self._styleEditor.cursorColor.setValue(
                                            RColor.qColorToHexCode(ColorDialog.getColor(
                                                initial=self._styleEditor.cursorColor.value(),
                                                parent=a0, offset=QPoint(a0.width(), -1),
                                                title=SemanticRemember(language, RString.stCursorColor)
                                            )),
                                        )
                                    )
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.mouse_cursor_colored),
                                    onClick=lambda a0: Execute(FixCircleShapeDialog(
                                        drivePlotter=ExpValue(DqtMethods.findTypedChildContents(
                                            DqtMethods.backtrackTypedParent(a0, Column),
                                            MultiAxisPlotter, CurvePlotter, strict=True
                                        ), lambda b0: b0[0]), language=language,
                                        parent=a0, dialogOffset=QPoint(a0.width(), -1),
                                    )),
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.ink_eraser),
                                    onClick=lambda: self._clearLastMarkTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.delete_sweep),
                                    onClick=lambda: self._clearAllMarkTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.cycle),
                                    onClick=lambda: self._moveLegendTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.output),
                                    onClick=lambda: self._exportTrigger.trig()
                                ),
                            )
                        ),
                        Row(
                            options=GList(Row.AutoSizeNoRemain),
                            autoContentResize=True,
                            arrangement=Row.Align.Left,
                            fixHeight=True,
                            fixWidth=True,
                            padding=int(0),
                            verticalPadding=int(0),
                            spacing=toolButtonSpacing,
                            content=GList(
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.expand_x),
                                    enable=ReferState(self._aspectMode, referExp=lambda a0: Equal(
                                        a0, MultiAxisPlotter.aspectAuto
                                    )),
                                    onClick=lambda: self._expandXLimTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.compress_x),
                                    enable=ReferState(self._aspectMode, referExp=lambda a0: Equal(
                                        a0, MultiAxisPlotter.aspectAuto
                                    )),
                                    onClick=lambda: self._shrinkXLimTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.expand_y),
                                    enable=ReferState(self._aspectMode, referExp=lambda a0: Equal(
                                        a0, MultiAxisPlotter.aspectAuto
                                    )),
                                    onClick=lambda: self._expandYLimTrigger.trig()
                                ),
                                IconButton(
                                    size=buttonSize,
                                    fixedRadiusRatio=buttonRadiusRatio,
                                    icon=RIcon().loadIconPixmap(RIcon.Src.compress_y),
                                    enable=ReferState(self._aspectMode, referExp=lambda a0: Equal(
                                        a0, MultiAxisPlotter.aspectAuto
                                    )),
                                    onClick=lambda: self._shrinkYLimTrigger.trig()
                                ),
                            )
                        )
                    )
                ),
                CurvePlotter(
                    datas=self._datas,
                    xLabel=self._xLabel,
                    yLabels=self._yLabels,
                    aspectMode=self._aspectMode,
                    width=width,
                    height=height,
                    dpi=dpi,
                    curveVisibles=self._curveVisibles,
                    markLimit=markLimit,
                    language=language,
                    exportOptions=exportOptions,
                    cursorOff=self._cursorOff,
                    gridOn=self._gridOn,
                    plotterTrigs=PlotterTrigger(
                        homeTrig=self._homeTrigger,
                        canvasFlushTrig=self._flushTrigger,
                        exportFigureTrig=self._exportTrigger,
                        adjustLegendTrig=self._moveLegendTrigger,
                        clearAllMarkTrig=self._clearAllMarkTrigger,
                        clearLastMarkTrig=self._clearLastMarkTrigger,
                        circleMarkFixTrig=self._circleMarkFixTrigger,
                        shrinkXLimTrig=self._shrinkXLimTrigger,
                        shrinkYLimTrig=self._shrinkYLimTrigger,
                        expandXLimTrig=self._expandXLimTrigger,
                        expandYLimTrig=self._expandYLimTrigger,
                    ),
                    triggers=triggers,
                    styleEditor=self._styleEditor,
                ),
            ),
        )
        self._curveNames.connect(self.fixCurvesElements, host=self)

    @private
    def fixCurvesElements(self):
        self._yLabels.setValue(SeqToRemember(Remember.getListValue(self._curveNames).copy()))
        self.fixCurveArgs(self._styleEditor.lineColors, lambda i, a0=None: Remember(RColor().randomColor()))
        fixAnnotColor = lambda i, a0: self._styleEditor.lineColors.value()[len(a0):][i].copy()
        self.fixCurveArgs(self._styleEditor.annotationColors, fixAnnotColor)
        self.fixCurveArgs(self._styleEditor.lineWidths, lambda i, a0=None: CurvePlotter.defaultLineWidth)
        self.fixCurveArgs(self._styleEditor.lineStyles, lambda i, a0=None: CurvePlotter.defaultCurveStyle)
        self.fixCurveArgs(self._styleEditor.pinnerStyles, lambda i, a0=None: CurvePlotter.defaultPinnerStyle)
        self.fixCurveArgs(self._styleEditor.pinnerSizes, lambda i, a0=None: CurvePlotter.defaultPinnerSize)
        fixVisible = lambda i, a0=None: Remember(True if i < MultiAxisPlotter.oncePlotLimit else False)
        self.fixCurveArgs(self._curveVisibles, fixVisible)
        return None

    @private
    def fixCurveArgs(
            self, tar: Remember[List[RState]],
            method: Callable[[int, List], Any],
    ) -> None:
        argsVal = Remember.getValue(tar)
        n = len(self._curveNames.value())
        dif = n - len(argsVal)
        if dif <= 0:
            tar.setValue(argsVal[:n])
            return None
        fixer = ReferList(range(dif), lambda i, a0=argsVal: method(i, a0))
        tar.setValue(JoinLists(argsVal, fixer))
        return None

    @staticmethod
    def CurveEditorDailog(
            curveNames: Remember[List[Remember[str]]],
            curveLabels: Remember[List[Remember[str]]],
            lineColors: Remember[List[Remember[str]]],
            annotColors: Remember[List[Remember[str]]],
            lineWidths: Remember[List[Remember[float]]],
            lineStyles: Remember[List[Remember[str]]],
            pinnerStyles: Remember[List[Remember[str]]],
            pinnerSizes: Remember[List[Remember[float]]],
            curveVisibles: Remember[List[Remember[bool]]],
            dialogOffset: QPoint = None,
            language: RState[NLIndex] = None,
            dialogTitle: str = None,
            dialogWidth: int = int(540),
            contentPadding: int = int(100),
            initialDialogHeight: int = int(680),
            editAreaHeight: int = int(540),
            curveCardHeight: int = int(32),
            confirmButtonHeight: int = int(40),
            parent: QWidget = None,
            buttonRadiusRatio: float = 0.15,
    ) -> QDialog:
        dialogCloser = Trigger()
        contentWidth = int(dialogWidth - contentPadding)
        return Dialog(
            fixedWidth=dialogWidth,
            offset=dialogOffset,
            style=DqtStyle(
                appendix=DictData(
                    Key(DqtStyle.atBackgroundColor).Val(RColor.hexLightWhite)
                ).data,
                selector=DqtStyle.QWidget
            ).style,
            size=QSize(dialogWidth, initialDialogHeight),
            parent=parent,
            title=dialogTitle,
            closeTrig=dialogCloser,
            content=Box(
                autoContentResize=True,
                content=Column(
                    padding=int(10),
                    spacing=int(30),
                    autoContentResize=True,
                    arrangement=Column.Align.Top,
                    content=GList(
                        LazyColumn(
                            style=DqtStyle(
                                appendix=DictData(
                                    Key(DqtStyle.atBackgroundColor).Val(RColor.hexLightWhite)
                                ).data,
                                selector=DqtStyle.QWidget
                            ).style,
                            scrollAreaHeight=editAreaHeight,
                            padding=int(20),
                            spacing=int(14),
                            autoContentResize=True,
                            arrangement=Column.Align.Top,
                            content=SumNestedList(
                                ReferList(
                                    range(len(curveLabels.value())), lambda i: GList(
                                        ManusPlotter.CurveArgDisplayCard(
                                            cardWidth=contentWidth,
                                            cardHeight=curveCardHeight,
                                            language=language,
                                            curveName=Remember.getValue(curveNames)[i],
                                            curveLabel=Remember.getValue(curveLabels)[i],
                                            curveColor=Remember.getValue(lineColors)[i],
                                            curveStyle=Remember.getValue(lineStyles)[i],
                                            curveWidth=Remember.getValue(lineWidths)[i],
                                            pinnerSize=Remember.getValue(pinnerSizes)[i],
                                            pinnerStyle=Remember.getValue(pinnerStyles)[i],
                                            curveVisible=Remember.getValue(curveVisibles)[i],
                                            annotColor=Remember.getValue(annotColors)[i],
                                            buttonRadiusRatio=buttonRadiusRatio,
                                        ),
                                        HorizontalDivider(
                                            length=contentWidth,
                                            color=RColor.hexLightGrey
                                        )
                                    )
                                )
                            )
                        ),
                        IconButton(
                            size=QSize(int(contentWidth / 1.4), confirmButtonHeight),
                            fixedHeight=confirmButtonHeight,
                            onClick=lambda: dialogCloser.trig(),
                            fixedRadiusRatio=buttonRadiusRatio,
                            icon=RIcon().loadIconPixmap(RIcon.Src.task_alt),
                            shortCuts=DqtKeyboard.multiShortCuts(DqtKeyboard.keyEnter, DqtKeyboard.keyReturn)
                        )
                    )
                )
            )
        )

    @staticmethod
    def CurveArgDisplayCard(
            curveName: Remember[str],
            curveLabel: Remember[str],
            curveColor: Remember[str],
            curveWidth: Remember[float],
            curveStyle: Remember[str],
            pinnerStyle: Remember[str],
            pinnerSize: Remember[float],
            curveVisible: Remember[bool],
            annotColor: Remember[str],
            language: RState[NLIndex] = None,
            cardHeight: int = int(30),
            cardWidth: int = int(560),
            buttonSpacing: int = int(5),
            labelSpacing: int = int(14),
            itemSpacing: int = int(1),
            visibleGap: int = int(15),
            colorButtonWidthRatio: float = 1.4,
            nameEditButtonSizeRatio: float = 0.8,
            buttonRadiusRatio: float = 0.15
    ) -> QWidget:
        language = Validate(language, RString.EnglishIndex)
        buttonWidth = cardHeight
        colorButtonWidth = int(colorButtonWidthRatio * buttonWidth)
        nameButtonWidth = int(nameEditButtonSizeRatio * buttonWidth)
        nameButtonHeight = nameButtonWidth
        visibleSpacerWidth = visibleGap - int(2.0 * buttonSpacing)
        buttonGroupWidth = int(buttonWidth * 3.0 + colorButtonWidth + buttonSpacing * 4.0 + visibleSpacerWidth)
        leadingWidth = cardWidth - buttonGroupWidth - itemSpacing
        labelWidth = leadingWidth - nameButtonWidth - labelSpacing
        return Row(
            autoContentResize=True,
            autoUniformDistribute=True,
            padding=int(0),
            spacing=itemSpacing,
            alignment=Row.Align.VCenter,
            options=GList(Row.AutoSizeNoRemain),
            content=GList(
                Row(
                    autoContentResize=True,
                    padding=int(0),
                    spacing=labelSpacing,
                    options=GList(Row.AutoSizeNoRemain),
                    content=GList(
                        IconButton(
                            iconSizeRatio=QSizeF(0.7, 0.7),
                            size=QSize(nameButtonWidth, nameButtonHeight),
                            fixedRadiusRatio=buttonRadiusRatio,
                            icon=RIcon().loadIconPixmap(RIcon.Src.edit_note),
                            onClick=lambda a0: Run(
                                curveLabel.setValue(InputDialog.TextInputDialog(
                                    initial=curveLabel.value(), restore=curveName.value(),
                                    parent=a0, dialogOffset=QPoint(
                                        a0.width(), -int(float(cardHeight - nameButtonHeight) / 2.0 + 1)
                                    )
                                ))
                            )
                        ),
                        IndicatorLabel(
                            size=QSize(labelWidth, cardHeight),
                            alignment=IndicatorLabel.Align.Left | IndicatorLabel.Align.VCenter,
                            text=curveLabel,
                            indicatorStyle=IndicatorLabelStyle(
                                fontSize=9.4,
                                fontFamily=RFont.YaHei,
                            ),
                        ),
                    )
                ),
                Row(
                    autoContentResize=True,
                    spacing=buttonSpacing,
                    padding=int(0),
                    options=GList(Row.AutoSizeNoRemain),
                    content=GList(
                        IconButton(
                            size=QSize(buttonWidth, cardHeight),
                            iconSizeRatio=QSizeF(0.7, 0.7),
                            fixedRadiusRatio=buttonRadiusRatio,
                            icon=RIcon().loadIconPixmap(RIcon.Src.package_random),
                            onClick=lambda: Run(
                                curveColor.setValue(RColor().randomColor())
                            )
                        ),
                        IconButton(
                            size=QSize(colorButtonWidth, cardHeight),
                            iconSizeRatio=QSizeF(0.4, 0.4),
                            fixedRadiusRatio=buttonRadiusRatio,
                            icon=ReferState(curveColor, referExp=lambda a0: RImage.createQPixmp(a0)),
                            onClick=lambda a0: curveColor.setValue(
                                RColor.qColorToHexCode(ColorDialog.getColor(
                                    initial=Remember.getValue(curveColor),
                                    parent=a0, offset=QPoint(a0.width(), -1),
                                    title=SemanticRemember(language, RString.stCurveColor),
                                )),
                            ),
                            triggers=DictData(
                                Key(curveColor).Val(lambda: annotColor.setValue(curveColor))
                            ).data
                        ),
                        IconButton(
                            size=QSize(buttonWidth, cardHeight),
                            iconSizeRatio=QSizeF(0.7, 0.7),
                            fixedRadiusRatio=buttonRadiusRatio,
                            icon=RIcon().loadIconPixmap(RIcon.Src.format_paint),
                            onClick=lambda a0: Execute(ManusPlotter.CurveStyleArgEditor(
                                parent=a0,
                                dialogOffset=QPoint(a0.width(), -1),
                                language=language,
                                curveLabel=curveLabel,
                                lineWidth=curveWidth,
                                lineStyle=curveStyle,
                                pinnerSize=pinnerSize,
                                pinnerStyle=pinnerStyle,
                            )),
                        ),
                        HorizontalSpacer(width=visibleSpacerWidth),
                        IconButton(
                            size=QSize(buttonWidth, cardHeight),
                            iconSizeRatio=QSizeF(0.7, 0.7),
                            fixedRadiusRatio=buttonRadiusRatio,
                            icon=ReferState(
                                curveVisible, referExp=lambda a0: DataBox(
                                    RIcon().loadIconPixmap(RIcon.Src.visibility_dark)
                                    if a0 else RIcon().loadIconPixmap(RIcon.Src.visibility_off_light)
                                ).data
                            ),
                            onClick=lambda: Run(
                                curveVisible.setValue(not Remember.getValue(curveVisible))
                            ),
                        )
                    )
                )
            )
        )

    @staticmethod
    def CurveStyleArgEditor(
            curveLabel: Remember[str],
            lineWidth: Remember[float],
            lineStyle: Remember[str],
            pinnerStyle: Remember[str],
            pinnerSize: Remember[float],
            parent: QWidget = None,
            dialogOffset: QPoint = None,
            language: RState[NLIndex] = None,
            leadingLabelWidth: int = int(70),
            leadingLabelSpacing: int = int(12),
            leadingLabelFontSize: float = float(9.8),
            sliderLabelWidth: int = int(56),
            sliderPercision: int = int(70),
            sliderLabelFontSize: float = float(9.3),
            sliderValueRound: int = int(2),
            dialogHPadding: int = int(20),
            dialogVPadding: int = int(25),
            editorSpacing: int = int(8),
            editorHeight: int = int(32),
            styleButtonWidth: int = int(44),
            buttonSpacing: int = int(5),
            sliderWidth: int = int(156),
            borderRadius: int = int(3),
    ) -> QDialog:
        language = Validate(language, RString.EnglishIndex)
        sliderModuleWidth = sliderWidth + sliderLabelWidth + buttonSpacing
        editableModuleWidth = sliderModuleWidth + styleButtonWidth + buttonSpacing
        entireWidth = editableModuleWidth + leadingLabelSpacing + leadingLabelWidth
        leadingLabelBackground = RColor.setQStyleAlpha(RColor.hexGrey, 0.24)
        acceptor = Trigger()
        return Dialog(
            title=curveLabel,
            acceptTrig=acceptor,
            fixWidth=True,
            parent=parent,
            offset=dialogOffset,
            style=DqtStyle.widgetLightStyle(RColor.hexLightWhite),
            content=Column(
                padding=dialogVPadding,
                horizontalPadding=dialogHPadding,
                spacing=editorSpacing,
                options=GList(Row.AutoSizeNoRemain),
                content=GList(
                    Row(
                        options=GList(Row.NoPadding),
                        spacing=leadingLabelSpacing,
                        content=GList(
                            IconButton(
                                size=QSize(leadingLabelWidth, editorHeight),
                                fixedHeight=editorHeight,
                                styleEditor=ButtonStyle(
                                    borderRadius=borderRadius,
                                ),
                                icon=RIcon.loadIconPixmap(RIcon.Src.arrow_back),
                                onClick=lambda: acceptor.trig(),
                            ),
                            IndicatorLabel(
                                size=QSize(editableModuleWidth, editorHeight),
                                fixedHeight=editorHeight,
                                text=SemanticRemember(language, RString.stCurveStyle),
                                alignment=IndicatorLabel.Align.Center,
                                indicatorStyle=IndicatorLabelStyle(
                                    borderRadius=borderRadius,
                                    normalBackground=leadingLabelBackground,
                                    fontSize=leadingLabelFontSize,
                                )
                            ),
                        )
                    ),
                    HorizontalDivider(length=entireWidth),
                    Row(
                        options=GList(Row.NoPadding),
                        spacing=leadingLabelSpacing,
                        content=GList(
                            IndicatorLabel(
                                size=QSize(leadingLabelWidth, editorHeight),
                                fixedHeight=editorHeight,
                                text=SemanticRemember(language, RString.stLine),
                                alignment=IndicatorLabel.Align.Center,
                                indicatorStyle=IndicatorLabelStyle(
                                    borderRadius=borderRadius,
                                    normalBackground=leadingLabelBackground,
                                    fontSize=leadingLabelFontSize,
                                )
                            ),
                            Row(
                                options=GList(Row.NoPadding),
                                spacing=buttonSpacing,
                                content=GList(
                                    IconButton(
                                        size=QSize(styleButtonWidth, editorHeight),
                                        fixedHeight=editorHeight,
                                        iconSizeRatio=QSizeF(0.98, 0.98),
                                        icon=ReferState(
                                            lineStyle, referExp=lambda a0:
                                            QPixmap(GetDictItem(ManusPlotter.LineStyleIconMap, a0))
                                        ),
                                        styleEditor=ButtonStyle(borderRadius=borderRadius),
                                        onClick=lambda: lineStyle.updateValue(
                                            lambda a0: SwitchListItem(list(ManusPlotter.LineStyleIconMap.keys()), a0)
                                        )
                                    ),
                                    ColoredSlider(
                                        size=QSize(sliderWidth, editorHeight),
                                        fixedHeight=editorHeight,
                                        minVal=ManusPlotter.MinLineWidth,
                                        maxVal=ManusPlotter.MaxLineWidth,
                                        data=lineWidth,
                                        percision=sliderPercision,
                                        styleEditor=SliderStyle(
                                            borderWidth=int(0),
                                            themeHexColor=RColor.hexSteelBlue,
                                        )
                                    ),
                                    IndicatorLabel(
                                        size=QSize(sliderLabelWidth, editorHeight),
                                        fixedHeight=editorHeight,
                                        text=ReferState(
                                            lineWidth, referExp=
                                            lambda a0: RString.frDecimalRound(sliderValueRound).format(a0)
                                        ),
                                        alignment=IndicatorLabel.Align.Center,
                                        indicatorStyle=IndicatorLabelStyle(
                                            borderRadius=borderRadius,
                                            normalBackground=RColor.setQStyleAlpha(
                                                RColor.hexSteelBlue, 0.14
                                            ),
                                            fontSize=sliderLabelFontSize,
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    Row(
                        options=GList(Row.NoPadding),
                        spacing=leadingLabelSpacing,
                        content=GList(
                            IndicatorLabel(
                                size=QSize(leadingLabelWidth, editorHeight),
                                fixedHeight=editorHeight,
                                text=SemanticRemember(language, RString.stPinner),
                                alignment=IndicatorLabel.Align.Center,
                                indicatorStyle=IndicatorLabelStyle(
                                    borderRadius=borderRadius,
                                    normalBackground=leadingLabelBackground,
                                    fontSize=leadingLabelFontSize,
                                )
                            ),
                            Row(
                                options=GList(Row.NoPadding),
                                spacing=buttonSpacing,
                                content=GList(
                                    IconButton(
                                        size=QSize(styleButtonWidth, editorHeight),
                                        fixedHeight=editorHeight,
                                        icon=ReferState(
                                            pinnerStyle, referExp=lambda a0:
                                            QPixmap(GetDictItem(ManusPlotter.PinnerStyleIconMap, a0))
                                        ),
                                        styleEditor=ButtonStyle(borderRadius=borderRadius),
                                        onClick=lambda: pinnerStyle.updateValue(
                                            lambda a0: SwitchListItem(list(ManusPlotter.PinnerStyleIconMap.keys()), a0)
                                        )
                                    ),
                                    ColoredSlider(
                                        size=QSize(sliderWidth, editorHeight),
                                        fixedHeight=editorHeight,
                                        minVal=ManusPlotter.MinPinnerSize,
                                        maxVal=ManusPlotter.MaxPinnerSize,
                                        data=pinnerSize,
                                        percision=sliderPercision,
                                        styleEditor=SliderStyle(
                                            borderWidth=int(0),
                                            themeHexColor=RColor.hexRoyalBlue,
                                        )
                                    ),
                                    IndicatorLabel(
                                        size=QSize(sliderLabelWidth, editorHeight),
                                        fixedHeight=editorHeight,
                                        text=ReferState(
                                            pinnerSize, referExp=
                                            lambda a0: RString.frDecimalRound(sliderValueRound).format(a0)
                                        ),
                                        alignment=IndicatorLabel.Align.Center,
                                        indicatorStyle=IndicatorLabelStyle(
                                            borderRadius=borderRadius,
                                            fontSize=sliderLabelFontSize,
                                            normalBackground=RColor.setQStyleAlpha(
                                                RColor.hexRoyalBlue, 0.14
                                            ),
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

    MaxLineWidth = 5.2
    MinLineWidth = 0.08
    MaxPinnerSize = 12.0
    MinPinnerSize = 0.0
    PinnerStyleIconMap = DictData(
        Key(CurvePlotter.pinnerStar).Val(RIcon.loadIconPath(RIcon.Src.star)),
        Key(CurvePlotter.pinnerSquare).Val(RIcon.loadIconPath(RIcon.Src.square)),
        Key(CurvePlotter.pinnerCircle).Val(RIcon.loadIconPath(RIcon.Src.circle)),
        Key(CurvePlotter.pinnerDiamond).Val(RIcon.loadIconPath(RIcon.Src.diamond)),
        Key(CurvePlotter.pinnerTriangle).Val(RIcon.loadIconPath(RIcon.Src.triangle)),
        Key(CurvePlotter.pinnerNone).Val(RIcon.loadIconPath(RIcon.Src.block_small)),
    ).data
    LineStyleIconMap = DictData(
        Key(CurvePlotter.lineDash).Val(RIcon.loadIconPath(RIcon.Src.dash_line)),
        Key(CurvePlotter.lineDot).Val(RIcon.loadIconPath(RIcon.Src.dot_line)),
        Key(CurvePlotter.lineDashDot).Val(RIcon.loadIconPath(RIcon.Src.dashdot_line)),
        Key(CurvePlotter.lineSolid).Val(RIcon.loadIconPath(RIcon.Src.solid_line)),
    ).data
