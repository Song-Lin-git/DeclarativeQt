from functools import partial
from typing import List, Callable, Dict

from PyQt5.QtCore import QSizeF, QSize, QModelIndex, Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QFont, QPainter
from PyQt5.QtWidgets import QWidget, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListView, QComboBox, \
    QApplication, QFrame

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtStyle.DqtStyleEditor import DqtStyleEditor
from DeclarativeQt.DqtUI.DqtMaven.ComboBoxes.BaseComboBox.ComboBox import ComboBox
from DeclarativeQt.DqtUI.DqtTools.Scroller import ScrollerStyle
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, Validate, Equal
from DeclarativeQt.Resource.Images.RIcon import RIcon


class ComboBoxStyle(DqtStyleEditor):
    borderColor = "borderColor"
    borderWidth = "borderWidth"
    borderStyle = "borderStyle"
    downArrowIcon = "downArrowIcon"
    upArrowIcon = "upArrowIcon"
    iconSizeRatio = "iconSizeRatio"
    dropDownHoverColor = "dropDownHoverColor"
    dropDownPressedColor = "dropDownPressedColor"
    dropDownOpenColor = "dropDownOpenColor"
    dropListBackground = "dropListBackground"
    dropListBorderColor = "dropListBorderColor"
    dropListBorderWidth = "dropListBorderWidth"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            textColor: RState[str] = None,
            borderColor: RState[str] = None,
            borderStyle: RState[str] = None,
            borderWidth: RState[int] = None,
            borderRadius: RState[int] = None,
            backgroundColor: RState[str] = None,
            downArrowIcon: RState[str] = None,
            upArrowIcon: RState[str] = None,
            iconSizeRatio: QSizeF = None,
            dropDownHoverColor: RState[str] = None,
            dropDownPressedColor: RState[str] = None,
            dropDownOpenColor: RState[str] = None,
            dropListBackground: RState[str] = None,
            dropListBorderColor: RState[str] = None,
            dropListBorderWidth: RState[int] = None,
            scrollerStyle: ScrollerStyle = None
    ):
        self._styles = DictData(
            Key(DqtStyle.atFontFamily).Val(Remember.toValid(fontFamily, RFont.YaHei)),
            Key(DqtStyle.atFontSize).Val(Remember.toValid(fontSize, float(RFont.fzSmallSize))),
            Key(DqtStyle.atColor).Val(Remember.toValid(textColor, RColor.hexBlack)),
            Key(DqtStyle.atBackgroundColor).Val(Remember.toValid(backgroundColor, RColor.hexWhite)),
            Key(DqtStyle.atBorderRadius).Val(Remember.toValid(borderRadius, int(5))),
            Key(self.borderWidth).Val(Remember.toValid(borderWidth, int(1))),
            Key(self.borderColor).Val(Remember.toValid(borderColor, RColor.hexDarkGrey)),
            Key(self.borderStyle).Val(Remember.toValid(borderStyle, DqtStyle.valBorderSolid)),
            Key(self.downArrowIcon).Val(Remember.toValid(downArrowIcon, self.DefaultDownArrowIcon)),
            Key(self.upArrowIcon).Val(Remember.toValid(upArrowIcon, self.DefaultUpArrowIcon)),
            Key(self.iconSizeRatio).Val(Remember.toValid(iconSizeRatio, self.DefaultIconSizeRatio)),
            Key(self.dropDownPressedColor).Val(Remember.toValid(dropDownPressedColor, self.DefaultPressedColor)),
            Key(self.dropDownHoverColor).Val(Remember.toValid(dropDownHoverColor, self.DefaultHoverColor)),
            Key(self.dropDownOpenColor).Val(Remember.toValid(dropDownOpenColor, self.DefaultOpenColor)),
            Key(self.dropListBackground).Val(Remember.toValid(dropListBackground, RColor.hexIceBlue)),
            Key(self.dropListBorderColor).Val(Remember.toValid(dropListBorderColor, self.DefaultDropListBorderColor)),
            Key(self.dropListBorderWidth).Val(Remember.toValid(dropListBorderWidth, int(1)))
        ).data
        self._scrollerStyle = Validate(scrollerStyle, ScrollerStyle(
            scrollHandleBackground=RColor.hexMistBlue,
            scrollHandleHoverBackground=RColor.hexTealGrey,
            scrollHandlePressedBackground=RColor.hexDeepStoneBlue
        ))
        super().__init__(self._styles)

    def getStyleSheet(self, size: QSize):
        iconRatio = self.getStyle(self.iconSizeRatio)
        downArrowIcon = self.getStyle(self.downArrowIcon)
        upArrowIcon = self.getStyle(self.upArrowIcon)
        iconSize = DqtCanvas.scaleIconSize(QPixmap(downArrowIcon), size, iconRatio)
        shrink = int(self.getStyle(self.borderWidth) * 2.0)
        dropButtonSize = QSize(size.height() - shrink, size.height() - shrink)
        return DqtStyle(
            fontFamily=self.getStyle(DqtStyle.atFontFamily),
            fontSize=self.getStyle(DqtStyle.atFontSize),
            color=self.getStyle(DqtStyle.atColor),
            selector=DqtStyle.QComboBox,
            appendix=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.borderWidth)),
                    self.getStyle(self.borderStyle),
                    self.getStyle(self.borderColor)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(DqtStyle.atBackgroundColor)),
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxDownArrow,
            styles=DictData(
                Key(DqtStyle.atImage).Val(DqtStyle.Url(downArrowIcon)),
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(iconSize.width())),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(iconSize.height()))
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxDropDown,
            styles=DictData(
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(dropButtonSize.width())),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(dropButtonSize.height())),
                Key(DqtStyle.atBackgroundColor).Val(RColor.qtTransparent),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(self.getStyle(DqtStyle.atBorderRadius)))
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxDropDownHover,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.dropDownHoverColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxDropDownOpen,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.dropDownOpenColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxDownArrowOn,
            styles=DictData(
                Key(DqtStyle.atImage).Val(DqtStyle.Url(upArrowIcon)),
                Key(DqtStyle.atWidth).Val(DqtStyle.Px(iconSize.width())),
                Key(DqtStyle.atHeight).Val(DqtStyle.Px(iconSize.height()))
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxDropDownPressed,
            styles=DictData(
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.dropDownPressedColor))
            ).data
        ).appendStyle(
            apply=DqtStyle.QComboBoxQAbstractItemView,
            styles=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(self.getStyle(self.dropListBorderWidth)), DqtStyle.valBorderSolid,
                    self.getStyle(self.dropListBorderColor)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(0)),
                Key(DqtStyle.atBackgroundColor).Val(self.getStyle(self.dropListBackground)),
            ).data
        ).mergeStyle(
            styleSheet=self._scrollerStyle.getStyleSheet()
        ).style

    DefaultIconSizeRatio = QSizeF(0.92, 0.92)
    DefaultPressedColor = RColor().setQStyleAlpha(RColor.hexSteelBlue, 0.22)
    DefaultOpenColor = RColor().setQStyleAlpha(RColor.hexSteelBlue, 0.22)
    DefaultHoverColor = RColor().setQStyleAlpha(RColor.hexSteelBlue, 0.1)
    DefaultDropListBorderColor = RColor().setQStyleAlpha(RColor.hexDeepStoneBlue, 0.6)
    DefaultDownArrowIcon = RIcon().loadIconPath(RIcon.Src.arrow_drop_down)
    DefaultUpArrowIcon = RIcon().loadIconPath(RIcon.Src.arrow_drop_up)


class DropListItemDelegate(QStyledItemDelegate):
    DefaultItemSpacing = int(8)
    DefaultItemPadding = int(8)
    TextDrawRectRemainRatio = 1.28
    DefaultIconSizeRatio = 0.82
    DefaultItemBackground = RColor().hexCodeToQColor(RColor.hexWhite, 0.92)
    DefaultMouseHoverColor = QColor(230, 230, 230, int(255 * 0.8))
    DefaultPreviousColor = QColor(230, 230, 230, int(255 * 0.6))
    DefaultSelectColor = QColor(210, 210, 210, int(255 * 0.8))

    def __init__(
            self,
            itemFont: RState[QFont] = None,
            textColor: RState[str] = None,
            itemBackground: RState[QColor] = None,
            hoverBackground: RState[QColor] = None,
            selectBackground: RState[QColor] = None,
            previousBackground: RState[QColor] = None,
            itemSpacing: RState[int] = None,
            itemPadding: RState[int] = None,
            itemIcon: RState[QPixmap] = None,
            hoverIcon: RState[QPixmap] = None,
            previousIcon: RState[QPixmap] = None,
            iconSizeRatio: RState[float] = None
    ):
        super().__init__()
        self.itemFont = Validate(itemFont, QFont(RFont.YaHei, RFont.fzTinySize))
        self.textColor = Validate(textColor, RColor.hexBlack)
        self.itemBackground = Validate(itemBackground, self.DefaultItemBackground)
        self.hoverBackground = Validate(hoverBackground, self.DefaultMouseHoverColor)
        self.selectBackground = Validate(selectBackground, self.DefaultSelectColor)
        self.previousBackground = Validate(previousBackground, self.DefaultPreviousColor)
        self.itemSpacing = Validate(itemSpacing, self.DefaultItemSpacing)
        self.itemPadding = Validate(itemPadding, self.DefaultItemPadding)
        self.itemIcon = Validate(itemIcon, RIcon().loadIconPixmap(RIcon.Src.check_box_outline_blank_light))
        self.hoverIcon = Validate(hoverIcon, RIcon().loadIconPixmap(RIcon.Src.select_check_box_sereneblue))
        self.iconSizeRatio = Validate(iconSizeRatio, self.DefaultIconSizeRatio)
        self.previousIcon = Validate(previousIcon, RIcon().loadIconPixmap(RIcon.Src.check))

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + Remember.getValue(self.itemSpacing))
        return size

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        offsetRatio = 0.08
        color: QColor = QColor(Remember.getValue(self.itemBackground))
        if not index.row() % 2:
            color.setAlphaF(color.alphaF() * 0.76)
        painter.fillRect(option.rect, color)
        selected = option.state & QStyle.State_Selected
        color = Qt.transparent
        if selected:
            color = self.selectBackground
        elif option.state & QStyle.State_MouseOver:
            color = self.hoverBackground
        icon = self.itemIcon if not selected else self.hoverIcon
        text = index.data(Qt.DisplayRole)
        parent = self.parent()
        if isinstance(parent, QComboBox):
            if Equal(text, parent.currentText()) and not selected:
                icon = self.previousIcon
                color = self.previousBackground
        painter.fillRect(option.rect, Remember.getValue(color))
        option.rect.setY(int(option.rect.y() + option.rect.height() * offsetRatio))
        option.rect.setHeight(int(option.rect.height() * float(1.0 - 2.1 * offsetRatio)))
        padding = Remember.getValue(self.itemPadding)
        option.rect.setX(option.rect.x() + int(padding / 1.9))
        icon_size = int(option.rect.height() * Remember.getValue(self.iconSizeRatio))
        icon_at = QPoint(option.rect.x(), option.rect.y() + int((option.rect.height() - icon_size) / 1.02))
        painter.drawPixmap(icon_at.x(), icon_at.y(), icon_size, icon_size, Remember.getValue(icon))
        option.rect.setX(option.rect.x() + icon_size)
        option.rect.setX(option.rect.x() + int(padding / 1.08))
        option.rect.setWidth(int(option.rect.width() - 1.2 * padding))
        font = Remember.getValue(self.itemFont)
        painter.setFont(font)
        painter.setPen(QColor(Remember.getValue(self.textColor)))
        option.rect.setHeight(int(option.rect.height() * 0.92))
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignBottom, text)
        painter.restore()
        return None


class BorderedComboBox(ComboBox):
    ItemStyle = DropListItemDelegate

    def __init__(
            self,
            size: QSize = None,
            dataModel: RState[List[str]] = None,
            fixedHeight: int = None,
            selection: RState[str] = None,
            parent: QWidget = None,
            onSelected: Callable = None,
            styleEditor: ComboBoxStyle = None,
            dropListOffset: int = None,
            scrollStep: int = None,
            itemStyle: DropListItemDelegate = None,
            placeholder: str = None,
            wheelEnable: RState[bool] = False,
            wheelCycle: RState[bool] = True,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__(
            size=size,
            dataModel=dataModel,
            fixedHeight=fixedHeight,
            selection=selection,
            parent=parent,
            onSelected=onSelected,
            placeholder=placeholder,
            triggers=triggers,
            wheelCycle=wheelCycle,
            wheelEnable=wheelEnable,
        )
        itemStyle = Validate(itemStyle, DropListItemDelegate())
        itemStyle.setParent(self)
        self.view().setItemDelegate(itemStyle)
        self.view().setVerticalScrollMode(QListView.ScrollPerPixel)
        scrollStep = Validate(scrollStep, self.DefaultScrollStep)
        self.view().verticalScrollBar().setSingleStep(scrollStep)
        self.view().setAutoScroll(False)
        self._styleEditor = Validate(styleEditor, ComboBoxStyle())
        self._dropListOffset = Validate(dropListOffset, int(0))
        for v in self._styleEditor.styles.values():
            if isinstance(v, Remember):
                v.connect(partial(self.updateStyle), host=self)

    def updateStyle(self):
        self.setStyleSheet(self._styleEditor.getStyleSheet(self.size()))
        return None

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.updateStyle()
        return None

    def showPopup(self):
        popup = self.view()
        popup.setWindowFlags(popup.windowFlags() | Qt.FramelessWindowHint)
        view_port = popup.parent()
        screen_height = QApplication.primaryScreen().size().height()
        if isinstance(view_port, QFrame):
            view_port.setMaximumHeight(screen_height)
        animate = QApplication.isEffectEnabled(Qt.UI_AnimateCombo)
        QApplication.setEffectEnabled(Qt.UI_AnimateCombo, False)
        super().showPopup()
        QApplication.setEffectEnabled(Qt.UI_AnimateCombo, animate)
        if isinstance(view_port, QFrame):
            base_pos = self.mapToGlobal(QPoint(0, self.height()))
            move_to = QPoint(base_pos.x(), base_pos.y() + self._dropListOffset)
            max_height = screen_height - move_to.y() - self.DropListVerticalRemain
            if max_height < self.MinMaxDropListHeight:
                move_to = QPoint(base_pos.x() + self.width(), base_pos.y() - popup.height() + self._dropListOffset)
            else:
                view_port.setMaximumHeight(max_height)
            view_port.move(move_to)
        return None

    DropListVerticalRemain: int = int(10)
    MinMaxDropListHeight: int = int(200)
    DefaultScrollStep: int = int(3)
