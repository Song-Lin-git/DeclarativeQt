import math
import time
from concurrent import futures
from itertools import chain
from typing import Dict, List, Callable, Tuple, Union, Any, Optional

import numpy as np
from PyQt5.QtCore import QSizeF
from matplotlib import pyplot as plt, patches, rcParams
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse
from matplotlib.text import Annotation
from scipy.spatial import cKDTree

from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import DataBox, ReferDict, ReferList, RepeatList, DtReferDict, \
    Validate, GList, GIters, Equal, isEmpty, inRange, StrFrame, GTuple, Inf, ConditionList, EnumList, PureList, isValid
from DeclarativeQt.Resource.Images.RImage import LutRatio
from DeclarativeQt.Resource.Strings.RString import RString

OptionArg = Union[float, int, str]
AnnotFrame = Callable[[float, float], str]
LayoutArg = Union[int, float, str, dict, Any]
CurveArg = Union[float, str, Any]
ModeFrame = Union[Dict, Callable]
ModeArg = str
PriorityArg = str
EventName = str
PlotterCpt = Tuple[Axes, Figure, FigureCanvasQTAgg]


class MultiAxisPlotter(FigureCanvasQTAgg):
    defaultLineWidth: CurveArg = 1.8
    defaultCurveStyle: CurveArg = "-"
    defaultCursorStyle: CurveArg = "--"
    defaultPinnerEdge: CurveArg = 0.2
    defaultPinnerStyle: CurveArg = "none"
    defaultPinnerSize: CurveArg = 0.0
    defaultPinnerEdgeColor: CurveArg = RColor.hexBlack
    defaultCursorColor: CurveArg = RColor.hexBlack
    defaultAnnotationAlpha: CurveArg = 0.2
    defaultCursorWidth: CurveArg = 1.0
    labelPadding: LayoutArg = 0
    annotationOffset: LayoutArg = GTuple(10, 10)
    cursorAboveOrder: LayoutArg = int(2)
    annotAboveOrder: LayoutArg = int(1)
    defaultMajorGridArgs: LayoutArg = dict(color=RColor.hexSoftStone, linewidth=0.8)
    defaultMinorGridArgs: LayoutArg = dict(color=RColor.hexPureMist, linewidth=0.4)
    defaultFigRatioMargin: LayoutArg = dict(left=0.06, right=0.96, top=0.96, bottom=0.12)
    defaultFigPixelMargin: LayoutArg = dict(left=80.0, right=35.0, top=30.0, bottom=70.0)
    annotationOffsetMeasure: ModeArg = "offset points"
    labelUpperLeftLoc: ModeArg = "upper left"
    labelUpperRightLoc: ModeArg = "upper right"
    labelLowerLeftLoc: ModeArg = "lower left"
    labelLowerRightLoc: ModeArg = "lower right"
    scrollUp: ModeArg = "up"
    axisOff: ModeArg = "off"
    lineDash: ModeArg = "--"
    lineSolid: ModeArg = "-"
    lineDashDot: ModeArg = "-."
    lineDot: ModeArg = ":"
    pinnerCircle: ModeArg = "o"
    pinnerNone: ModeArg = "none"
    pinnerTriangle: ModeArg = "^"
    pinnerDiamond: ModeArg = "D"
    pinnerSquare: ModeArg = "s"
    pinnerStar: ModeArg = "*"
    aspectEqual: ModeArg = "equal"
    aspectAuto: ModeArg = "auto"
    adjustableDatalim: ModeArg = "datalim"
    gridMinor: ModeArg = "minor"
    gridMajor: ModeArg = "major"
    axisY: ModeArg = "y"
    motionNotifyEvent: EventName = "motion_notify_event"
    pressEvent: EventName = "button_press_event"
    releaseEvent: EventName = "button_release_event"
    mouseScrollEvent: EventName = "scroll_event"
    canvasResizeEvent: EventName = "resize_event"
    xLimChangeEvent: EventName = "xlim_changed"
    yLimChangeEvent: EventName = "ylim_changed"
    priorityX: PriorityArg = "X"
    priorityManhattan: PriorityArg = "Manhattan"
    priorityEuclidean: PriorityArg = "Euclidean"
    priorityAuto: PriorityArg = "Auto"
    defaultAnnotationFrame: StrFrame = staticmethod(lambda x, y: f"x: {x:.4f}, y: {y:.4f}")
    annotationBBox: ModeFrame = staticmethod(lambda alpha: dict(boxstyle="round", fc="w", alpha=alpha))
    annotationArraw: LayoutArg = dict(arrowstyle="->")
    draggingRatio: OptionArg = 1.46
    doubleClickTimeThreshold: OptionArg = 0.3
    doubleClickPositionToleranceRatio: OptionArg = 0.1
    maxMarkCount: OptionArg = int(30)
    curveDistToleranceRatio: LutRatio = 0.07
    circleMarkRadiusRatio: LutRatio = 0.01
    circleMarkLimitRatio: LutRatio = 1.0
    circleMarkFixRatio: LutRatio = 0.91434
    defaultLimScaleRatio: LutRatio = 0.12
    axisExpandRatio: LutRatio = 0.03
    prtFontName: OptionArg = "font.sans-serif"
    prtUnicodeMinus: OptionArg = "axes.unicode_minus"

    def __init__(
            self,
            datas: Dict[str, List[Tuple[float, float]]] = None,
            xLabel: str = None,
            yLabels: List[str] = None,
            style: str = None,
            width: float = 6.0,
            height: float = 5.0,
            dpi: int = 100,
            autoLayout: bool = False,
            aspectMode: str = None,
            lineColors: List[str] = None,
            lineWidths: List[float] = None,
            lineStyles: List[str] = None,
            pinnerStyles: List[str] = None,
            pinnerSizes: List[float] = None,
            cursorColor: str = None,
            cursorAlpha: float = 1.0,
            cursorStyle: str = None,
            annotationColors: List[str] = None,
            annotationAlpha: float = None,
            annotationFrame: AnnotFrame = None,
            markLimit: bool = True,
            cursorOff: bool = False,
            gridOn: bool = True,
            circleFixRatio: float = None
    ):
        rcParams[self.prtFontName] = GList(RFont.YaHei)
        rcParams[self.prtUnicodeMinus] = False
        figSize = GTuple(width, height)
        self._fig = Figure(figsize=figSize, dpi=dpi, constrained_layout=autoLayout)
        self._fontProp = FontProperties(GList(RFont.YaHei, RFont.SegoeUI, RFont.TNR, RFont.SimHei))
        self._ax: Axes = self._fig.add_subplot()
        self._aspectMode = Validate(aspectMode, self.aspectEqual)
        self._ax.set_adjustable(self.adjustableDatalim)
        self._ax.set_aspect(self._aspectMode)
        super(MultiAxisPlotter, self).__init__(self._fig)
        self._autoLayout = autoLayout
        if not self._autoLayout:
            self.adjustFigLayout()
        if style is not None:
            self.setStyleSheet(style)
        datas = DtReferDict(Validate(datas, dict()), valExp=lambda k, v: self.cleanLineData(v))
        self._xAxis: List = ReferList(datas.values(), lambda v: ReferList(v, lambda p: p[0]))
        self._yDatas: Dict = DtReferDict(datas, lambda k, v: k, lambda k, v: ReferList(v, lambda p: p[1]))
        self._lines = list()
        self._lineCount = len(datas)
        self._dataRanges = list()
        self.fixDataSequence()
        self._KDTrees = list()
        self._cursorColor = Validate(cursorColor, RColor().randomColor())
        self._cursorAlpha = max(0.0, min(1.0, cursorAlpha))
        self._cursorStyle = Validate(cursorStyle, self.defaultCursorStyle)
        self._annotationAlpha = Validate(annotationAlpha, self.defaultAnnotationAlpha)
        self._annotationAlpha = max(0.0, min(1.0, self._annotationAlpha))
        self._annotationFrame = Validate(annotationFrame, lambda x, y: self.defaultAnnotationFrame(x, y))
        self._lineColors = Validate(lineColors, list())[:self._lineCount]
        self._lineWidths = Validate(lineWidths, list())[:self._lineCount]
        self._lineStyles = Validate(lineStyles, list())[:self._lineCount]
        self._pinnerStyles = Validate(pinnerStyles, list())[:self._lineCount]
        self._pinnerSizes = Validate(pinnerSizes, list())[:self._lineCount]
        self._annonationColors = Validate(annotationColors, list())[:self._lineCount]
        self._yLabels = Validate(yLabels, list())[:self._lineCount]
        self.fixMaterials()
        self._markLimit = markLimit
        self._cursorOff = cursorOff
        self._gridOn = gridOn
        self.setCanvasGrid(gridOn)
        self._circleFixRatio = Validate(circleFixRatio, self.circleMarkFixRatio)
        self._annotationMarks: Dict = ReferDict(range(self._lineCount), lambda it: it, lambda it: list())
        self._markRecord = list()
        for i in range(self._lineCount):
            self.drawCurve(i)
        self._legendLoc = self.labelUpperLeftLoc
        self.updateCurveLegends()
        if xLabel:
            self._ax.set_xlabel(xLabel)
        self._yLimitation = None
        self._xLimitation = None
        self._isDragging = False
        self._dragStart = None
        self._lastClick = None
        self._dragged = False
        self._scaled = False
        self._annotation: Annotation = DataBox(self._ax.annotate(
            RString.pEmpty, xy=GTuple(0, 0), xytext=self.annotationOffset,
            textcoords=self.annotationOffsetMeasure, bbox=self.annotationBBox(self._annotationAlpha),
            fontproperties=self._fontProp, arrowprops=self.annotationArraw
        )).data
        self._annotation.set_visible(False)
        self._vline, self._hline = None, None
        visibleExp = lambda idx, b0: b0 if self._lines[idx].get_visible() else None
        self._visibleAxis = lambda a0: PureList(EnumList(a0, exp=visibleExp))
        self.drawCrossCursor()
        self.syncAxisLimitations()
        self.updateKDTreeFromCurveData()
        self.updateCurveDataRange()
        self.destroyed.connect(lambda: self.closeFigureCanvas())
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(self.motionNotifyEvent, self.onMouseMove)
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(self.mouseScrollEvent, self.onScroll)
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(self.pressEvent, self.onMousePress)
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(self.releaseEvent, self.onMouseRelease)
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(self.canvasResizeEvent, self.onCanvasResize)
        self._ax.callbacks.connect(self.xLimChangeEvent, self.onCanvasResize)
        self._ax.callbacks.connect(self.yLimChangeEvent, self.onCanvasResize)

    @staticmethod
    def cleanLineData(datas: List[Tuple[float, float]]):
        datas = ConditionList(datas, lambda a0: None not in a0)
        if len(datas) <= 0:
            datas = GList(GTuple(float(0), float(0)))
        return datas

    def calcRatioMargin(self, pixelMargin: dict) -> dict:
        left, right, top, bottom = pixelMargin.values()
        width, height = self.width(), self.height()
        margins = GList(left / width, 1.0 - right / width, 1.0 - top / height, bottom / height)
        return dict(zip(pixelMargin.keys(), margins))

    def adjustFigLayout(self):
        self.adjustPlots(self._fig)
        self.adjustAxesPosition(self._ax, **self.calcRatioMargin(self.defaultFigPixelMargin))
        return None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustFigLayout()
        return None

    def wheelEvent(self, event):
        super().wheelEvent(event)
        event.accept()
        return None

    def setCanvasGrid(self, grid: bool):
        self._gridOn = grid
        if not grid:
            self._ax.grid(False, which=self.gridMajor)
            self._ax.grid(False, which=self.gridMinor)
        else:
            self._ax.grid(which=self.gridMajor, **self.defaultMajorGridArgs)
            self._ax.minorticks_on()
            self._ax.grid(which=self.gridMinor, **self.defaultMinorGridArgs)
        self._fig.canvas.draw_idle()
        return None

    @staticmethod
    def pltAdjustPlots(margin: dict = None):
        margin = Validate(margin, MultiAxisPlotter.defaultFigRatioMargin)
        plt.subplots_adjust(**margin)
        return None

    @staticmethod
    def adjustPlots(figure: Figure, margin: dict = None):
        margin = Validate(margin, MultiAxisPlotter.defaultFigRatioMargin)
        figure.subplots_adjust(**margin)
        return None

    @staticmethod
    def adjustAxesPosition(ax: Axes, **margins: float):
        ratioMargin = MultiAxisPlotter.defaultFigRatioMargin.copy()
        ratioMargin.update(margins)
        left, right, top, bottom = ratioMargin.values()
        ax.set_position(GList(left, bottom, right - left, top - bottom))
        return None

    def flushFigureCanvas(self):
        self._fig.canvas.flush_events()
        if not self._autoLayout:
            self.adjustFigLayout()
        return None

    def closeFigureCanvas(self):
        plt.close(self._fig)
        return None

    def sampleCircleSize(self, aspectRatio: float = None) -> Tuple[float, float]:
        return self.calcCircleEllipseSize(limit=False, aspectRatio=aspectRatio)

    def copyAnnotationsToAxes(self, tarAx: Axes):
        for circle, annot in self._markRecord:
            color = circle.get_edgecolor()
            ax_circle: Ellipse = DataBox(patches.Ellipse(
                GTuple(0, 0), circle.width, circle.height, color=color, zorder=circle.get_zorder(),
                linewidth=circle.get_linewidth(), linestyle=circle.get_linestyle(), fill=False
            )).data
            ax_circle.center = circle.center
            tarAx.add_patch(ax_circle)
            ax_annot: Annotation = DataBox(tarAx.annotate(
                annot.get_text(), xy=annot.xy, xytext=self.annotationOffset,
                textcoords=self.annotationOffsetMeasure, arrowprops=self.annotationArraw,
                bbox=MultiAxisPlotter.annotationBBox(self._annotationAlpha),
                fontproperties=self._fontProp,
            )).data
            ax_annot.get_bbox_patch().set_facecolor(color)
        return None

    def copyCurvesToAxes(self, tarAx: Axes, labelLoc: str = None):
        y_labels, plot_lines = list(), list()
        for i, line in enumerate(self._lines):
            if not line.get_visible():
                continue
            plot_lines += DataBox(tarAx.plot(
                line.get_xdata(), line.get_ydata(), label=line.get_label(),
                linestyle=line.get_linestyle(), linewidth=line.get_linewidth(),
                marker=line.get_marker(), color=line.get_color(), markersize=line.get_markersize(),
                markeredgecolor=self.defaultPinnerEdgeColor, markeredgewidth=self.defaultPinnerEdge
            )).data
            y_labels.append(self._yLabels[i])
        tarAx.legend(plot_lines, y_labels, loc=Validate(labelLoc, self._legendLoc), prop=self._fontProp)
        if self._gridOn:
            tarAx.grid(which=self.gridMajor, **self.defaultMajorGridArgs)
            tarAx.minorticks_on()
            tarAx.grid(which=self.gridMinor, **self.defaultMinorGridArgs)
        return None

    def plotterCopy(
            self, aspectMode: str = None, curvesCopy: bool = False, labelLoc: str = None
    ) -> PlotterCpt:
        figSize = GTuple(*self._fig.get_size_inches())
        copyFig: Figure = Figure(figsize=figSize, dpi=self._fig.get_dpi())
        copyAx: Axes = copyFig.add_subplot()
        xlim, ylim = self._ax.get_xlim(), self._ax.get_ylim()
        originAspect = self._aspectMode
        aspectKeep = not bool(aspectMode and not Equal(originAspect, aspectMode))
        if not aspectKeep:
            self.setAspectMode(aspectMode, flush=True)
        copyAx.set_aspect(self._aspectMode, adjustable=self.adjustableDatalim)
        copyAx.set_xlim(self._ax.get_xlim())
        copyAx.set_ylim(self._ax.get_ylim())
        if not aspectKeep:
            self.setAspectMode(originAspect, flush=True)
            self._ax.set_xlim(xlim)
            self._ax.set_ylim(ylim)
        if curvesCopy:
            self.adjustPlots(copyFig)
            self.adjustAxesPosition(copyAx, **self.calcRatioMargin(self.defaultFigPixelMargin))
            copyAx.set_xlabel(self._ax.get_xlabel())
            self.copyCurvesToAxes(copyAx, labelLoc)
            self.copyAnnotationsToAxes(copyAx)
        copyPlot = GTuple(copyAx, copyFig)
        return GTuple(*copyPlot, FigureCanvasQTAgg(copyFig))

    def scaleCircleFixRatio(self, scaleRate: float):
        self._circleFixRatio = self._circleFixRatio * scaleRate
        self.resizeAllCircleMarks()
        return None

    def switchCursor(self, off: bool):
        self._cursorOff = off
        if off:
            self.clearCursorAnnotation()
            self._fig.canvas.draw_idle()
        return None

    def setAnnotationFrame(self, frame: AnnotFrame):
        self._annotationFrame = frame
        return None

    def setAnnotationAlpha(self, alpha: float):
        self._annotationAlpha = alpha
        for mark in self._markRecord:
            annotation = mark[1]
            annotation.get_bbox_patch().set_alpha(alpha)
        self._annotation.get_bbox_patch().set_alpha(alpha)
        self._fig.canvas.draw_idle()
        return None

    def setCursorStyle(self, cursorStyle: str):
        self._cursorStyle = cursorStyle
        self._hline.set_linestyle(cursorStyle)
        self._vline.set_linestyle(cursorStyle)
        self._fig.canvas.draw_idle()
        return None

    def setCursorAlpha(self, cursorAlpha: float):
        self._cursorAlpha = cursorAlpha
        self._hline.set_alpha(cursorAlpha)
        self._vline.set_alpha(cursorAlpha)
        self._fig.canvas.draw_idle()
        return None

    def setCursorColor(self, cursorColor: str):
        self._cursorColor = cursorColor
        self._hline.set_color(cursorColor)
        self._vline.set_color(cursorColor)
        self._fig.canvas.draw_idle()
        return None

    def setAnnotationColor(self, idx: int, annotationColor: str):
        if not self.isValidIndex(idx):
            return None
        self._annonationColors[idx] = annotationColor
        for circle, annotation in self._annotationMarks[idx]:
            annotation.get_bbox_patch().set_facecolor(annotationColor)
            circle.set_edgecolor(annotationColor)
        self._fig.canvas.draw_idle()
        return None

    def setLineWidth(self, idx: int, lineWidth: float):
        if not self.isValidIndex(idx):
            return None
        self._lineWidths[idx] = lineWidth
        self._lines[idx].set_linewidth(lineWidth)
        self.updateCurveLegends()
        self._fig.canvas.draw_idle()
        return None

    def setLineColor(self, idx: int, lineColor: str):
        if not self.isValidIndex(idx):
            return None
        self._lineColors[idx] = lineColor
        self._lines[idx].set_color(lineColor)
        self.updateCurveLegends()
        self._fig.canvas.draw_idle()
        return None

    def setLineStyle(self, idx: int, lineStyle: str):
        if not self.isValidIndex(idx):
            return None
        self._lineStyles[idx] = lineStyle
        self._lines[idx].set_linestyle(lineStyle)
        self.updateCurveLegends()
        self._fig.canvas.draw_idle()
        return None

    def setPinnerStyle(self, idx: int, pinnerStyle: str):
        if not self.isValidIndex(idx):
            return None
        self._pinnerStyles[idx] = pinnerStyle
        self._lines[idx].set_marker(pinnerStyle)
        self.updateCurveLegends()
        self.resizeCircleMarks(idx)
        self._fig.canvas.draw_idle()
        return None

    def setPinnerSize(self, idx: int, pinnerSize: float):
        if not self.isValidIndex(idx):
            return None
        self._pinnerSizes[idx] = pinnerSize
        self._lines[idx].set_markersize(pinnerSize)
        self.updateCurveLegends()
        self.resizeCircleMarks(idx)
        self._fig.canvas.draw_idle()
        return None

    @private
    def clearCursorAnnotation(self):
        self._vline.set_visible(False)
        self._hline.set_visible(False)
        self._annotation.set_visible(False)
        return None

    @private
    def clearAllCurves(self):
        for line in self._lines:
            line.remove()
        self._lines.clear()
        return None

    def clearFigCanvas(self):
        self.clearAllMarks()
        self._xAxis.clear()
        self._yDatas.clear()
        self._yLabels.clear()
        self.clearAllCurves()
        self._lineWidths.clear()
        self._lineColors.clear()
        self._lineStyles.clear()
        self._pinnerSizes.clear()
        self._pinnerStyles.clear()
        self._annonationColors.clear()
        self.clearCursorAnnotation()
        self.stopMouseOptions()
        self._lineCount = 0
        self.updateCurveLegends()
        self._fig.canvas.draw_idle()
        return None

    def setCurveDescription(self, idx: int, description: str):
        if not self.isValidIndex(idx):
            return None
        if Equal(list(self._yDatas.keys())[idx], description):
            return None
        self._lines[idx].set_label(description)
        yAxisDatas = dict()
        for i, item in enumerate(self._yDatas.items()):
            k, v = item
            if not Equal(i, idx):
                yAxisDatas[k] = v
                continue
            yAxisDatas[description] = v
        self._yDatas = yAxisDatas
        self._fig.canvas.draw_idle()
        return None

    def setYLabel(self, idx: int, yLabel: str):
        if not self.isValidIndex(idx):
            return None
        self._yLabels[idx] = yLabel
        self.updateCurveLegends()
        for circlr, annot in self._annotationMarks[idx]:
            text = annot.get_text().split(RString.pLinefeed)[1:]
            annot.set_text(RString.pLinefeed.join(GList(yLabel) + text))
        self._fig.canvas.draw_idle()
        return None

    def setXLabel(self, xLabel: str):
        self._ax.set_xlabel(xLabel)
        self._fig.canvas.draw_idle()
        return None

    def setMarkLimit(self, markLimit: bool):
        self._markLimit = markLimit
        return None

    def clearLastMark(self):
        if len(self._markRecord) < 1:
            return None
        circle, annotation = self._markRecord[-1]
        self._markRecord = self._markRecord[:-1]
        circle.remove()
        annotation.remove()
        for key, val in self._annotationMarks.items():
            if GTuple(circle, annotation) in val:
                self._annotationMarks[key].remove(GTuple(circle, annotation))
                break
        self._fig.canvas.draw_idle()
        return None

    @private
    def drawCurve(self, idx: int):
        if not self.isValidIndex(idx):
            return None
        plot_line: List[Line2D] = DataBox(self._ax.plot(
            self._xAxis[idx], list(self._yDatas.values())[idx],
            linestyle=self._lineStyles[idx], linewidth=self._lineWidths[idx],
            label=list(self._yDatas.keys())[idx], color=self._lineColors[idx],
            marker=self._pinnerStyles[idx], markersize=self._pinnerSizes[idx],
            markeredgecolor=self.defaultPinnerEdgeColor, markeredgewidth=self.defaultPinnerEdge
        )).data
        self._lines += plot_line
        self._annotationMarks[idx] = list()
        self._fig.canvas.draw_idle()
        return None

    def setAxCurveDatas(
            self, key: str, datas: List[Tuple[float, float]], label: str = None,
            lineColor: str = None, lineWidth: float = None, lineStyle: str = None,
            pinnerStyle: str = None, pinnerSize: float = None, annotationColor: str = None
    ) -> None:
        pre_count = self._lineCount
        datas = self.cleanLineData(datas)
        yAxisData = ReferList(datas, lambda p: p[1])
        xAxisData = ReferList(datas, lambda p: p[0])
        if key in self._yDatas:
            self._yDatas[key] = yAxisData
            idx = list(self._yDatas.keys()).index(key)
            self._xAxis[idx] = xAxisData
            self._lines[idx].set_data(self._xAxis[idx], self._yDatas[key])
            self.checkMarkValidation(idx)
        else:
            self._yDatas[key] = yAxisData
            self._xAxis.append(xAxisData)
            if lineColor is not None:
                self._lineColors.append(lineColor)
            if lineWidth is not None:
                self._lineWidths.append(lineWidth)
            if lineStyle is not None:
                self._lineStyles.append(lineStyle)
            if pinnerStyle is not None:
                self._pinnerStyles.append(pinnerStyle)
            if pinnerSize is not None:
                self._pinnerSizes.append(pinnerSize)
            if annotationColor is not None:
                self._annonationColors.append(annotationColor)
            if label is not None:
                self._yLabels.append(label)
            self._lineCount += 1
            self.fixMaterials()
            self.drawCurve(self._lineCount - 1)
            self.updateCurveLegends()
        self.updateKDTreeFromCurveData()
        self.updateCurveDataRange()
        self._fig.canvas.draw_idle()
        if pre_count <= 0 or bool(not self._scaled and not self._dragged):
            self.syncAxisLimitations()
        return None

    def restoreCanvas(self, sync: bool = True):
        if sync:
            self.syncAxisLimitations()
            return None
        self.stopMouseOptions()
        self._ax.set_xlim(self._xLimitation)
        self._ax.set_ylim(self._yLimitation)
        self._fig.canvas.draw_idle()
        return None

    @private
    def scaleCanvas(self, xdata: float, ydata: float, scaleFactor: float):
        self._scaled = True
        xlim = self._ax.get_xlim()
        ylim = self._ax.get_ylim()
        xlim = GList(xdata + (xlim[0] - xdata) * scaleFactor, xdata + (xlim[1] - xdata) * scaleFactor)
        ylim = GList(ydata + (ylim[0] - ydata) * scaleFactor, ydata + (ylim[1] - ydata) * scaleFactor)
        self._ax.set_xlim(xlim)
        self._ax.set_ylim(ylim)
        self._fig.canvas.draw_idle()
        return None

    @private
    def dragCanvas(self, x: float, y: float, xStart: float, yStart: float):
        self._dragged = True
        dx = float(x - xStart) * self.draggingRatio
        dy = float(y - yStart) * self.draggingRatio
        xlim = self._ax.get_xlim()
        ylim = self._ax.get_ylim()
        self._ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
        self._ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
        self._fig.canvas.draw_idle()
        return None

    def clearAllMarks(self):
        for i in range(self._lineCount):
            self.clearAnnotMark(i)
        self._fig.canvas.draw_idle()
        return None

    def setCurveVisibleByIndex(self, idx: int, visible: bool):
        if not self.isValidIndex(idx):
            return None
        self._lines[idx].set_visible(visible)
        if not visible:
            self.clearAnnotMark(idx)
        self.updateCurveLegends()
        self._fig.canvas.draw_idle()
        return None

    def setCurveVisible(self, key: str, visible: bool):
        if key not in self._yDatas:
            return None
        idx = list(self._yDatas.keys()).index(key)
        self.setCurveVisibleByIndex(idx, visible)
        return None

    def setAspectMode(self, aspectMode: str, flush: bool = True):
        self._aspectMode = aspectMode
        self._ax.set_aspect(aspectMode, adjustable=self.adjustableDatalim)
        self.syncAxisLimitations(flush)
        return None

    @private
    def isValidIndex(self, idx: int):
        if idx < 0 or idx >= self._lineCount:
            return False
        return True

    @private
    def xAxisValues(self) -> list:
        return list(set(chain(*self._visibleAxis(self._xAxis))))

    @private
    def yAxisValues(self) -> list:
        return list(set(chain(*list(self._visibleAxis(self._yDatas.values())))))

    @private
    def axisScopeSpan(self):
        x_lim, y_lim = self._ax.get_xlim(), self._ax.get_ylim()
        x_span = abs(x_lim[1] - x_lim[0])
        y_span = abs(y_lim[1] - y_lim[0])
        return GTuple(x_span, y_span)

    @private
    def curveDataSpan(self):
        xAxisData = self.xAxisValues()
        yAxisData = self.yAxisValues()
        if isEmpty(xAxisData) or isEmpty(yAxisData):
            return float(0), float(0)
        x_span = max(xAxisData) - min(xAxisData)
        y_span = max(yAxisData) - min(yAxisData)
        return GTuple(x_span, y_span)

    @private
    def axisAspectRatio(self) -> float:
        width, height = self.axisScopeSpan()
        return DqtCanvas.rectAspect(QSizeF(float(width), float(height)))

    @private
    def canvasAspectRatio(self) -> float:
        width, height = self._fig.get_size_inches()
        return DqtCanvas.rectAspect(QSizeF(float(width), float(height)))

    @private
    def calcCircleEllipseSize(self, limit: bool = True, aspectRatio: float = None) -> Tuple[float, float]:
        axis_aspect = Validate(aspectRatio, self.axisAspectRatio())
        circle_radius = min(self.axisScopeSpan()) * self.circleMarkRadiusRatio
        if limit:
            limitation = max(self.curveDataSpan()) * self.circleMarkRadiusRatio * self.circleMarkLimitRatio
            circle_radius = min(circle_radius, limitation)
        canvas_aspect = self.canvasAspectRatio()
        ratio = axis_aspect / canvas_aspect * self._circleFixRatio
        if axis_aspect > 1.0:
            width: float = circle_radius * ratio
            return GTuple(width, circle_radius)
        height: float = circle_radius / ratio
        return GTuple(circle_radius, height)

    @private
    def stopMouseOptions(self):
        self._dragged = False
        self._scaled = False
        return None

    def currentLegendAt(self):
        return self._legendLoc

    @private
    def updateCurveLegends(self, loc: ModeArg = None):
        loc = Validate(loc, self._legendLoc)
        lines, yLabels = list(), list()
        for i in range(self._lineCount):
            if not self._lines[i].get_visible():
                continue
            lines.append(self._lines[i])
            yLabels.append(self._yLabels[i])
        self._ax.legend(lines, yLabels, loc=loc, prop=self._fontProp)
        self._legendLoc = loc
        self._fig.canvas.draw_idle()
        return None

    @private
    def checkMarkValidation(self, idx: int):
        if not self.isValidIndex(idx):
            return None
        for circle, annotation in self._annotationMarks[idx]:
            x, y = circle.center
            found = False
            if x in self._xAxis[idx]:
                data_index = self._xAxis[idx].index(x)
                if Equal(list(self._yDatas.values())[idx][data_index], y):
                    found = True
            if not found:
                circle.remove()
                annotation.remove()
                self._annotationMarks[idx].remove(GTuple(circle, annotation))
                self._markRecord.remove(GTuple(circle, annotation))
        self._fig.canvas.draw_idle()
        return None

    @private
    def clearAnnotMark(self, index: int):
        if index not in self._annotationMarks:
            return None
        for circle, annotation in self._annotationMarks[index]:
            circle.remove()
            annotation.remove()
            self._markRecord.remove(GTuple(circle, annotation))
        self._annotationMarks[index].clear()
        return None

    def setMarkAnnotationsVisible(self, visible: bool):
        for circle, annotation in self._markRecord:
            annotation.set_visible(visible)
        self._fig.canvas.draw_idle()
        return None

    @private
    def syncAxisLimitations(self, flush: bool = True):
        self.stopMouseOptions()
        self._xLimitation = self.syncXAxisLimitation(flush)
        self._yLimitation = self.syncYAxisLimitation(flush)
        if flush:
            self.flushFigureCanvas()
        return None

    @private
    def scaleYAxisLimitation(self, ratio: float, flush: bool = True):
        y_lim = self._ax.get_ylim()
        if not Equal(self._aspectMode, self.aspectAuto):
            return y_lim
        y_min, y_max = y_lim
        y_span = ratio * float(y_max - y_min)
        y_min += -y_span / 2.0
        y_max += y_span / 2.0
        y_lim = GList(y_min, y_max)
        self._ax.set_ylim(y_min, y_max)
        if flush:
            self._fig.canvas.draw_idle()
        return y_lim

    @private
    def scaleXAxisLimitation(self, ratio: float, flush: bool = True):
        x_lim = self._ax.get_xlim()
        if not Equal(self._aspectMode, self.aspectAuto):
            return x_lim
        x_min, x_max = x_lim
        x_span = ratio * float(x_max - x_min)
        x_min += -x_span / 2.0
        x_max += x_span / 2.0
        x_lim = GList(x_min, x_max)
        self._ax.set_xlim(x_min, x_max)
        if flush:
            self._fig.canvas.draw_idle()
        return x_lim

    @private
    def syncYAxisLimitation(self, flush: bool = True) -> List:
        yAxis = self.yAxisValues()
        y_min, y_max = 0, 1.0
        if len(yAxis) > 0 and min(yAxis) != max(yAxis):
            y_min, y_max = min(yAxis), max(yAxis)
        expand = abs(y_max - y_min) * self.axisExpandRatio
        y_min += -expand
        y_max += expand
        y_lim = GList(y_min, y_max)
        self._ax.set_ylim(y_min, y_max)
        if flush:
            self._fig.canvas.draw_idle()
        return y_lim

    @private
    def syncXAxisLimitation(self, flush: bool = True) -> List:
        xAxis = self.xAxisValues()
        x_min, x_max = 0, 1.0
        if len(xAxis) > 0 and min(xAxis) != max(xAxis):
            x_min, x_max = min(xAxis), max(xAxis)
        expand = abs(x_max - x_min) * self.axisExpandRatio
        x_min += -expand
        x_max += expand
        x_lim = GList(x_min, x_max)
        self._ax.set_xlim(x_min, x_max)
        if flush:
            self._fig.canvas.draw_idle()
        return x_lim

    @private
    def fixNearestPriority(self, priority: str):
        priority = Validate(priority, self.priorityX)
        if Equal(priority, self.priorityAuto):
            if Equal(self._aspectMode, self.aspectEqual):
                return self.priorityEuclidean
            return self.priorityX
        return priority

    @private
    def updateKDTreeFromCurveData(self):
        self._KDTrees.clear()
        for i, line in enumerate(self._lines):
            x_data, y_data = np.array(line.get_xdata()), np.array(line.get_ydata())
            try:
                self._KDTrees.append(cKDTree(np.column_stack(GTuple(x_data, y_data))))
            except Exception as e:
                RString.log(str(e), RString.pLogError)
        return None

    @private
    def updateCurveDataRange(self):
        self._dataRanges.clear()
        for i, line in enumerate(self._lines):
            x_data, y_data = np.array(line.get_xdata()), np.array(line.get_ydata())
            x_range = GTuple(np.min(x_data), np.max(x_data))
            y_range = GTuple(np.min(y_data), np.max(y_data))
            self._dataRanges.append(GTuple(x_range, y_range))
        return None

    def isOutOfCurveRange(self, idx: int, x: float, y: float, tolerance: float = Inf):
        if not self.isValidIndex(idx):
            return True
        x_range, y_range = self._dataRanges[idx]
        x_min, x_max = x_range
        y_min, y_max = y_range
        if tolerance >= Inf:
            tolerance = max(abs(x_max - x_min), abs(y_max - y_min)) * self.curveDistToleranceRatio
        x_min, x_max = x_min - tolerance, x_max + tolerance
        y_min, y_max = y_min - tolerance, y_max + tolerance
        if not inRange(x, x_min, x_max) or not inRange(y, y_min, y_max):
            return True
        return False

    def findNearestPointWithThread(self, x: float, y: float, tolerance: float = Inf):
        min_distance = Inf
        curve_index, idx = -1, -1
        with futures.ThreadPoolExecutor() as executor:
            find_nearest = lambda t: self._KDTrees[t].query(GList(x, y))
            search_range = ConditionList(list(range(self._lineCount)), lambda t: self._lines[t].get_visible())
            search_range = ConditionList(search_range, lambda t: not self.isOutOfCurveRange(t, x, y, tolerance))
            result = list(executor.map(find_nearest, search_range))
            if len(result) > 0:
                nearest = min(result, key=lambda t: t[0])
                curve_index = search_range[result.index(nearest)]
                min_distance, idx = nearest
        return GTuple(min_distance, curve_index, idx)

    @private
    def findNearestPointByAlgorithm(self, x: float, y: float, priority: str = None, tolerance: float = Inf):
        min_distance = Inf
        curve_index, data_index = -1, -1
        for i, line in enumerate(self._lines):
            if not self._lines[i].get_visible():
                continue
            if not Equal(priority, self.priorityX) and self.isOutOfCurveRange(i, x, y, tolerance):
                continue
            x_data, y_data = np.array(line.get_xdata()), np.array(line.get_ydata())
            if x_data.size <= 0:
                continue
            if Equal(priority, self.priorityX):
                idx = np.argmin(np.abs(x_data - x))
                distance = np.abs(y_data[idx] - y)
                xAxis = self.xAxisValues()
                if inRange(x, min(xAxis), max(xAxis)) and np.abs(x_data[idx] - x) > tolerance:
                    continue
            elif Equal(priority, self.priorityEuclidean):
                distance, idx = self._KDTrees[i].query(GList(x, y))
            elif Equal(priority, self.priorityManhattan):
                idx = np.argmin(np.abs(x_data - x) + np.abs(y_data - y))
                distance = np.abs(x_data[idx] - x) + np.abs(y_data[idx] - y)
            else:
                idx = np.argmin(np.sqrt(np.pow(x_data - x, 2) + np.pow(y_data - y, 2)))
                distance = np.sqrt(np.pow(x_data[idx] - x, 2) + np.pow(y_data[idx] - y, 2))
            if distance < min_distance:
                min_distance = distance
                curve_index, data_index = i, idx
        return GTuple(min_distance, curve_index, data_index)

    @private
    def findNearestPoint(
            self, x: float, y: float, limited: bool = False, priority: str = None, useThread: bool = False
    ) -> Optional[Tuple[int, Tuple[float, float]]]:
        priority = self.fixNearestPriority(priority)
        tolerance = self.curveDistToleranceRatio * max(self.axisScopeSpan())
        if useThread and Equal(priority, self.priorityEuclidean):
            min_distance, curve_index, idx = self.findNearestPointWithThread(x, y, tolerance)
        else:
            min_distance, curve_index, idx = self.findNearestPointByAlgorithm(x, y, priority, tolerance)
        if curve_index < 0 or idx < 0 or bool(limited and min_distance > tolerance):
            return None
        nearest_line = self._lines[curve_index]
        x_nearest, y_nearest = nearest_line.get_xdata()[idx], nearest_line.get_ydata()[idx]
        return curve_index, GTuple(float(x_nearest), float(y_nearest))

    @private
    def onCanvasResize(self, event):
        if isValid(event):
            self.resizeAllCircleMarks()
        return None

    def resizeAllCircleMarks(self) -> None:
        for idx in self._annotationMarks.keys():
            self.resizeCircleMarks(idx)
        self._fig.canvas.draw_idle()
        return None

    def resizeCircleMarks(self, idx: int):
        if not self.isValidIndex(idx):
            return None
        circle_size = self.calcCircleEllipseSize()
        pinned = self.isCurvePinned(idx)
        width, height = circle_size if not pinned else GTuple(0, 0)
        for circle, annotation in self._annotationMarks[idx]:
            circle.set_width(width)
            circle.set_height(height)
        self._fig.canvas.draw_idle()
        return None

    def isCurvePinned(self, idx: int):
        if not self.isValidIndex(idx):
            return False
        pinned = not Equal(self._lines[idx].get_marker(), self.pinnerNone)
        size = self._lines[idx].get_markersize()
        return pinned and size > 0.0

    @private
    def onScroll(self, event) -> None:
        if event.inaxes is None:
            return None
        scale_factor = 1.25 if event.button not in GIters(self.scrollUp) else 0.8
        self.scaleCanvas(event.xdata, event.ydata, scale_factor)
        return None

    @private
    def onMousePress(self, event):
        if event.inaxes:
            self._isDragging = True
            self._dragStart = event.xdata, event.ydata
        return None

    @private
    def onMouseMove(self, event) -> None:
        if event.inaxes is None:
            self._isDragging = False
            self.setMarkAnnotationsVisible(True)
            return None
        x, y = event.xdata, event.ydata
        if x is None:
            return None
        if self._isDragging:
            self.setMarkAnnotationsVisible(False)
            start_x, start_y = self._dragStart
            self.dragCanvas(x, y, start_x, start_y)
            self._dragStart = GTuple(start_x, start_y)
            return None
        if self._cursorOff:
            return None
        nearest = self.findNearestPoint(x, y, priority=self.priorityAuto, useThread=True)
        if not nearest:
            return None
        self.clearCursorAnnotation()
        curve_index, pos_nearest = nearest
        curve_name, color = self._yLabels[curve_index], self._annonationColors[curve_index]
        x_nearest, y_nearest = pos_nearest
        self._hline.set_visible(True)
        self._vline.set_visible(True)
        self._hline.set_ydata(GList(y_nearest, y_nearest))
        self._vline.set_xdata(GList(x_nearest, x_nearest))
        cursor_zorder = int(self._lineCount + self.cursorAboveOrder)
        self._hline.set_zorder(cursor_zorder)
        self._vline.set_zorder(cursor_zorder)
        self._annotation.xy = pos_nearest
        text = curve_name + RString.pLinefeed + self._annotationFrame(x_nearest, y_nearest)
        self._annotation.set_text(text)
        self._annotation.get_bbox_patch().set_facecolor(color)
        self._annotation.set_visible(True)
        self._fig.canvas.draw_idle()
        return None

    @private
    def onMouseRelease(self, event):
        if not event.inaxes:
            return None
        self._isDragging = False
        self.setMarkAnnotationsVisible(True)
        current_time = time.time()
        x, y = event.xdata, event.ydata
        if self._lastClick is not None:
            last_time, last_position = self._lastClick
            last_x, last_y = last_position
            if abs(last_time - current_time) < self.doubleClickTimeThreshold:
                dist = math.sqrt(math.pow(last_x - x, 2) + math.pow(last_y - y, 2))
                tolerance = self.doubleClickPositionToleranceRatio * min(self.axisScopeSpan())
                if dist < tolerance:
                    self.onDoubleClick(event)
        self._lastClick = time.time(), GTuple(x, y)
        return None

    @private
    def onDoubleClick(self, event):
        if event.inaxes is None:
            return None
        x, y = event.xdata, event.ydata
        nearest = self.findNearestPoint(x, y, limited=self._markLimit, priority=self.priorityAuto, useThread=True)
        if not nearest:
            return None
        curve_index, pos_nearest = nearest
        curve_name, color = self._yLabels[curve_index], self._annonationColors[curve_index]
        x_nearest, y_nearest = pos_nearest
        if self.removeCircleAnnotation(x_nearest, y_nearest):
            return None
        if len(self._markRecord) > self.maxMarkCount:
            return None
        circle_size = GTuple(0, 0)
        if not self.isCurvePinned(curve_index):
            circle_size = self.calcCircleEllipseSize()
        width, height = circle_size
        annot_zorder = int(self._lineCount + self.annotAboveOrder)
        circle: Ellipse = DataBox(patches.Ellipse(
            pos_nearest, width, height, color=color, zorder=annot_zorder,
            linewidth=self.defaultLineWidth, linestyle=self.defaultCurveStyle, fill=False
        )).data
        self._ax.add_patch(circle)
        annotation: Annotation = DataBox(self._ax.annotate(
            curve_name + RString.pLinefeed + self._annotationFrame(x_nearest, y_nearest),
            xy=pos_nearest, xytext=self.annotationOffset, textcoords=self.annotationOffsetMeasure,
            arrowprops=self.annotationArraw, bbox=MultiAxisPlotter.annotationBBox(self._annotationAlpha),
            fontproperties=self._fontProp
        )).data
        annotation.get_bbox_patch().set_facecolor(color)
        self._annotationMarks[curve_index].append(GTuple(circle, annotation))
        self._markRecord.append(GTuple(circle, annotation))
        self._fig.canvas.draw_idle()
        return None

    @private
    def removeCircleAnnotation(self, x: float, y: float):
        for i in range(self._lineCount):
            for circle, annotation in self._annotationMarks[i]:
                if circle.center in GIters(GTuple(x, y)):
                    circle.remove()
                    annotation.remove()
                    self._annotationMarks[i].remove(GTuple(circle, annotation))
                    self._markRecord.remove(GTuple(circle, annotation))
                    self._fig.canvas.draw_idle()
                    return True
        return False

    @private
    def drawCrossCursor(self):
        self._vline: Line2D = DataBox(self._ax.axvline(
            x=float(0), color=self._cursorColor, alpha=self._cursorAlpha,
            linewidth=self.defaultCursorWidth, linestyle=self._cursorStyle
        )).data
        self._hline: Line2D = DataBox(self._ax.axhline(
            y=float(0), color=self._cursorColor, alpha=self._cursorAlpha,
            linewidth=self.defaultCursorWidth, linestyle=self._cursorStyle
        )).data
        self._vline.set_visible(False)
        self._hline.set_visible(False)
        return None

    @private
    def fixDataSequence(self):
        for i, key in enumerate(self._yDatas.keys()):
            valid_len = min(len(self._xAxis[i]), len(self._yDatas[key]))
            self._xAxis[i] = self._xAxis[i][:valid_len]
            self._yDatas[key] = self._yDatas[key][:valid_len]
        return None

    @private
    def fixMaterials(self):
        dif = self._lineCount - len(self._lineColors)
        self._lineColors += ReferList(range(max(dif, 0)), lambda i: RColor().randomColor())
        fixLength = lambda a0: max(self._lineCount - len(a0), 0)
        self._lineWidths += RepeatList(self.defaultLineWidth, fixLength(self._lineWidths))
        self._lineStyles += RepeatList(self.defaultCurveStyle, fixLength(self._lineStyles))
        self._pinnerSizes += RepeatList(self.defaultPinnerSize, fixLength(self._pinnerSizes))
        self._pinnerStyles += RepeatList(self.defaultPinnerStyle, fixLength(self._pinnerStyles))
        self._annonationColors += self._lineColors[len(self._annonationColors):]
        self._yLabels += list(self._yDatas.keys())[len(self._yLabels):]
        return None
