from functools import partial
from typing import Callable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QCheckBox

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.Resource.Grammars.RGrammar import Validate


class CheckBox(QCheckBox):
    DefaultSize: QSize = QSize(180, 30)

    def __init__(
            self,
            size: QSize = None,
            fixedHeight: int = None,
            description: RState[str] = None,
            checked: RState[bool] = False,
            style: RState[str] = None,
            parent: QWidget = None,
            onValueChange: Callable = None,
            onClick: Callable = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__()
        size = Validate(size, QSize(self.DefaultSize))
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        self.setFixedSize(size)
        self.setParent(parent)
        self.setText(description)
        if isinstance(description, Remember):
            description.connect(lambda value: self.setText(value), host=self)
        self.setChecked(checked)
        if isinstance(checked, Remember):
            checked.connect(lambda value: self.setChecked(value), host=self)
            checked.connect(partial(Validate(onValueChange, lambda: None)), host=self)
            # noinspection PyUnresolvedReferences
            self.clicked.connect(lambda: checked.setValue(self.isChecked()))
        style = Validate(style, DqtStyle.emptyStyle(DqtStyle.QCheckBox))
        self.setStyleSheet(style)
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        if onClick:
            # noinspection PyUnresolvedReferences
            self.clicked.connect(partial(onClick))
        triggers = Validate(triggers, dict())
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        return None

    def setStyleSheet(self, styleSheet):
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None

    def setChecked(self, a0):
        checked = Remember.getValue(a0)
        if self.isChecked() != checked:
            super().setChecked(checked)
        return None

    def setText(self, text):
        super().setText(Remember.getValue(text))
        return None
