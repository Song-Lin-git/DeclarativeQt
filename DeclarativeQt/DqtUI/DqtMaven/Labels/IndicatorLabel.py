from functools import partial
from typing import Callable, Dict

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtUI.DqtMaven.Labels.BaseLabel.Label import Label
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, DictData, Key, JoinLists, GList, GetDictItem

StateIndicate = str
StyleAttribute = str


class IndicatorStates:
    WARNING: StateIndicate = "WARNING"
    INFO: StateIndicate = "INFO"
    ERROR: StateIndicate = "ERROR"
    NORMAL: StateIndicate = "NORMAL"
    REMIND: StateIndicate = "REMIND"
    DISABLED: StateIndicate = "DISABLED"


class IndicatorLabelStyle:
    WARNING = IndicatorStates.WARNING
    INFO = IndicatorStates.INFO
    ERROR = IndicatorStates.ERROR
    NORMAL = IndicatorStates.NORMAL
    REMIND = IndicatorStates.REMIND
    DISABLED = IndicatorStates.DISABLED
    atTextColor: StyleAttribute = ":atTextColor"
    atBackgroundColor: StyleAttribute = ":atBackgroundColor"
    atBorderColor: StyleAttribute = ":atBorderColor"

    def __init__(
            self,
            fontFamily: RState[str] = None,
            fontSize: RState[float] = None,
            borderWidth: RState[int] = None,
            borderRadius: RState[int] = None,
            borderStyle: RState[str] = None,
            normalColor: RState[str] = None,
            infoColor: RState[str] = None,
            errorColor: RState[str] = None,
            remindColor: RState[str] = None,
            warningColor: RState[str] = None,
            disabledColor: RState[str] = None,
            normalBackground: RState[str] = None,
            infoBackground: RState[str] = None,
            errorBackground: RState[str] = None,
            remindBackground: RState[str] = None,
            warningBackground: RState[str] = None,
            disabledBackground: RState[str] = None,
            normalBorder: RState[str] = None,
            infoBorder: RState[str] = None,
            errorBorder: RState[str] = None,
            remindBorder: RState[str] = None,
            warningBorder: RState[str] = None,
            disabledBorder: RState[str] = None,
    ):
        self._fontFamily = Validate(fontFamily, RFont.YaHei)
        self._fontSize = Validate(fontSize, RFont.fzSmallSize)
        self._borderStyle = Validate(borderStyle, DqtStyle.valBorderSolid)
        self._borderRadius = Validate(borderRadius, int(0))
        self._borderWidth = Validate(borderWidth, int(0))
        self._colors: Dict = DictData(
            Key(self.WARNING + self.atTextColor).Val(Validate(warningColor, RColor.hexRed)),
            Key(self.WARNING + self.atBackgroundColor).Val(Validate(warningBackground, RColor.qtTransparent)),
            Key(self.WARNING + self.atBorderColor).Val(Validate(warningBorder, RColor.qtTransparent)),
            Key(self.NORMAL + self.atTextColor).Val(Validate(normalColor, RColor.hexBlack)),
            Key(self.NORMAL + self.atBackgroundColor).Val(Validate(normalBackground, RColor.qtTransparent)),
            Key(self.NORMAL + self.atBorderColor).Val(Validate(normalBorder, RColor.qtTransparent)),
            Key(self.INFO + self.atTextColor).Val(Validate(infoColor, RColor.hexBlack)),
            Key(self.INFO + self.atBackgroundColor).Val(Validate(infoBackground, RColor.qtTransparent)),
            Key(self.INFO + self.atBorderColor).Val(Validate(infoBorder, RColor.qtTransparent)),
            Key(self.ERROR + self.atTextColor).Val(Validate(errorColor, RColor.hexRed)),
            Key(self.ERROR + self.atBackgroundColor).Val(Validate(errorBackground, RColor.qtTransparent)),
            Key(self.ERROR + self.atBorderColor).Val(Validate(errorBorder, RColor.qtTransparent)),
            Key(self.DISABLED + self.atTextColor).Val(Validate(disabledColor, RColor.hexGrey)),
            Key(self.DISABLED + self.atBackgroundColor).Val(Validate(disabledBackground, RColor.qtTransparent)),
            Key(self.DISABLED + self.atBorderColor).Val(Validate(disabledBorder, RColor.qtTransparent)),
            Key(self.REMIND + self.atTextColor).Val(Validate(remindColor, RColor.hexBlue)),
            Key(self.REMIND + self.atBackgroundColor).Val(Validate(remindBackground, RColor.qtTransparent)),
            Key(self.REMIND + self.atBorderColor).Val(Validate(remindBorder, RColor.qtTransparent)),
        ).data

    @property
    def colors(self):
        return self._colors

    def styles(self) -> list:
        base = GList(self._fontFamily, self._fontSize, self._borderStyle, self._borderRadius, self._borderWidth)
        return JoinLists(list(self._colors.values()), base)

    def getColor(self, state: str, key: str):
        return Remember.getValue(GetDictItem(self._colors, state + key, RColor.hexWhite))

    def getStyleSheet(self, state: str) -> str:
        return DqtStyle(
            fontFamily=Remember.getValue(self._fontFamily),
            fontSize=Remember.getValue(self._fontSize),
            color=self.getColor(Remember.getValue(state), self.atTextColor),
            appendix=DictData(
                Key(DqtStyle.atBorder).Val(DqtStyle.valueCat(
                    DqtStyle.Px(Remember.getValue(self._borderWidth)), Remember.getValue(self._borderStyle),
                    self.getColor(Remember.getValue(state), self.atBorderColor)
                )),
                Key(DqtStyle.atBorderRadius).Val(DqtStyle.Px(Remember.getValue(self._borderRadius))),
                Key(DqtStyle.atBackgroundColor).Val(self.getColor(Remember.getValue(state), self.atBackgroundColor)),
            ).data,
            selector=DqtStyle.QLabel,
        ).style


class IndicatorLabel(Label):
    WARNING: StateIndicate = IndicatorStates.WARNING
    INFO: StateIndicate = IndicatorStates.INFO
    ERROR: StateIndicate = IndicatorStates.ERROR
    NORMAL: StateIndicate = IndicatorStates.NORMAL
    REMIND: StateIndicate = IndicatorStates.REMIND
    DISABLED: StateIndicate = IndicatorStates.DISABLED

    def __init__(
            self,
            size: QSize = None,
            text: RState[str] = None,
            alignment: RState[int] = None,
            parent: QWidget = None,
            fixedHeight: int = None,
            fixedWidth: int = None,
            onClick: Callable = None,
            state: RState[str] = None,
            indicatorStyle: IndicatorLabelStyle = None,
            enable: RState[bool] = True,
            clickInfo: RState[bool] = False,
            infoTitle: RState[str] = None,
            hoverTip: RState[bool] = False,
            tipText: RState[str] = None,
            triggers: Dict[Remember, Callable] = None
    ):
        super().__init__(
            size=size,
            text=text,
            parent=parent,
            onClick=onClick,
            fixedHeight=fixedHeight,
            enable=enable,
            clickInfo=clickInfo,
            infoTitle=infoTitle,
            fixedWidth=fixedWidth,
            hoverTip=hoverTip,
            tipText=tipText,
            triggers=triggers,
            alignment=alignment,
        )
        self._styleEditor: IndicatorLabelStyle = Validate(indicatorStyle, IndicatorLabelStyle())
        self._state = Validate(state, self.NORMAL)
        self.updateStyle()
        for item in self._styleEditor.styles() + GList(self._state):
            if isinstance(item, Remember):
                item.connect(partial(self.updateStyle), host=self)

    @private
    def updateStyle(self):
        self.setStyleSheet(self._styleEditor.getStyleSheet(self._state))
        return None
