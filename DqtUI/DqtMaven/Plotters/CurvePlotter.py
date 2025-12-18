from functools import partial
from typing import List, Tuple, Dict, Callable, Any

from DeclarativeQt.DqtCore.DqtBase import Remember, RState, Run
from DeclarativeQt.DqtCore.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax import DqtSyntax
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import Execute
from DeclarativeQt.DqtUI.DqtMaven.Plotters.BasePlotter.MultiAxisPlotter import MultiAxisPlotter, \
    AnnotFrame, ModeArg
from DeclarativeQt.DqtUI.DqtMaven.Plotters.PlotterAssistant.ExportFigureDialog import \
    ExportFigureDialog, ExportOptionArg
from DeclarativeQt.DqtUI.DqtMaven.Plotters.PlotterAssistant.FixCircleShapeDialog import \
    FixCircleShapeDialog
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, DictData, Key, DataBox, isValid, \
    ListData, DictToDefault
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex

StyleKey = DqtStyle.StyleKey
StringSTox = DqtSyntax.StringSTox
ColorSTox = DqtSyntax.ColorSTox
FloatSTox = DqtSyntax.FloatSTox
BoolSTox = DqtSyntax.BoolSTox
AxisData = List[Tuple[float, float]]
CurveData = Dict[RState[str], RState[AxisData]]


class PlotterStyle:
    atLineColor: StyleKey = "lineColor"
    atLineWidth: StyleKey = "lineWidth"
    atLineStyle: StyleKey = "lineStyle"
    atPinnerStyle: StyleKey = "pinnerStyle"
    atPinnerSize: StyleKey = "pinnerSize"
    atAnnotationColor: StyleKey = "annotationColor"

    def __init__(
            self,
            style: RState[str] = None,
            lineColors: RState[ColorSTox] = None,
            lineWidths: RState[FloatSTox] = None,
            lineStyles: RState[StringSTox] = None,
            pinnerStyles: RState[StringSTox] = None,
            pinnerSizes: RState[FloatSTox] = None,
            cursorColor: RState[str] = None,
            cursorAlpha: RState[float] = None,
            cursorStyle: RState[str] = None,
            annotationColors: RState[ColorSTox] = None,
            annotationAlpha: RState[float] = None,
            annotationFrame: RState[AnnotFrame] = None,
    ):
        self.style = Remember.toValid(style, RString.pEmpty)
        self.lineColors = Remember.toValid(lineColors, list())
        self.lineWidths = Remember.toValid(lineWidths, list())
        self.lineStyles = Remember.toValid(lineStyles, list())
        self.pinnerStyles = Remember.toValid(pinnerStyles, list())
        self.pinnerSizes = Remember.toValid(pinnerSizes, list())
        self.cursorColor = Remember.toValid(cursorColor, RColor().randomColor())
        self.cursorAlpha = Remember.toValid(cursorAlpha, 1.0)
        self.cursorStyle = Remember.toValid(cursorStyle, MultiAxisPlotter.defaultCursorStyle)
        self.annotationColors = Remember.toValid(annotationColors, list())
        self.annotationAlpha = Remember.toValid(annotationAlpha, MultiAxisPlotter.defaultAnnotationAlpha)
        self.annotationFrame = Remember.toValid(annotationFrame, MultiAxisPlotter.defaultAnnotationFrame)


class PlotterTrigger:
    def __init__(
            self,
            homeTrig: Remember = None,
            clearAllMarkTrig: Remember = None,
            clearLastMarkTrig: Remember = None,
            circleMarkFixTrig: Remember = None,
            canvasFlushTrig: Remember = None,
            exportFigureTrig: Remember = None,
            adjustLegendTrig: Remember = None,
            expandXLimTrig: Remember = None,
            expandYLimTrig: Remember = None,
            shrinkXLimTrig: Remember = None,
            shrinkYLimTrig: Remember = None,
    ):
        self.homeTrig = homeTrig
        self.clearAllMarkTrig = clearAllMarkTrig
        self.clearLastMarkTrig = clearLastMarkTrig
        self.circleMarkFixTrig = circleMarkFixTrig
        self.canvasFlushTrig = canvasFlushTrig
        self.exportFigureTrig = exportFigureTrig
        self.adjustLegendTrig = adjustLegendTrig
        self.expandXLimTrig = expandXLimTrig
        self.expandYLimTrig = expandYLimTrig
        self.shrinkXLimTrig = shrinkXLimTrig
        self.shrinkYLimTrig = shrinkYLimTrig


class CurvePlotter(MultiAxisPlotter):
    curveLabel: StyleKey = "label"
    curveVisible: StyleKey = "visible"
    curveLegendLocations: List[ModeArg] = ListData(
        MultiAxisPlotter.labelUpperLeftLoc,
        MultiAxisPlotter.labelUpperRightLoc,
        MultiAxisPlotter.labelLowerRightLoc,
        MultiAxisPlotter.labelLowerLeftLoc,
    ).data
    curvePinnerStyles: List[ModeArg] = ListData(
        MultiAxisPlotter.pinnerCircle,
        MultiAxisPlotter.pinnerSquare,
        MultiAxisPlotter.pinnerDiamond,
        MultiAxisPlotter.pinnerTriangle,
        MultiAxisPlotter.pinnerStar,
        MultiAxisPlotter.pinnerNone,
    ).data
    curveLineStyles: List[ModeArg] = ListData(
        MultiAxisPlotter.lineSolid,
        MultiAxisPlotter.lineDash,
        MultiAxisPlotter.lineDot,
        MultiAxisPlotter.lineDashDot,
    ).data

    def __init__(
            self,
            curveData: RState[CurveData] = None,
            xLabel: RState[str] = None,
            yLabels: RState[StringSTox] = None,
            aspectMode: RState[str] = None,
            width: float = 6.0,
            height: float = 4.0,
            dpi: int = 100,
            language: RState[NLIndex] = None,
            curveVisibles: RState[BoolSTox] = None,
            markLimit: RState[bool] = True,
            cursorOff: RState[bool] = False,
            gridOn: RState[bool] = True,
            plotterTrigs: PlotterTrigger = None,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: PlotterStyle = None,
            exportOptions: Dict[str, ExportOptionArg] = None,
    ):
        styleEditor: PlotterStyle = Validate(styleEditor, PlotterStyle())
        super().__init__(
            curveData=Remember.getDictValue(curveData),
            xLabel=Remember.getValue(xLabel),
            yLabels=Remember.getListValue(yLabels),
            aspectMode=Remember.getValue(aspectMode),
            width=width,
            height=height,
            dpi=dpi,
            style=Remember.getValue(styleEditor.style),
            lineWidths=Remember.getListValue(styleEditor.lineWidths),
            lineColors=Remember.getListValue(styleEditor.lineColors),
            lineStyles=Remember.getListValue(styleEditor.lineStyles),
            pinnerStyles=Remember.getListValue(styleEditor.pinnerStyles),
            pinnerSizes=Remember.getListValue(styleEditor.pinnerSizes),
            cursorStyle=Remember.getValue(styleEditor.cursorStyle),
            cursorAlpha=Remember.getValue(styleEditor.cursorAlpha),
            cursorColor=Remember.getValue(styleEditor.cursorColor),
            annotationAlpha=Remember.getValue(styleEditor.annotationAlpha),
            annotationFrame=Remember.getValue(styleEditor.annotationFrame),
            annotationColors=Remember.getListValue(styleEditor.annotationColors),
            markLimit=Remember.getValue(markLimit),
            cursorOff=Remember.getValue(cursorOff),
            gridOn=Remember.getValue(gridOn),
        )
        curveData = Remember.toValid(curveData, dict())
        yLabels = Remember.toValid(yLabels, list())
        lineWidths = Remember.toValid(styleEditor.lineWidths, list())
        lineColors = Remember.toValid(styleEditor.lineColors, list())
        lineStyles = Remember.toValid(styleEditor.lineStyles, list())
        pinnerStyles = Remember.toValid(styleEditor.pinnerStyles, list())
        pinnerSizes = Remember.toValid(styleEditor.pinnerSizes, list())
        annotationColors = Remember.toValid(styleEditor.annotationColors, list())
        curveVisibles = Remember.toValid(curveVisibles, list())
        self._curveParams = lambda idx: DictData(
            Key(self.curveLabel).Val(Remember.obtainListItem(yLabels, idx)),
            Key(PlotterStyle.atLineWidth).Val(Remember.obtainListItem(lineWidths, idx)),
            Key(PlotterStyle.atLineColor).Val(Remember.obtainListItem(lineColors, idx)),
            Key(PlotterStyle.atLineStyle).Val(Remember.obtainListItem(lineStyles, idx)),
            Key(PlotterStyle.atPinnerStyle).Val(Remember.obtainListItem(pinnerStyles, idx)),
            Key(PlotterStyle.atPinnerSize).Val(Remember.obtainListItem(pinnerSizes, idx)),
            Key(PlotterStyle.atAnnotationColor).Val(Remember.obtainListItem(annotationColors, idx)),
            Key(self.curveVisible).Val(Remember.obtainListItem(curveVisibles, idx))
        ).data
        self._curveKeys = list(Remember.getDictValue(curveData).keys())
        if isinstance(curveData, Remember):
            curveData.connect(lambda value: self.setCurveData(value), host=self)
        if isinstance(xLabel, Remember):
            xLabel.connect(lambda value: self.setXLabel(value), host=self)
        if isinstance(yLabels, Remember):
            yLabels.connect(lambda value: self.setYLabels(value), host=self)
        if isinstance(aspectMode, Remember):
            aspectMode.connect(lambda value: self.setAspectMode(value), host=self)
        if isinstance(lineWidths, Remember):
            lineWidths.connect(lambda value: self.setLineWidths(value), host=self)
        if isinstance(lineColors, Remember):
            lineColors.connect(lambda value: self.setLineColors(value), host=self)
        if isinstance(lineStyles, Remember):
            lineStyles.connect(lambda value: self.setLineStyles(value), host=self)
        if isinstance(pinnerStyles, Remember):
            pinnerStyles.connect(lambda value: self.setPinnerStyles(value), host=self)
        if isinstance(pinnerSizes, Remember):
            pinnerSizes.connect(lambda value: self.setPinnerSizes(value), host=self)
        if isinstance(annotationColors, Remember):
            annotationColors.connect(lambda value: self.setAnnotationColors(value), host=self)
        if isinstance(curveVisibles, Remember):
            curveVisibles.connect(lambda value: self.setCurveVisibles(value), host=self)
        for i, item in enumerate(Remember.getValue(curveData).items()):
            k, v = item
            if isinstance(k, Remember):
                k.uniqueConnect(self.setCurveDescription, i, host=self)
            if isinstance(v, Remember):
                updateData = lambda a0, a1=k: self.setAxCurveData(Remember.getValue(a1), a0)
                v.uniqueConnect(self.setAxCurveData, method=updateData, host=self)
        for i, label in enumerate(Remember.getValue(yLabels)):
            if isinstance(label, Remember):
                label.uniqueConnect(self.setYLabel, i, host=self)
        for i, width in enumerate(Remember.getValue(lineWidths)):
            if isinstance(width, Remember):
                width.uniqueConnect(self.setLineWidth, i, host=self)
        for i, style in enumerate(Remember.getValue(lineStyles)):
            if isinstance(style, Remember):
                style.uniqueConnect(self.setLineStyle, i, host=self)
        for i, style in enumerate(Remember.getValue(pinnerStyles)):
            if isinstance(style, Remember):
                style.uniqueConnect(self.setPinnerStyle, i, host=self)
        for i, size in enumerate(Remember.getValue(pinnerSizes)):
            if isinstance(size, Remember):
                size.uniqueConnect(self.setPinnerSize, i, host=self)
        for i, color in enumerate(Remember.getValue(lineColors)):
            if isinstance(color, Remember):
                color.uniqueConnect(self.setLineColor, i, host=self)
        for i, color in enumerate(Remember.getValue(annotationColors)):
            if isinstance(color, Remember):
                color.uniqueConnect(self.setAnnotationColor, i, host=self)
        for i, visible in enumerate(Remember.getValue(curveVisibles)):
            if isinstance(visible, Remember):
                visible.uniqueConnect(self.setCurveVisibleByIndex, i, host=self)
        if isinstance(styleEditor.style, Remember):
            styleEditor.style.connect(lambda value: self.setStyleSheet(value), host=self)
        if isinstance(styleEditor.cursorStyle, Remember):
            styleEditor.cursorStyle.connect(lambda value: self.setCursorStyle(value), host=self)
        if isinstance(styleEditor.cursorAlpha, Remember):
            styleEditor.cursorAlpha.connect(lambda value: self.setCursorAlpha(value), host=self)
        if isinstance(styleEditor.cursorColor, Remember):
            styleEditor.cursorColor.connect(lambda value: self.setCursorColor(value), host=self)
        if isinstance(styleEditor.annotationAlpha, Remember):
            styleEditor.annotationAlpha.connect(lambda value: self.setAnnotationAlpha(value), host=self)
        if isinstance(styleEditor.annotationFrame, Remember):
            styleEditor.annotationFrame.connect(lambda value: self.setAnnotationFrame(value), host=self)
        if isinstance(markLimit, Remember):
            markLimit.connect(lambda value: self.setMarkLimit(value), host=self)
        if isinstance(cursorOff, Remember):
            cursorOff.connect(lambda value: self.switchCursor(value), host=self)
        if isinstance(gridOn, Remember):
            gridOn.connect(lambda value: self.setCanvasGrid(value))
        self._lng = Validate(language, RString.EnglishIndex)
        self._exportOptions = Validate(exportOptions, dict())
        self.setPlotterTrigs(plotterTrigs)
        triggers = Validate(triggers, dict())
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    @private
    def setPlotterTrigs(self, trigs: PlotterTrigger):
        trigs: PlotterTrigger = Validate(trigs, PlotterTrigger())
        optionTrigs = DictData(
            Key(trigs.homeTrig).Val(self.restoreCanvas),
            Key(trigs.clearAllMarkTrig).Val(self.clearAllMarks),
            Key(trigs.clearLastMarkTrig).Val(self.clearLastMark),
            Key(trigs.canvasFlushTrig).Val(self.flushFigureCanvas),
            Key(trigs.adjustLegendTrig).Val(self.autoMoveLegend),
            Key(trigs.exportFigureTrig).Val(self.exportAxFigure),
            Key(trigs.circleMarkFixTrig).Val(self.fixCircleMarker),
            Key(trigs.expandXLimTrig).Val(partial(self.scaleXAxisLimitation, -self.defaultLimScaleRatio)),
            Key(trigs.expandYLimTrig).Val(partial(self.scaleYAxisLimitation, -self.defaultLimScaleRatio)),
            Key(trigs.shrinkXLimTrig).Val(partial(self.scaleXAxisLimitation, self.defaultLimScaleRatio)),
            Key(trigs.shrinkYLimTrig).Val(partial(self.scaleYAxisLimitation, self.defaultLimScaleRatio)),
        ).data
        for k, v in optionTrigs.items():
            if isinstance(k, Remember):
                k.connect(partial(v), host=self)
        return None

    @private
    def exportAxFigure(self, **options) -> bool:
        args = self._exportOptions.copy()
        args.update(options)
        dialog: Dialog = DataBox(ExportFigureDialog(
            parent=self, dialogOffset=None,
            drivePlotter=self, language=self._lng, **args,
        )).data
        result = Run(Execute(dialog)).result
        return bool(result[0])

    @private
    def fixCircleMarker(self) -> bool:
        dialog: Dialog = DataBox(FixCircleShapeDialog(
            parent=self, dialogOffset=None,
            drivePlotter=self, language=self._lng,
        )).data
        result = Run(Execute(dialog)).result
        return bool(result[0])

    @private
    def autoMoveLegend(self):
        locs = self.curveLegendLocations.copy()
        cur = self.currentLegendAt()
        if cur not in locs:
            cur = locs[0]
        else:
            cur = locs[int(locs.index(cur) + 1) % len(locs)]
        self.updateCurveLegends(loc=cur)
        return None

    @private
    def setLineStyles(self, styles: StringSTox):
        for i, style in enumerate(styles):
            if isinstance(style, Remember):
                style.uniqueConnect(self.setLineStyle, i, host=self)
            self.setLineStyle(i, Remember.getValue(style))
        return None

    @private
    def setPinnerStyles(self, styles: StringSTox):
        for i, style in enumerate(styles):
            if isinstance(style, Remember):
                style.uniqueConnect(self.setPinnerStyle, i, host=self)
            self.setPinnerStyle(i, Remember.getValue(style))
        return None

    @private
    def setPinnerSizes(self, sizes: FloatSTox):
        for i, size in enumerate(sizes):
            if isinstance(size, Remember):
                size.uniqueConnect(self.setPinnerSize, i, host=self)
            self.setPinnerSize(i, Remember.getValue(size))
        return None

    @private
    def setCurveVisibles(self, visibles: BoolSTox):
        for i, visible in enumerate(visibles):
            if isinstance(visible, Remember):
                visible.uniqueConnect(self.setCurveVisibleByIndex, i, host=self)
            self.setCurveVisibleByIndex(i, Remember.getValue(visible))
        return None

    @private
    def setAnnotationColors(self, colors: ColorSTox):
        for i, color in enumerate(colors):
            if isinstance(color, Remember):
                color.uniqueConnect(self.setAnnotationColor, i, host=self)
            self.setAnnotationColor(i, Remember.getValue(color))
        return None

    @private
    def setLineColors(self, colors: ColorSTox):
        for i, color in enumerate(colors):
            if isinstance(color, Remember):
                color.uniqueConnect(self.setLineColor, i, host=self)
            self.setLineColor(i, Remember.getValue(color))
            self.updateCurveLegends()
        return None

    @private
    def setLineWidths(self, widths: FloatSTox):
        for i, width in enumerate(widths):
            if isinstance(width, Remember):
                width.uniqueConnect(self.setLineWidth, i, host=self)
            self.setLineWidth(i, Remember.getValue(width))
        return None

    @private
    def setYLabels(self, labels: StringSTox):
        for i, label in enumerate(labels):
            if isinstance(label, Remember):
                label.uniqueConnect(self.setYLabel, i, host=self)
            self.setYLabel(i, Remember.getValue(label))
        return None

    @private
    def setAxCurveData(
            self, key: str, curveData: List[Tuple[float, float]], **kwargs: Any
    ) -> None:
        kwargs = DictToDefault(kwargs)
        return DataBox(super().setAxCurveData(
            key=key, curveData=curveData,
            label=kwargs[self.curveLabel],
            lineColor=kwargs[PlotterStyle.atLineColor],
            lineWidth=kwargs[PlotterStyle.atLineWidth],
            lineStyle=kwargs[PlotterStyle.atLineStyle],
            pinnerStyle=kwargs[PlotterStyle.atPinnerStyle],
            pinnerSize=kwargs[PlotterStyle.atPinnerSize],
            annotationColor=kwargs[PlotterStyle.atAnnotationColor]
        )).data

    @private
    def setCurveData(self, curveData: CurveData):
        if not isValid(curveData):
            return None
        self.clearFigCanvas()
        curveKeys = Remember.getListValue(curveData.keys())
        for k, v in curveData.items():
            idx = curveKeys.index(k)
            if isinstance(k, Remember):
                k.uniqueConnect(self.setCurveDescription, idx, host=self)
            if isinstance(v, Remember):
                v.uniqueConnect(self.setAxCurveData, Remember.getValue(k), host=self)
            description = Remember.getValue(k)
            axis_data = Remember.getValue(v)
            curveParams = self._curveParams(idx)
            self.setAxCurveData(description, axis_data, **curveParams)
            self.setCurveVisible(description, curveParams[self.curveVisible])
        self._curveKeys = curveKeys
        return None
