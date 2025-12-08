from typing import Callable

from PyQt5.QtCore import QSize, QSizeF, QPoint
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, Trigger, Run, RState
from DeclarativeQt.DqtCore.DqtDevice.DqtKeyboard import DqtKeyboard
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import Execute
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.TextFields.BorderedTextField import BorderedTextField, \
    TextFieldStyle
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog, Box, Column, Row
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import Validate, Equal, GList, GStr
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Strings.RString import RString


class InputDialog:
    DefaultDialogSize: QSize = QSize(400, 240)
    DefaultEditorSize: QSize = QSize(240, 34)
    DefaultEditorStyle = TextFieldStyle(fontSize=9.8, fontFamily=RFont.YaHei, focusedBackground=RColor.hexWhite)

    @staticmethod
    def TextInputDialog(
            parent: QWidget = None,
            dialogTitle: RState[str] = None,
            dialogOffset: QPoint = None,
            dialogVPadding: int = int(30),
            dialogHPadding: int = int(20),
            editorSize: QSize = None,
            editorStyle: TextFieldStyle = None,
            editorSpacing: int = int(4),
            restoreButtonWidth: int = int(30),
            buttonSpacing: int = int(20),
            initial: str = None,
            restore: str = None,
            checkMethod: Callable = None,
            borderRadiusRatio: float = 0.08,
    ) -> str:
        initial = Validate(initial, RString.pEmpty)
        editorStyle = Validate(editorStyle, InputDialog.DefaultEditorStyle)
        editorSize = Validate(editorSize, InputDialog.DefaultEditorSize)
        confirmButtonWidth = editorSize.width() + editorSpacing + restoreButtonWidth
        text = Remember[str](initial)
        checkMethod = Validate(checkMethod, lambda a0: True)
        acceptor = Trigger()
        if Equal(Execute(Dialog(
                parent=parent,
                title=dialogTitle,
                offset=dialogOffset,
                fixWidth=True,
                acceptTrig=acceptor,
                style=DqtStyle.widgetLightStyle(RColor.hexLightWhite),
                content=Box(
                    content=Column(
                        arrangement=Column.Align.Top,
                        padding=dialogVPadding,
                        horizontalPadding=dialogHPadding,
                        spacing=buttonSpacing,
                        content=GList(
                            Row(
                                padding=int(0),
                                spacing=editorSpacing,
                                options=GList(Row.AutoSizeNoRemain),
                                content=GList(
                                    BorderedTextField(
                                        styleEditor=editorStyle,
                                        size=editorSize,
                                        fixedRadiusRatio=borderRadiusRatio,
                                        text=text,
                                    ),
                                    IconButton(
                                        size=QSize(restoreButtonWidth, editorSize.height()),
                                        fixedRadiusRatio=borderRadiusRatio,
                                        iconSizeRatio=QSizeF(0.8, 0.8),
                                        icon=RIcon().loadIconPixmap(RIcon.Src.history),
                                        onClick=lambda: Run(
                                            text.setValue(restore) if restore else None
                                        )
                                    )
                                )
                            ),
                            IconButton(
                                size=QSize(confirmButtonWidth, editorSize.height()),
                                fixedRadiusRatio=borderRadiusRatio,
                                iconSizeRatio=QSizeF(0.76, 0.76),
                                icon=RIcon().loadIconPixmap(RIcon.Src.edit_square_darkblue),
                                styleEditor=ButtonStyle(
                                    backgroundColor=RColor.setQStyleAlpha(RColor.hexForestGreen, 0.34),
                                    hoverBackground=RColor.setQStyleAlpha(RColor.hexTealGreen, 0.20),
                                    pressedBackground=RColor.setQStyleAlpha(RColor.hexTealGreen, 0.62),
                                    borderColor=RColor.hexDarkGrey,
                                ),
                                shortCuts=DqtKeyboard.multiShortCuts(
                                    DqtKeyboard.keyEnter, DqtKeyboard.keyReturn
                                ),
                                onClick=lambda: acceptor.trig() if checkMethod(text) else None,
                            )
                        )
                    )
                )
        )), Dialog.Accepted):
            return text.value()
        return GStr(initial)
