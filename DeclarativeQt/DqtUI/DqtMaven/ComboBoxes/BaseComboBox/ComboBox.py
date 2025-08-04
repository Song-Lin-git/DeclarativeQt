from functools import partial
from typing import Callable, Dict, List, Optional

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QComboBox

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Strings.RString import RString

ComboBoxModel = RState[List[str]]


class ComboBox(QComboBox):
    DefaultSize: QSize = QSize(180, 30)
    DefaultPlaceholder: str = RString.pNull + RString.pBlank + RString.bracket(RString.pFalse, RString.EnglishIndex)
    PlaceholdAt: int = int(0)

    def __init__(
            self,
            size: QSize = None,
            dataModel: ComboBoxModel = None,
            fixedHeight: int = None,
            selection: RState[str] = None,
            style: RState[str] = None,
            parent: QWidget = None,
            wheelEnable: RState[bool] = False,
            wheelCycle: RState[bool] = True,
            onSelected: Callable = None,
            placeholder: str = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__()
        size = Validate(size, QSize(self.DefaultSize))
        self._wheelEnable = wheelEnable
        self._wheelCycle = wheelCycle
        self._fixedHeight = None if not fixedHeight else max(fixedHeight, DqtCanvasBase.MinHeight)
        if self._fixedHeight:
            size.setHeight(self._fixedHeight)
        self.setFixedSize(size)
        self.setParent(parent)
        self._placeholder = Validate(placeholder, self.DefaultPlaceholder)
        self._selection = ValToRemember(selection)
        if isinstance(self._selection, Remember):
            self._selection.connect(lambda value: self.setCurrentText(value), host=self)
            # noinspection PyUnresolvedReferences
            self.activated.connect(lambda: self._selection.setValue(self.currentItem()))
        self._dataModel = Validate(dataModel, list())
        self.setItems(self._dataModel)
        if isinstance(self._dataModel, Remember):
            self._dataModel.connect(lambda value: self.setItems(value), host=self)
        self.setStyleSheet(Validate(style, DqtStyle.emptyStyle(DqtStyle.QComboBox)))
        if isinstance(style, Remember):
            style.connect(lambda value: self.setStyleSheet(value), host=self)
        # noinspection PyUnresolvedReferences
        self.activated.connect(partial(Validate(onSelected, lambda: None)))
        triggers = Validate(triggers, dict())
        for k, v in triggers.items():
            k.connect(partial(v), host=self)

    def wheelEvent(self, e):
        if not Remember.getValue(self._wheelEnable):
            e.ignore()
            return None
        if not Remember.getValue(self._wheelCycle):
            super().wheelEvent(e)
            return None
        factor = int(-1) if e.angleDelta().y() > 0 else int(+1)
        index = int(self.currentIndex() + factor) % self.count()
        self.setCurrentIndex(index)
        self.activated.emit(index)
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        DqtCanvas.setFixedHeight(self, self._fixedHeight)
        return None

    def currentItem(self) -> Optional[str]:
        if self.currentIndex() <= 0:
            return None
        return super().currentText()

    def setCurrentText(self, text: RState[str]):
        text = Remember.getValue(text)
        if text is None or text not in Remember.getValue(self._dataModel):
            self.setCurrentIndex(self.PlaceholdAt)
            return None
        super().setCurrentText(text)
        return None

    def setStyleSheet(self, styleSheet: RState[str]):
        super().setStyleSheet(Remember.getValue(styleSheet))
        return None

    def setItems(self, texts: ComboBoxModel):
        self.clear()
        self.addItem(self._placeholder)
        for item in Remember.getValue(texts):
            self.addItem(item)
        self.setCurrentText(self._selection)
        if self.currentIndex() <= 0:
            self._selection.setValue(None)
        return None

    def addItems(self, texts: ComboBoxModel):
        super().addItems(list(set(Remember.getValue(texts))))
        return None
