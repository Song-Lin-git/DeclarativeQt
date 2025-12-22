from typing import Callable, Dict

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtUI.DqtMaven.Labels.BaseLabel.Label import Label
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Images.RIcon import RIcon, IconName


class PixmapLabel(Label):
    DefaultSize: QSize = QSize(200, 160)
    PlaceholderSize: QSize = QSize(40, 40)
    Placeholder: IconName = RIcon.R.broken_image

    def __init__(
            self,
            size: QSize = None,
            pixmap: RState[QPixmap] = None,
            placeholder: QPixmap = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            style: RState[str] = None,
            parent: QWidget = None,
            onClick: Callable = None,
            alignment: RState[int] = None,
            hoverTip: RState[bool] = False,
            tipText: RState[str] = None,
            triggers: Dict[Remember, Callable] = None,
            enable: RState[bool] = True,
    ):
        super().__init__(
            size=size,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            style=style,
            parent=parent,
            onClick=onClick,
            alignment=Validate(alignment, Label.Align.Center),
            hoverTip=hoverTip,
            triggers=triggers,
            enable=enable,
            tipText=tipText
        )
        self.setScaledContents(False)
        self._pixmap = pixmap
        self._placeholder = Validate(placeholder, self.Placeholder)
        if isinstance(self._pixmap, Remember):
            self._pixmap.connect(lambda value: self.setPixmap(value), host=self)
        self.setPixmap(self._pixmap)

    def setPixmap(self, a0: RState[QPixmap]):
        pixmap = Remember.getValue(a0)
        if not isinstance(pixmap, QPixmap):
            placeholder = RIcon.loadIconPixmap(self._placeholder)
            placeholder = placeholder.scaled(self.PlaceholderSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            super().setPixmap(placeholder)
            return None
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super().setPixmap(pixmap)
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.setPixmap(self._pixmap)
        return None
