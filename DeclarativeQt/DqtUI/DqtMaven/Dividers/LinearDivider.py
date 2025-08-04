from PyQt5.QtCore import QSize

from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtUI.DqtWidgets.Control import Label
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key


def VerticalDivider(
        length: int = int(40),
        fixedLength: int = None,
        lineWidth: int = int(1),
        color: str = RColor.hexLightGrey
) -> Label:
    style = DqtStyle(
        appendix=DictData(
            Key(DqtStyle.atBackgroundColor).Val(color)
        ).data,
        selector=DqtStyle.QLabel
    ).style
    return Label(
        size=QSize(lineWidth, length),
        fixedWidth=lineWidth,
        style=style
    ) if not fixedLength else Label(
        fixedHeight=fixedLength,
        fixedWidth=lineWidth,
        style=style
    )


def HorizontalDivider(
        length: int = int(40),
        fixedLength: int = None,
        lineWidth: int = int(1),
        color: str = RColor.hexLightGrey
) -> Label:
    style = DqtStyle(
        appendix=DictData(
            Key(DqtStyle.atBackgroundColor).Val(color)
        ).data,
        selector=DqtStyle.QLabel
    ).style
    return Label(
        size=QSize(length, lineWidth),
        fixedHeight=lineWidth,
        style=style
    ) if not fixedLength else Label(
        fixedWidth=fixedLength,
        fixedHeight=lineWidth,
        style=style
    )
