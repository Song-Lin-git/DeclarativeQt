from typing import Iterable, List, Callable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas.DqtCanvas import DqtCanvasBase
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.BoxLayout import BoxLayout
from DeclarativeQt.DqtUI.DqtLayouts.BaseLayouts.LinearLayout import LinearLayout


class Box(BoxLayout):
    def __init__(
            self,
            size: QSize = None,
            options: Iterable = None,
            contentPaddingRatio: float = DqtCanvasBase.DefaultWidgetPaddingRatio,
            fixedAspectRatio: float = None,
            parent: QWidget = None,
            style: RState[str] = None,
            content: RState[QWidget] = None,
            destroyPrevious: bool = False,
            autoContentResize: bool = False,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__(
            size=size,
            options=options,
            contentPaddingRatio=contentPaddingRatio,
            fixedAspectRatio=fixedAspectRatio,
            parent=parent,
            style=style,
            content=content,
            autoContentResize=autoContentResize,
            destroyPrevious=destroyPrevious,
            triggers=triggers
        )


class Row(LinearLayout):
    def __init__(
            self,
            size: QSize = None,
            options: Iterable = None,
            alignment: int = LinearLayout.Align.VCenter,
            arrangement: int = LinearLayout.Align.HCenter,
            spacing: int = None,
            padding: int = None,
            fixWidth: bool = False,
            fixHeight: bool = False,
            verticalPadding: int = None,
            autoUniformDistribute: bool = False,
            autoExpandContentAt: int = None,
            autoExpandToMaxCross: List[int] = None,
            style: RState[str] = None,
            content: List[QWidget] = None,
            autoContentResize: bool = False,
    ):
        super().__init__(
            size=size,
            alignment=alignment,
            spacing=spacing,
            style=style,
            options=options,
            autoUniformDistribute=autoUniformDistribute,
            arrangement=arrangement,
            linePadding=padding,
            crossPadding=verticalPadding,
            autoExpandContentAt=autoExpandContentAt,
            autoExpandToMaxCross=autoExpandToMaxCross,
            fixWidth=fixWidth,
            fixHeight=fixHeight,
            content=content,
            autoContentResize=autoContentResize,
            direction=LinearLayout.Horizontal
        )


class Column(LinearLayout):
    def __init__(
            self,
            size: QSize = None,
            options: Iterable = None,
            alignment: int = LinearLayout.Align.HCenter,
            arrangement: int = LinearLayout.Align.VCenter,
            spacing: int = None,
            padding: int = None,
            fixWidth: bool = False,
            fixHeight: bool = False,
            horizontalPadding: int = None,
            autoUniformDistribute: bool = False,
            autoExpandToMaxCross: List[int] = None,
            autoExpandContentAt: int = None,
            style: RState[str] = None,
            content: List[QWidget] = None,
            autoContentResize: bool = False,
    ):
        super().__init__(
            size=size,
            alignment=alignment,
            spacing=spacing,
            style=style,
            options=options,
            autoUniformDistribute=autoUniformDistribute,
            arrangement=arrangement,
            linePadding=padding,
            crossPadding=horizontalPadding,
            autoExpandContentAt=autoExpandContentAt,
            autoExpandToMaxCross=autoExpandToMaxCross,
            fixWidth=fixWidth,
            fixHeight=fixHeight,
            content=content,
            autoContentResize=autoContentResize,
            direction=LinearLayout.Vertical
        )
