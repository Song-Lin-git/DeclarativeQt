from typing import Optional, Union, Any

from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import StrFrame, DtLambdaList, GList, DictData, Key, isEmpty, \
    Validate, GIters
from DeclarativeQt.Resource.Images.RImage import RImage
from DeclarativeQt.Resource.Strings.RString import RString

Selector = str
StyleKey = str
StyleVal = Union[str, int, float, Any]


class DqtStyle:
    QPushButton: Selector = "QPushButton"
    QPushButtonPressd: Selector = "QPushButton:pressed"
    QPushButtonDisabled: Selector = "QPushButton:disabled"
    QPushButtonHover: Selector = "QPushButton:hover"
    QLabel: Selector = "QLabel"
    QLineEdit: Selector = "QLineEdit"
    QLineEditPlaceholder: Selector = "QLineEdit[text=\'\']"
    QLineEditFocused: Selector = "QLineEdit:focus"
    QLineEditUnfocused: Selector = "QLineEdit:!focus"
    QLineEditDisabled: Selector = "QLineEdit:disabled"
    QLineEditReadOnly: Selector = "QLineEdit:read-only"
    QListView: Selector = "QListView"
    QWidget: Selector = "QWidget"
    QMainWindow: Selector = "QMainWindow"
    QCheckBox: Selector = "QCheckBox"
    QCheckBoxIndicator: Selector = "QCheckBox::indicator"
    QCheckBoxIndicatorChecked: Selector = "QCheckBox::indicator:checked"
    QCheckBoxIndicatorUnchecked: Selector = "QCheckBox::indicator:unchecked"
    QCheckBoxIndicatorHover: Selector = "QCheckBox::indicator:hover"
    QCheckBoxIndicatorPressed: Selector = "QCheckBox::indicator:pressed"
    QScrollArea: Selector = "QScrollArea"
    QScrollBarHorizontal: Selector = "QScrollBar:horizontal"
    QScrollBarVertical: Selector = "QScrollBar:vertical"
    QScrollBarHandleHorizontal: Selector = "QScrollBar::handle:horizontal"
    QScrollBarHandleVertical: Selector = "QScrollBar::handle:vertical"
    QScrollBarHandleHover: Selector = "QScrollBar::handle:hover"
    QScrollBarHandlePressed: Selector = "QScrollBar::handle:pressed"
    QScrollAddSubLine: Selector = "QScrollBar::add-line, QScrollBar::sub-line"
    QScrollAddSubPage: Selector = "QScrollBar::add-page, QScrollBar::sub-page"
    QComboBoxDropDown: Selector = "QComboBox::drop-down"
    QComboBoxDropDownPressed: Selector = "QComboBox::drop-down:pressed"
    QComboBoxDropDownHover: Selector = "QComboBox::drop-down:hover"
    QComboBoxDropDownOpen: Selector = "QComboBox::drop-down:open"
    QComboBoxDownArrow: Selector = "QComboBox::down-arrow"
    QComboBoxDownArrowOn: Selector = "QComboBox::down-arrow:on"
    QComboBoxQAbstractItemView: Selector = "QComboBox QAbstractItemView"
    QComboBoxQAbstractItemViewItem: Selector = "QComboBox QAbstractItemView::item"
    QComboBoxQAbstractItemViewItemSelected: Selector = "QComboBox QAbstractItemView::item:selected"
    QComboBox: Selector = "QComboBox"
    QTableView: Selector = "QTableView"
    QTableViewQTableCornerButtonSection: Selector = "QTableView QTableCornerButton::section"
    QHeaderViewSection: Selector = "QHeaderView::section"
    QHeaderViewSectionChecked: Selector = "QHeaderView::section:checked"
    QHeaderViewSectionHover: Selector = "QHeaderView::section:hover"
    QTableViewItemSelected: Selector = "QTableView::item:selected"
    QTableViewItemHover: Selector = "QTableView::item:hover"
    QMenu: Selector = "QMenu"
    QMenuItem: Selector = "QMenu::item"
    QMenuItemSelected: Selector = "QMenu::item:selected"
    QMenuItemDisabled: Selector = "QMenu::item:disabled"
    QMenuItemHover: Selector = "QMenu::item:hover"
    QMenuSeparator: Selector = "QMenu::separator"
    QSlider: Selector = "QSlider"
    QSliderGroove: Selector = "QSlider::groove"
    QSliderSubPage: Selector = "QSlider::sub-page"
    QSliderAddPage: Selector = "QSlider::add-page"
    QSliderHandle: Selector = "QSlider::handle"
    PseudoHorizontal: Selector = ":horizontal"
    PseudoVertical: Selector = ":vertical"
    PseudoPressed: Selector = ":pressed"
    PseudoHover: Selector = ":hover"
    atGridlineColor: StyleKey = "gridline-color"
    atAlternateBackgroundColor: StyleKey = "alternate-background-color"
    atImage: StyleKey = "image"
    atBackgroundColor: StyleKey = "background-color"
    atWidth: StyleKey = "width"
    atHeight: StyleKey = "height"
    atMinWidth: StyleKey = "min-width"
    atMinHeight: StyleKey = "min-height"
    atMargin: StyleKey = "margin"
    atOutline: StyleKey = "outline"
    atColor: StyleKey = "color"
    atFontFamily: StyleKey = "font-family"
    atFontSize: StyleKey = "font-size"
    atPadding: StyleKey = "padding"
    atPaddingLeft: StyleKey = "padding-left"
    atBorder: StyleKey = "border"
    atBorderLeft: StyleKey = "border-left"
    atBorderRight: StyleKey = "border-right"
    atBorderBottom: StyleKey = "border-bottom"
    atBorderTop: StyleKey = "border-top"
    atSpacing: StyleKey = "spacing"
    atMarginTop: StyleKey = "margin-top"
    atMarginBottom: StyleKey = "margin-bottom"
    atBorderRadius: StyleKey = "border-radius"
    atFontWeight: StyleKey = "font-weight"
    atBackgroundClip: StyleKey = "background-clip"
    valBorderSolid: StyleVal = "solid"
    valBorderBox: StyleVal = "border-box"
    valPaddingBox: StyleKey = "padding-box"
    valNoBorder: StyleVal = "0px solid black"
    valNone: StyleVal = "none"
    valFontNormal: StyleVal = "normal"
    Pt: StrFrame = staticmethod(lambda x: f"{x}pt")
    Px: StrFrame = staticmethod(lambda x: f"{x}px")
    Url: StrFrame = staticmethod(lambda x: f"url({RImage.absolutePathToRelativeUrl(x)})")
    valueCat: StrFrame = staticmethod(lambda *items: " ".join(items))
    stringFrame: StrFrame = staticmethod(lambda x: f"\'{x}\'")

    def __init__(
            self, color: str = None, fontFamily: str = None, fontSize: float = None,
            selector: str = None, appendix: dict = None
    ):
        self._pDivider = " "
        self._pEnding = ";"
        self._styleMatch: StrFrame = lambda k, v: ": ".join(GList(k, v))
        self._styleCat: StrFrame = lambda styles: "; ".join(DtLambdaList(styles, self._styleMatch))
        self._styleBlock: StrFrame = lambda styles: "{ " + f"{styles}" + " }"
        self._styleFrame: StrFrame = lambda apply, styles: f"{apply} " + self._styleBlock(styles)
        self._styleDivide = lambda style: style + self._pDivider if len(style) > 0 else style
        self._style = RString.pEmpty
        if fontFamily:
            self._style += self._styleMatch(self.atFontFamily, self.stringFrame(fontFamily)) + self._pEnding
        if fontSize:
            self._style = self._styleDivide(self._style)
            self._style += self._styleMatch(self.atFontSize, self.Pt(fontSize)) + self._pEnding
        if color:
            self._style = self._styleDivide(self._style)
            self._style += self._styleMatch(self.atColor, color) + self._pEnding
        appendix: dict = Validate(appendix, dict())
        for key, val in appendix.items():
            self._style = self._styleDivide(self._style)
            self._style += self._styleMatch(key, val) + self._pEnding
        if selector and len(self._style) >= 0:
            self._style = self._styleFrame(selector, self._style)

    def appendStyle(self, apply: str, styles: dict):
        if isEmpty(styles):
            return self
        self._style = self._styleDivide(self._style)
        self._style += self._styleFrame(apply, self._styleCat(styles))
        return self

    def mergeStyle(self, styleSheet: str):
        self._style = self._styleDivide(self._style)
        self._style += styleSheet
        return self

    @property
    def style(self):
        return self._style

    def setStyle(self, style: str):
        self._style = style
        return self

    @staticmethod
    def combineSelector(*selectors: Selector):
        return str(RString.pEngComma + RString.pBlank).join(list(selectors))

    @staticmethod
    def hierarchySelector(parent: Selector, *descendant: Selector):
        return RString.pBlank.join(GList(parent) + list(descendant))

    @staticmethod
    def emptyStyle(selector: str):
        if selector in GIters(DqtStyle.QWidget):
            return DqtStyle(
                selector=DqtStyle.QWidget,
                appendix=DictData(
                    Key(DqtStyle.atBorder).Val(DqtStyle.Px(0)),
                    Key(DqtStyle.atBackgroundColor).Val(RColor.qtTransparent)
                ).data
            ).style
        return DqtStyle(selector=selector).style

    @staticmethod
    def widgetLightStyle(backgroundColor: Optional[str] = None, outline: bool = False, lineColor: str = None):
        return DqtStyle(
            appendix=DictData(
                Key(DqtStyle.atBackgroundColor).Val(Validate(backgroundColor, RColor.hexLightWhite)),
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(int(1) if outline else int(0)),
                    DqtStyle.valBorderSolid, Validate(lineColor, RColor.hexBlack)
                )),
            ).data,
            selector=DqtStyle.QWidget,
        ).style
