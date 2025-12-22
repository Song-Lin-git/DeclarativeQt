from functools import partial
from typing import Iterable, Optional, Union, Callable

from PyQt5.QtCore import QModelIndex, Qt, QRect, QObject, QPoint, QEvent, QTimer
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QFont, QPixmap
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem, QCompleter, QLineEdit, QListView, \
    QApplication

from DeclarativeQt.DqtCore.DqtBase import RState, Remember
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtTools.Scroller import ScrollerStyle
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate, ReferList, Equal, ExecMethod
from DeclarativeQt.Resource.Images.RIcon import RIcon


class CompleterStyle(DqtStyleEditor):
    borderWidth = "borderWidth"
    borderColor = "borderColor"
    borderStyle = "borderStyle"

    def __init__(
            self,
            borderWidth: RState[int] = None,
            borderStyle: RState[str] = None,
            borderColor: RState[str] = None,
            backgroundColor: RState[str] = None,
            scrollerStyle: ScrollerStyle = None,
    ):
        defaultBorderColor = RColor.setQStyleAlpha(RColor.hexNightSkyBlue, 0.6)
        self._styles = DictData(
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, RColor.hexIceBlue)),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.borderColor).Val(Remember.toValid(borderColor, defaultBorderColor)),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
            Key(DqtStyle.atBorderRadius).Val(int(0))
        ).data
        self._scrollerStyle = Validate(scrollerStyle, ScrollerStyle(
            scrollHandleBackground=RColor.hexMistBlue,
            scrollHandleHoverBackground=RColor.hexTealGrey,
            scrollHandlePressedBackground=RColor.hexDeepStoneBlue
        ))
        super(CompleterStyle, self).__init__(self._styles)

    def getStyleSheet(self) -> str:
        return DqtStyle(
            appendix=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor),
                )),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius)))
            ).data,
            selector=DqtStyle.QListView
        ).mergeStyle(
            styleSheet=self._scrollerStyle.getStyleSheet()
        ).style


class MatchSubstrDelegate(QStyledItemDelegate):
    DefaultStrictMatchColor = QColor(173, 216, 230, int(255 * 0.63))
    DefaultLooseMatchColor = QColor(196, 238, 144, int(255 * 0.83))
    DefaultCompleterFont = QFont(RFont.YaHei, RFont.fzTinySize)
    DefaultItemSpacing = int(10)
    DefaultItemPadding = int(8)
    TextDrawRectRemainRatio = 1.28
    MouseHoverColor = QColor(230, 230, 230, int(255 * 0.8))
    KeyboardAtColor = QColor(210, 210, 210, int(255 * 0.8))

    def __init__(
            self,
            parent: QObject = None,
            lineEdit: QLineEdit = None,
            completerFont: QFont = None,
            textColor: str = None,
            strictMatchColor: QColor = None,
            looseMatchColor: QColor = None,
            itemSpacing: int = None,
            itemPadding: int = None,
            itemIcon: QPixmap = None,
            iconSizeRatio: float = 0.72
    ):
        super().__init__(parent)
        self.lineEdit = lineEdit
        self.font = Validate(completerFont, self.DefaultCompleterFont)
        self.textColor = Validate(textColor, RColor.hexBlack)
        self.strictMatchColor = Validate(strictMatchColor, self.DefaultStrictMatchColor)
        self.looseMatchColor = Validate(looseMatchColor, self.DefaultLooseMatchColor)
        self.spacing = Validate(itemSpacing, self.DefaultItemSpacing)
        self.padding = Validate(itemPadding, self.DefaultItemPadding)
        self.icon = Validate(itemIcon, RIcon().loadIconPixmap(RIcon.R.edit_square_mistgreen))
        self.iconSizeRatio = iconSizeRatio

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + self.spacing)
        return size

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        offsetRatio = 0.04
        color = RColor.hexCodeToQColor(RColor.hexWhite, 0.92)
        if not index.row() % 2:
            color.setAlphaF(color.alphaF() * 0.78)
        painter.fillRect(option.rect, color)
        default_color = Qt.transparent
        if option.state & QStyle.State_Selected:
            default_color = self.KeyboardAtColor
        if option.state & QStyle.State_MouseOver:
            default_color = self.MouseHoverColor
        painter.fillRect(option.rect, default_color)
        option.rect.setY(int(option.rect.y() + option.rect.height() * offsetRatio))
        option.rect.setHeight(int(option.rect.height() * float(1.0 - 2.1 * offsetRatio)))
        option.rect.setX(option.rect.x() + int(self.padding / 1.9))
        icon_size = int(option.rect.height() * self.iconSizeRatio)
        icon_at = QPoint(option.rect.x(), option.rect.y() + int((option.rect.height() - icon_size) / 1.02))
        painter.drawPixmap(icon_at.x(), icon_at.y(), icon_size, icon_size, self.icon)
        option.rect.setX(option.rect.x() + icon_size)
        option.rect.setX(option.rect.x() + int(self.padding / 1.08))
        option.rect.setWidth(int(option.rect.width() - 1.2 * self.padding))
        text = index.data(Qt.DisplayRole)
        input_text = self.lineEdit.text()
        match_start = text.lower().find(input_text.lower())
        match_end = match_start + len(input_text)
        font = self.font
        charWidth = lambda it: int(QFontMetrics(font).horizontalAdvance(it) * self.TextDrawRectRemainRatio)
        char_widths = ReferList(text, charWidth)
        matched_x = option.rect.x() + sum(char_widths[:match_start])
        matched_width = sum(char_widths[match_start:match_end])
        matched_area = QRect(matched_x, option.rect.y(), matched_width, option.rect.height())
        radius = min(char_widths) * 0.28
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.strictMatchColor)
        painter.drawRoundedRect(matched_area, radius, radius)
        painter.setFont(font)
        for i, item in enumerate(text):
            item_width = char_widths[i]
            paint_rect = QRect(option.rect.x(), option.rect.y(), item_width, option.rect.height())
            if match_start < 0 or bool(i < match_start or i >= match_end):
                painter.fillRect(paint_rect, default_color)
            elif input_text[i - match_start] != item:
                painter.fillRect(paint_rect, self.looseMatchColor)
            painter.setPen(QColor(self.textColor))
            paint_rect.setHeight(int(paint_rect.height() * 0.92))
            painter.drawText(paint_rect, Qt.AlignLeft | Qt.AlignBottom, item)
            option.rect.setX(option.rect.x() + item_width)
        painter.restore()
        return None


class CompleterShowEventFilter(QObject):
    CompleterVerticalRemain = int(10)
    CompleterMinMaxHeight = int(200)

    def __init__(self, parent: QLineEdit, offset: int = 0, onShow: Callable = None, onHide: Callable = None):
        super().__init__()
        self._parent = parent
        self._onShow = lambda: ExecMethod(onShow)
        self._onHide = lambda: ExecMethod(onHide)
        self._dY = offset
        self._stopWork = False
        # noinspection PyUnresolvedReferences
        self._parent.textEdited.connect(lambda: QTimer.singleShot(0, lambda: self.replaceCompleter(dY=self._dY)))
        self._parent.destroyed.connect(partial(self.onParentDestroy))

    def onParentDestroy(self):
        self._stopWork = True
        return None

    def replaceCompleter(self, dX: int = 0, dY: int = 0):
        if self._parent.completer() and self._parent.completer().popup().isVisible():
            screen_height = QApplication.primaryScreen().size().height()
            popup = self._parent.completer().popup()
            base_at = self._parent.mapToGlobal(QPoint(0, self._parent.height()))
            move_to = QPoint(base_at.x() + dX, base_at.y() + dY)
            max_height = screen_height - move_to.y() - self.CompleterVerticalRemain
            if max_height < self.CompleterMinMaxHeight:
                move_to.setX(base_at.x() + self._parent.width() + dX)
                move_to.setY(base_at.y() - popup.height() + dY)
            else:
                popup.setMaximumHeight(max_height)
            popup.move(move_to)
        return None

    def eventFilter(self, a0, a1):
        if self._stopWork or not self._parent.completer():
            return False
        popup = self._parent.completer().popup()
        if Equal(a0, popup):
            if Equal(a1.type(), QEvent.Hide):
                self._onHide()
            elif Equal(a1.type(), QEvent.Show):
                self._onShow()
                screen_height = QApplication.primaryScreen().size().height()
                popup.setMaximumHeight(screen_height)
                QTimer.singleShot(0, lambda: self.replaceCompleter(dY=self._dY))
        return super().eventFilter(a0, a1)


def buildCompleterForLineEdit(
        dataModel: Iterable[Optional[str]], lineEdit: QLineEdit,
        completerFilter: int = Qt.MatchContains, sensitivity: bool = False,
        styleEditor: CompleterStyle = None, completerFont: QFont = None,
        onCompleterShow: Callable = None, onCompleterHide: Callable = None
) -> Union[QCompleter, None]:
    if dataModel is None or lineEdit is None:
        return None
    completer = QCompleter(list(set(dataModel)))
    completer.setFilterMode(completerFilter)
    completer.setCaseSensitivity(Qt.CaseSensitive if sensitivity else Qt.CaseInsensitive)
    delegate = MatchSubstrDelegate(completer, lineEdit, completerFont)
    completer.popup().setItemDelegate(delegate)
    lineEdit.setCompleter(completer)
    viewer = lineEdit.completer().popup()
    showEvent = CompleterShowEventFilter(lineEdit, onShow=onCompleterShow, onHide=onCompleterHide)
    viewer.installEventFilter(showEvent)
    viewer.setMouseTracking(True)
    styleEditor = Validate(styleEditor, CompleterStyle())
    viewer.setStyleSheet(styleEditor.getStyleSheet())
    viewer.setVerticalScrollMode(QListView.ScrollPerPixel)
    viewer.verticalScrollBar().setSingleStep(int(3))
    return completer
