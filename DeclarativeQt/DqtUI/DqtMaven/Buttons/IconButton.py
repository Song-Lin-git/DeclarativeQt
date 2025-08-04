from typing import Callable, Dict, List

from PyQt5.QtCore import QSize, QSizeF, Qt
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, Run, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import BorderedButton, ButtonStyle
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate


class IconButton(BorderedButton):
    DefaultIconSizeRatio = QSizeF(0.8, 0.8)

    def __init__(
            self,
            size: QSize = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            text: RState[str] = None,
            icon: RState[QPixmap] = None,
            iconSizeRatio: QSizeF = None,
            parent: QWidget = None,
            onClick: Callable = None,
            enable: RState[bool] = True,
            fixedAspectRatio: float = None,
            fixedRadiusRatio: float = None,
            shortCut: QKeySequence = None,
            shortCuts: List[QKeySequence] = None,
            triggers: Dict[Remember, Callable] = None,
            styleEditor: ButtonStyle = None
    ):
        super().__init__(
            size=size,
            text=text,
            fixedWidth=fixedWidth,
            fixedHeight=fixedHeight,
            parent=parent,
            onClick=onClick,
            enable=enable,
            fixedAspectRatio=fixedAspectRatio,
            fixedRadiusRatio=fixedRadiusRatio,
            triggers=triggers,
            shortCut=shortCut,
            shortCuts=shortCuts,
            styleEditor=styleEditor
        )
        self.setFocusPolicy(Qt.ClickFocus)
        self._icon = icon
        self._iconRatio = Validate(iconSizeRatio, self.DefaultIconSizeRatio)
        self.setIcon(self._icon)
        if isinstance(self._icon, Remember):
            self._icon.connect(lambda value: Run(self.setIcon(QIcon(value)), self.resizeIcon()), host=self)

    @private
    def resizeIcon(self):
        if self._icon:
            icon = Remember.getValue(self._icon)
            self.setIconSize(DqtCanvas.scaleIconSize(icon, self.size(), self._iconRatio))
        return None

    def setIcon(self, icon):
        if icon is None:
            return None
        super().setIcon(QIcon(Remember.getValue(icon)))
        return None

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.resizeIcon()
        return None
