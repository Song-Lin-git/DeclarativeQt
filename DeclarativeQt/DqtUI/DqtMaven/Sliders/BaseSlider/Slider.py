from functools import partial
from typing import Callable, Dict

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QSlider, QWidget, QStyle, QStyleOptionSlider

from DeclarativeQt.DqtCore.DqtBase import RState, Remember, Run
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, NxLimitVal, Equal, DataBox, isValid


class Slider(QSlider):
    Horizontal = Qt.Horizontal
    Vertical = Qt.Vertical
    DefaultSize = QSize(240, 30)
    DefaultPercision = int(100)
    MinPercision = int(5)

    def __init__(
            self,
            size: QSize = None,
            parent: QWidget = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            direction: int = Horizontal,
            data: RState[float] = None,
            percision: int = None,
            maxVal: float = None,
            minVal: float = None,
            onValueChange: Callable = None,
            style: RState[str] = None,
            triggers: Dict[Remember, Callable] = None,
    ):
        super().__init__()
        defaultSize = QSize(self.DefaultSize)
        if Equal(direction, self.Vertical):
            defaultSize = QSize(self.DefaultSize.height(), self.DefaultSize.width())
        size = Validate(size, defaultSize)
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        self._fixedWidth = None if not fixedWidth else max(fixedWidth, DqtCanvasBase.MinWidth)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        if self._fixedWidth:
            size.setWidth(self._fixedWidth)
        self.setFixedSize(size)
        self.setParent(parent)
        self.setOrientation(Qt.Orientation(direction))
        self._maxVal = Validate(maxVal, 1.0)
        self._minVal = Validate(minVal, 0.0)
        self._percision = Validate(percision, self.DefaultPercision)
        self.ensureSafety()
        self.setMaximum(self._percision)
        self.setMinimum(0)
        data = Remember.toValid(data, self._minVal)
        self.setValue(data)
        self.setPageStep(0)
        onValueChange = Validate(onValueChange, lambda: None)
        if isinstance(data, Remember):
            data.connect(lambda value: self.setValue(value), host=self)
            self.valueChanged.connect(lambda: Run(data.setValue(self.value()), onValueChange()))
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        self.setStyleSheet(style)
        triggers = Validate(triggers, dict())
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def setStyleSheet(self, a0: RState[str]):
        style = Remember.getValue(a0)
        if isValid(style):
            super().setStyleSheet(style)
        return None

    def ensureSafety(self):
        self._percision = max(self._percision, self.MinPercision)
        self._minVal = min(self._maxVal, self._minVal)
        self._maxVal = max(self._maxVal, self._minVal)
        if Equal(self._minVal, self._maxVal):
            self._maxVal += 1.0
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        DqtCanvas.setFixedWidth(self, self._fixedWidth)
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        return None

    def value(self) -> float:
        v0 = super().value()
        return v0 * float(self._maxVal - self._minVal) / self._percision + self._minVal

    def setValue(self, a0: RState[float]):
        a0 = Remember.getValue(a0)
        a0 = NxLimitVal(a0, self._minVal, self._maxVal)
        v0 = self._percision * float(a0 - self._minVal) / float(self._maxVal - self._minVal)
        if v0 != super().value():
            super().setValue(int(v0))
        return None

    def mousePressEvent(self, ev):
        if Equal(ev.button(), Qt.LeftButton):
            style = self.style()
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            groove = style.subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
            handle = style.subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
            if Equal(self.orientation(), Qt.Horizontal):
                slider_min = groove.x()
                slider_max = groove.right() - handle.width() + 1
                pos = ev.pos().x() - int(handle.width() / 2.0)
            else:
                slider_min = groove.y()
                slider_max = groove.bottom() - handle.height() + 1
                pos = ev.pos().y() - int(handle.height() / 2.0)
            pos, span = int(pos - slider_min), int(slider_max - slider_min)
            v0 = DataBox(QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), pos, span,
                upsideDown=Equal(self.orientation(), self.Vertical)
            )).data
            super().setValue(v0)
        super().mousePressEvent(ev)
        return None

    def initStyleOption(self, opt: QStyleOptionSlider) -> None:
        super().initStyleOption(opt)
        return None
