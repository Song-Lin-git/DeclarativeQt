from abc import ABC

from PyQt5.QtCore import QSize, QSizeF
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMessageBox, QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, OptionKey, Trigger, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtCore.DqtDevice.DqtKeyboard import DqtKeyboard
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import ValToRemember, Execute
from DeclarativeQt.DqtUI.DqtLayouts.Layout import Column, Row
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.Dividers.LinearDivider import HorizontalDivider
from DeclarativeQt.DqtUI.DqtMaven.Labels.IconLabel import IconLabel, LabelStyle
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabel, IndicatorLabelStyle
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog
from DeclarativeQt.Resource.Colors.RColor import RColor, HexColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, Equal, DictData, Key, ReferList, GStr, EnumList
from DeclarativeQt.Resource.Grammars.RGrmBase.RGrmObject import GList, Run, DataBox
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Images.RImage import LutRatio
from DeclarativeQt.Resource.Strings.RString import RString, NLIndex

ButtonHint = int


class NoteMode(ABC):
    Info: OptionKey = "Info"
    Query: OptionKey = "Query"
    Warn: OptionKey = "Warn"
    Error: OptionKey = "Error"
    Succeed: OptionKey = "Succeed"


class NoteDialog(Dialog):
    FixTextWidthRatio: LutRatio = 1.28
    Mode = NoteMode
    Ok: ButtonHint = QMessageBox.Ok
    Yes: ButtonHint = QMessageBox.Yes
    No: ButtonHint = QMessageBox.No
    Cancel: ButtonHint = QMessageBox.Cancel
    Close: ButtonHint = QMessageBox.Close
    Escape: ButtonHint = QMessageBox.Escape
    Apply: ButtonHint = QMessageBox.Apply

    def __init__(
            self,
            parent: QWidget = None,
            title: RState[str] = None,
            text: RState[str] = None,
            buttonHint: ButtonHint = None,
            mode: OptionKey = None,
            textFont: QFont = None,
            language: RState[NLIndex] = None,
            buttonWidth: int = int(90),
            buttonHeight: int = int(28),
            iconLabelWidth: int = int(80),
            borderRadius: int = int(3),
            lineHeightRatio: float = float(1.24),
            perLine: int = None,
            itemSpacing: int = int(28),
            iconSpacing: int = int(26),
            buttonSpacing: int = int(6),
            dialogVMargin: int = int(21),
            dialogHMargin: int = int(36),
            primaryHexColor: HexColor = None
    ):
        language = Validate(language, RString.EnglishIndex)
        language = Remember.getValue(language)
        mode = Validate(mode, self.Mode.Info)
        buttonHint = Validate(buttonHint, self.Ok | self.Cancel)
        if not RColor.isHexColor(primaryHexColor):
            primaryHexColor = RColor.hexCyanBlue
        title = Validate(title, self.ModeSemantics[mode][language])
        hints = list()
        for h in self.Positive + self.Negative:
            if Equal(h & buttonHint, h):
                hints.append(h)
        textFont = Validate(textFont, self.DefaultFont)
        text = ValToRemember(Remember.toValid(text, RString.pEmpty))
        perLine = Validate(perLine, self.MaxCharPerLine[language])
        labelSize = DqtCanvas.fontTextMetric(textFont, text, lchLim=perLine)
        labelSize.setHeight(int(labelSize.height() * lineHeightRatio))
        labelSize.setWidth(int(labelSize.width() * self.FixTextWidthRatio))
        iconHeight = int(labelSize.height() * (text.value().count(RString.pLinefeed) + 1))
        iconHeight += itemSpacing + buttonHeight
        buttonAreaWidth = int(buttonWidth + buttonSpacing) * len(hints) - buttonSpacing
        dividerWidth = iconLabelWidth + max(labelSize.width(), buttonAreaWidth) + iconSpacing
        self._activatedHint = Remember(None)
        acceptor = Trigger()
        super().__init__(
            title=title,
            parent=parent,
            fixSize=True,
            acceptTrig=acceptor,
            style=DqtStyle.widgetLightStyle(RColor.hexLightWhite),
            content=Column(
                padding=dialogVMargin,
                horizontalPadding=dialogHMargin,
                spacing=dialogVMargin,
                options=GList(Column.AutoSizeNoRemain),
                content=GList(
                    HorizontalDivider(length=dividerWidth),
                    Row(
                        padding=int(0),
                        verticalPadding=int(0),
                        spacing=iconSpacing,
                        options=GList(Row.AutoSizeNoRemain),
                        content=GList(
                            IconLabel(
                                size=QSize(iconLabelWidth, iconHeight),
                                fixedWidth=iconLabelWidth,
                                iconPixmap=QPixmap(self.ModeIcons[mode]),
                                iconSizeRatio=QSizeF(0.94, 0.94),
                                styleEditor=LabelStyle(
                                    borderWidth=int(1),
                                    borderRadius=borderRadius,
                                    borderColor=RColor.hexGrey,
                                    backgroundColor=RColor.hexWhite
                                )
                            ),
                            Column(
                                spacing=itemSpacing,
                                padding=int(0),
                                horizontalPadding=int(0),
                                options=GList(Column.AutoSizeNoRemain),
                                alignment=Column.Align.Left,
                                content=GList(
                                    Column(
                                        spacing=int(0),
                                        padding=int(0),
                                        horizontalPadding=int(0),
                                        options=GList(Column.AutoSizeNoRemain),
                                        content=GList(
                                            *ReferList(
                                                GStr(text.value()).split(RString.pLinefeed), lambda a0:
                                                IndicatorLabel(
                                                    text=a0,
                                                    fixedWidth=labelSize.width(),
                                                    fixedHeight=labelSize.height(),
                                                    indicatorStyle=IndicatorLabelStyle(
                                                        fontSize=textFont.pointSize(),
                                                        fontFamily=textFont.family(),
                                                        normalBackground=RColor.qtTransparent,
                                                    )
                                                ),
                                            ),
                                        )
                                    ),
                                    Row(
                                        padding=int(0),
                                        verticalPadding=int(0),
                                        spacing=buttonSpacing,
                                        options=GList(Row.AutoSizeNoRemain),
                                        content=EnumList(
                                            hints, lambda i, a0:
                                            IconButton(
                                                text=self.ButtonSemantics[a0][language],
                                                fixedWidth=buttonWidth,
                                                fixedHeight=buttonHeight,
                                                shortCuts=None if i > 0 else DqtKeyboard().keyEnterReturn,
                                                styleEditor=ButtonStyle(
                                                    borderRadius=borderRadius,
                                                    fontSize=textFont.pointSize(),
                                                    textColor=RColor.hexDeepGrey if i > 0 else None,
                                                    fontFamily=textFont.family(),
                                                    pressedBackground=RColor.setQStyleAlpha(
                                                        primaryHexColor, 0.74
                                                    ) if i <= 0 else None,
                                                    hoverBackground=RColor.setQStyleAlpha(
                                                        primaryHexColor, 0.52
                                                    ) if i <= 0 else None,
                                                    backgroundColor=RColor.setQStyleAlpha(
                                                        primaryHexColor, 0.34
                                                    ) if i <= 0 else None,
                                                ),
                                                onClick=lambda *az, b0=a0: Run(
                                                    self._activatedHint.setValue(b0), acceptor.trig()
                                                )
                                            )
                                        )
                                    ),
                                )
                            ),
                        )
                    ), HorizontalDivider(length=dividerWidth, lineWidth=int(1)),
                )
            )
        )

    @staticmethod
    def error(
            parent: QWidget = None,
            title: RState[str] = None, text: RState[str] = None,
            buttonHint: ButtonHint = None, language: RState[NLIndex] = None,
    ) -> ButtonHint:
        return DataBox(Execute(NoteDialog(
            mode=NoteDialog.Mode.Error, parent=parent, title=title,
            text=text, language=language, buttonHint=buttonHint,
        ))).data

    @staticmethod
    def succeed(
            parent: QWidget = None,
            title: RState[str] = None, text: RState[str] = None,
            buttonHint: ButtonHint = None, language: RState[NLIndex] = None,
    ) -> ButtonHint:
        buttonHint = Validate(buttonHint, NoteDialog.Ok)
        return DataBox(Execute(NoteDialog(
            mode=NoteDialog.Mode.Succeed, parent=parent, title=title,
            text=text, language=language, buttonHint=buttonHint,
        ))).data

    @staticmethod
    def require(
            parent: QWidget = None,
            title: RState[str] = None, text: RState[str] = None,
            buttonHint: ButtonHint = None, language: RState[NLIndex] = None,
    ) -> ButtonHint:
        buttonHint = Validate(buttonHint, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        return DataBox(Execute(NoteDialog(
            mode=NoteDialog.Mode.Query, parent=parent, title=title,
            text=text, language=language, buttonHint=buttonHint,
        ))).data

    @staticmethod
    def information(
            parent: QWidget = None,
            title: RState[str] = None, text: RState[str] = None,
            buttonHint: ButtonHint = None, language: RState[NLIndex] = None,
    ) -> ButtonHint:
        return DataBox(Execute(NoteDialog(
            mode=NoteDialog.Mode.Info, parent=parent, title=title,
            text=text, language=language, buttonHint=buttonHint,
        ))).data

    @staticmethod
    def warning(
            parent: QWidget = None,
            title: RState[str] = None, text: RState[str] = None,
            buttonHint: ButtonHint = None, language: RState[NLIndex] = None,
    ) -> ButtonHint:
        return DataBox(Execute(NoteDialog(
            mode=NoteDialog.Mode.Warn, parent=parent, title=title,
            text=text, language=language, buttonHint=buttonHint,
        ))).data

    def exec_(self) -> ButtonHint:
        super().exec_()
        return self._activatedHint.value()

    def exec(self) -> ButtonHint:
        super().exec()
        return self._activatedHint.value()

    MaxCharPerLine = DictData(
        Key(RString.ChineseIndex).Val(int(30)),
        Key(RString.EnglishIndex).Val(int(60)),
    ).data
    StandardRequire = Yes | No | Cancel
    DefaultFont = QFont(RFont.YaHei, RFont.fzTinySize)
    Positive = GList(Yes, Ok, Apply)
    Negative = GList(No, Cancel, Close, Escape)
    ModeIcons = DictData(
        Key(Mode.Warn).Val(RIcon.loadIconPath(RIcon.Src.warning)),
        Key(Mode.Query).Val(RIcon.loadIconPath(RIcon.Src.notification_important)),
        Key(Mode.Info).Val(RIcon.loadIconPath(RIcon.Src.notifications)),
        Key(Mode.Error).Val(RIcon.loadIconPath(RIcon.Src.gpp_bad)),
        Key(Mode.Succeed).Val(RIcon.loadIconPath(RIcon.Src.check_circle)),
    ).data
    ModeSemantics = DictData(
        Key(Mode.Warn).Val(RString.stWarning),
        Key(Mode.Query).Val(RString.stRequire),
        Key(Mode.Info).Val(RString.stRemind),
        Key(Mode.Error).Val(RString.stError),
        Key(Mode.Succeed).Val(RString.stSucceed),
    ).data
    ButtonSemantics = DictData(
        Key(Ok).Val(RString.stOkConfirm),
        Key(Yes).Val(RString.stYes),
        Key(No).Val(RString.stNo),
        Key(Cancel).Val(RString.stCancel),
        Key(Close).Val(RString.stClose),
        Key(Apply).Val(RString.stContinue),
        Key(Escape).Val(RString.stReturn),
    ).data
