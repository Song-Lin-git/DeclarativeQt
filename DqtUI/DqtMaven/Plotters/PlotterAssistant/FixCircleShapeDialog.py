from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtWidgets import QWidget
from matplotlib import patches
from matplotlib.patches import Ellipse

from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import RState, SmticToState
from DeclarativeQt.DqtUI.DqtMaven.Plotters.BasePlotter.MultiAxisPlotter import MultiAxisPlotter
from DeclarativeQt.DqtUI.DqtMaven.Plotters.PlotterAssistant.PlotterDialog.PlotterDialog import PlotterDialog
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, GTuple, Equal, DataBox, GList
from DeclarativeQt.Resource.Strings.RStr import NLIndex, RStr


class FixCircleShapeDialog(PlotterDialog):
    WheelStepRate: float = 1.01
    CircleSizeRatio = 1 / 1.8

    def __init__(
            self,
            drivePlotter: MultiAxisPlotter,
            parent: QWidget = None,
            dialogOffset: QPoint = None,
            size: QSize = None,
            language: RState[NLIndex] = None,
            circleColor: str = None,
    ):
        language = Validate(language, RStr.EN)
        self._ax, self._fig, self._plotter = drivePlotter.plotterCopy(aspectMode=MultiAxisPlotter.aspectEqual)
        self._circleSample: Ellipse = DataBox(patches.Ellipse(
            GTuple(0, 0), float(0), float(0), color=Validate(circleColor, RColor.hexMidnightNavy),
            linewidth=drivePlotter.defaultLineWidth, linestyle=drivePlotter.defaultCurveStyle, fill=False
        )).data
        self._circleCompare: Ellipse = DataBox(patches.Ellipse(
            GTuple(0, 0), float(0), float(0), color=RColor.hexCloudTouch, fill=False, alpha=0.8,
            linewidth=drivePlotter.defaultLineWidth, linestyle=drivePlotter.defaultCursorStyle
        )).data
        self._canvasSpan = None
        self._aspectRatio = None
        self._ax.add_patch(self._circleCompare)
        self._ax.add_patch(self._circleSample)
        self._drivePlotter = drivePlotter
        super().__init__(
            size=Validate(size, Dialog.DefaultSize),
            parent=parent,
            offset=dialogOffset,
            figures=GList(self._fig),
            title=SmticToState(language, RStr.R.stCircleMarker),
            content=self._plotter
        )
        self.buildCanvas()
        self.resizeCircle()
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(MultiAxisPlotter.mouseScrollEvent, self.onWheelScroll)
        # noinspection PyTypeChecker
        self._fig.canvas.mpl_connect(MultiAxisPlotter.canvasResizeEvent, self.onCanvasResize)

    def buildCanvas(self):
        x_lim, y_lim = self._ax.get_xlim(), self._ax.get_ylim()
        center = float(sum(x_lim) / 2), float(sum(y_lim) / 2)
        lim_span = lambda lim: lim[1] - lim[0]
        self._circleSample.center = center
        x_span, y_span = lim_span(x_lim), lim_span(y_lim)
        self._canvasSpan = GTuple(x_span, y_span)
        if not self._aspectRatio:
            self._aspectRatio = x_span / y_span
        return None

    def resizeCircle(self):
        width, height = self._drivePlotter.sampleCircleSize(aspectRatio=self._aspectRatio)
        x_span, y_span = self._canvasSpan
        boost_ratio = min(x_span, y_span) / max(width, height) * self.CircleSizeRatio
        self._circleSample.width = width * boost_ratio
        self._circleSample.height = height * boost_ratio
        self.updateCircleCompare()
        self._fig.canvas.draw_idle()
        return None

    def updateCircleCompare(self):
        self._circleCompare.center = self._circleSample.center
        radius = max(self._circleSample.width, self._circleSample.height)
        self._circleCompare.width = radius
        self._circleCompare.height = radius
        self._fig.canvas.draw_idle()
        return None

    def onCanvasResize(self, event):
        if event is not None:
            self.buildCanvas()
            self.resizeCircle()
        return None

    def onWheelScroll(self, event):
        if Equal(event.button, MultiAxisPlotter.scrollUp):
            self._drivePlotter.scaleCircleFixRatio(self.WheelStepRate)
        else:
            self._drivePlotter.scaleCircleFixRatio(1.0 / self.WheelStepRate)
        self.resizeCircle()
        return None

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() in GTuple(Qt.Key_Enter, Qt.Key_Return):
            self.accept()
        elif a0.key() in GTuple(Qt.Key_Escape):
            self.reject()
        return None
