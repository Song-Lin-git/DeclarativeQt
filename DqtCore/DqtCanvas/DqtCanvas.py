import textwrap
from typing import Callable, List, Union, Optional, Tuple

from PyQt5.QtCore import QSize, QPoint, QSizeF
from PyQt5.QtGui import QPixmap, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from DeclarativeQt.DqtCore.DqtBase import Remember
from DeclarativeQt.DqtCore.DqtCanvas.DqtAlign import DqtAlign
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import RState
from DeclarativeQt.Resource.Grammars.RGrammar import RepeatList, ReferList, DataBox, JoinLists, GList, \
    SumNestedList, Validate, LimitVal, isEmpty
from DeclarativeQt.Resource.Images.RImage import RImage
from DeclarativeQt.Resource.Strings.RString import RString


class DqtCanvasBase:
    MinWidth, MinHeight = int(0), int(0)
    MinAspectRatio = 0.001
    MinPaddingRatio = 0.001
    DefaultLayoutSpacingRatio = 0.01
    DefaultWidgetPaddingRatio = 0.01
    DefaultRemainRatio = 1.00
    NoRemainRatio = 1.00
    LayoutRemainRatio = 1.04


def setWindowOffset(body: QWidget, offset: QPoint, anchor: QWidget = None):
    if offset is None:
        return None
    desktop = QDesktopWidget().availableGeometry()
    if not anchor:
        frameGeo = body.frameGeometry()
        frameGeo.moveCenter(desktop.center())
        loc = frameGeo.topLeft()
    else:
        loc = anchor.mapToGlobal(QPoint(0, 0))
    loc = QPoint(loc.x() + offset.x(), loc.y() + offset.y())
    x = LimitVal(loc.x(), desktop.left(), desktop.right() - body.width())
    y = LimitVal(loc.y(), desktop.top(), desktop.bottom() - body.height())
    body.move(QPoint(x, y))
    return None


def fontTextMetric(font: QFont, text: RState[str], lineLim: int = None) -> QSize:
    metrics = QFontMetrics(font)
    height = metrics.height()
    lines = list()
    for line in Remember.getValue(text).split(RString.pLinefeed):
        if lineLim:
            lines += textwrap.wrap(line, width=lineLim)
        else:
            lines.append(line)
    if isEmpty(lines):
        return QSize(int(1), height)
    maxWidth = max(ReferList(lines, lambda a0: metrics.horizontalAdvance(a0)))
    if isinstance(text, Remember):
        text.setValue(RString.pLinefeed.join(lines))
    return QSize(maxWidth, height)


def rectAspect(rect: Union[QSize, QSizeF, Tuple]) -> Optional[float]:
    if rect is None:
        return None
    if isinstance(rect, Tuple):
        if len(rect) < int(2):
            return None
        rect = QSizeF(rect[0], rect[1])
    return rect.width() / rect.height()


def fillLimitBox(aspectRatio: float, limitBox: QSize):
    box_aspect = limitBox.width() / limitBox.height()
    if aspectRatio < box_aspect:
        return QSize(int(limitBox.height() * aspectRatio), limitBox.height())
    return QSize(limitBox.width(), int(limitBox.width() / aspectRatio))


def scaleIconSize(icon: QPixmap, boxSize: QSize, limitRatio: QSizeF):
    width, height = icon.width(), icon.height()
    scale_ratio = RImage.limitImageToBox(QSizeF(width / boxSize.width(), height / boxSize.height()), limitRatio)
    return QSize(int(scale_ratio.width() * boxSize.width()), int(scale_ratio.height() * boxSize.height()))


def placeCentralContent(canvas: QWidget, content: QWidget):
    content.move(int((canvas.width() - content.width()) / 2), int((canvas.height() - content.height()) / 2))
    return None


def scaleSingleContentCanvas(
        content: QWidget, paddingRatio: float, remainRatio: float = None
) -> QSize:
    remainRatio = Validate(remainRatio, DqtCanvasBase.DefaultRemainRatio)
    expand = 1.0 * remainRatio / float(1 - 2 * paddingRatio)
    return QSize(int(content.width() * expand), int(content.height() * expand))


def resizeCentralContent(canvas: QWidget, content: QWidget, paddingRatio: float):
    paddingRatio = max(DqtCanvasBase.MinPaddingRatio, paddingRatio)
    content_ratio = 1.0 - 2 * paddingRatio
    content.setFixedSize(int(content_ratio * canvas.width()), int(content_ratio * canvas.height()))
    return None


def setFixedWidth(canvas: QWidget, fixedWidth: int = None):
    setFixedWidgetSize(canvas, fixedWidth=fixedWidth)
    return None


def setFixedHeight(canvas: QWidget, fixedHeight: int = None):
    setFixedWidgetSize(canvas, fixedHeight=fixedHeight)
    return None


def setFixedWidgetSize(canvas: QWidget, fixedWidth: int = None, fixedHeight: int = None):
    if fixedWidth is not None and canvas.width() != fixedWidth:
        canvas.setFixedSize(max(DqtCanvasBase.MinWidth, fixedWidth), canvas.height())
    if fixedHeight is not None and canvas.height() != fixedHeight:
        canvas.setFixedSize(canvas.width(), max(DqtCanvasBase.MinHeight, fixedHeight))
    return None


def scaleCanvasAspect(canvas: QWidget, aspectRatio: float = None):
    if aspectRatio is None:
        return None
    aspectRatio = max(aspectRatio, DqtCanvasBase.MinAspectRatio)
    scaled_size = None
    scaled_width = int(aspectRatio * canvas.height())
    scaled_height = int(canvas.width() / aspectRatio)
    if canvas.width() > scaled_width:
        scaled_size = QSize(scaled_width, canvas.height())
    elif canvas.width() < scaled_width:
        scaled_size = QSize(canvas.width(), scaled_height)
    if scaled_size:
        canvas.setFixedSize(scaled_size)
    return None


def linearContentLayout(
        canvas: QWidget, contents: List[QWidget], isHorizontal: bool, arrangement: int,
        alignment: int, spacing: int, linePadding: int, crossPadding: int, uniformDistribute: bool,
) -> None:
    content_count = len(contents)
    if content_count <= 0:
        return None
    if isHorizontal:
        canvas_line: int = canvas.width()
        content_lines: list = ReferList(contents, lambda x: x.width())
        canvas_cross: int = canvas.height()
        content_crosses: list = ReferList(contents, lambda x: x.height())
    else:
        canvas_line: int = canvas.height()
        content_lines: list = ReferList(contents, lambda x: x.height())
        canvas_cross: int = canvas.width()
        content_crosses: list = ReferList(contents, lambda x: x.width())
    contentPosition = DataBox(calcLinearLayoutContentPosition(
        canvas_line, content_lines, canvas_cross, content_crosses,
        spacing=spacing, linePadding=linePadding, crossPadding=crossPadding,
        arrangement=arrangement, alignment=alignment, uniformDistribute=uniformDistribute
    )).data
    for i, ct in enumerate(contents):
        pos = contentPosition[i]
        if not isHorizontal:
            pos = QPoint(pos.y(), pos.x())
        ct.move(pos)
    return None


def calcUniformDistribute(space: int, items: int):
    base = space // items
    rest = space % items
    if not rest:
        return RepeatList(base, items)
    if rest >= items - rest:
        l_count, r_count = rest, items - rest
        l_value, r_value = base + 1, base
    else:
        l_count, r_count = items - rest, rest
        l_value, r_value = base, base + 1
    group_count = r_count + 1
    bt = l_count // group_count
    pt = l_count % group_count
    return SumNestedList(ReferList(range(group_count), lambda i: JoinLists(
        RepeatList(l_value, bt + 1 if i < pt else bt), GList(r_value)
    )))[:-1]


def calcLinearLayoutContentPosition(
        canvasLine: int, contentLines: list, canvasCross: int, contentCrosses: list,
        spacing: int, linePadding: int, crossPadding: int,
        arrangement: int, alignment: int, uniformDistribute: bool,
) -> List:
    content_count = len(contentLines)
    spacing_count = content_count - 1
    total_taken = int(sum(contentLines) + linePadding * 2 + spacing * spacing_count)
    crossPosition: Callable = lambda idx: crossPadding if alignment in DqtAlign.Front else DataBox(
        int(canvasCross - contentCrosses[idx] - crossPadding) if alignment in DqtAlign.Back
        else int(1.0 * (canvasCross - contentCrosses[idx]) / 2)
    ).data
    line_blank = canvasLine - sum(contentLines)
    if uniformDistribute and content_count > 1 and total_taken < canvasLine:
        content_spacings: list = calcUniformDistribute(line_blank - 2 * linePadding, spacing_count)
        front_padding: int = linePadding
    else:
        content_spacings: list = RepeatList(spacing, spacing_count)
        front_padding: int = linePadding if arrangement in DqtAlign.Front else DataBox(
            int(line_blank - spacing * spacing_count - linePadding) if arrangement in DqtAlign.Back
            else int(1.0 * (line_blank - spacing * spacing_count) / 2)
        ).data
        if uniformDistribute and content_count <= 1:
            front_padding: int = int(line_blank / 2)
    linePosition: Callable = lambda idx: int(front_padding + sum(contentLines[:idx]) + sum(content_spacings[:idx]))
    contentPosition: Callable = lambda idx: QPoint(linePosition(idx), crossPosition(idx))
    return ReferList(range(content_count), contentPosition)
