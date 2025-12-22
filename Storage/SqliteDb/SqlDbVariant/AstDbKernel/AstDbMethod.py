from typing import Callable

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore.DqtBase import Trigger, Run
from DeclarativeQt.DqtCore.DqtDevice.DqtKeyboard import DqtKeyboard
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import Execute
from DeclarativeQt.DqtUI.DqtLayouts.Layout import Column
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtWidgets.Container import Dialog
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Grammars.RGrammar import Equal, GList, DictData, Key, Validate
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDbMethod import SqlDbMethod


class AstDbMethod(SqlDbMethod):
    @staticmethod
    def executeRequestDialog(
            content: QWidget,
            parent: QWidget = None,
            padding: int = int(36),
            spacing: int = int(30),
            confirmButtonHeight: int = int(34),
            confirmButtinWidthRatio: float = float(1.0),
            confirmButtonRadius: int = int(3),
            dialogWidth: int = int(400),
            dialogTitle: str = None,
            dataCleanMethod: Callable = None,
            checkMethod: Callable = None,
    ) -> bool:
        confirmTrig = Trigger()
        dataCleanMethod = Validate(dataCleanMethod, lambda: None)
        checkMethod = Validate(checkMethod, lambda: True)
        result = Execute(
            Dialog(
                parent=parent,
                title=dialogTitle,
                fixedWidth=dialogWidth,
                acceptTrig=confirmTrig,
                style=DqtStyle(
                    appendix=DictData(
                        Key(DqtStyle.atBackgroundColor).Val(RColor.hexLightWhite)
                    ).data,
                    selector=DqtStyle.QWidget
                ).style,
                content=Column(
                    options=GList(Column.AutoSizeNoRemain),
                    padding=padding,
                    spacing=spacing,
                    autoExpandContentAt=int(0),
                    autoContentResize=True,
                    content=GList(
                        content,
                        IconButton(
                            size=QSize(int(content.width() * confirmButtinWidthRatio), confirmButtonHeight),
                            icon=RIcon().loadIconPixmap(RIcon.R.select_check_box),
                            fixedHeight=confirmButtonHeight,
                            styleEditor=ButtonStyle(borderRadius=confirmButtonRadius),
                            onClick=lambda: Run(
                                dataCleanMethod(), confirmTrig.trig() if checkMethod() else None
                            ),
                            shortCuts=DqtKeyboard.multiShortCuts(DqtKeyboard.keyEnter, DqtKeyboard.keyReturn)
                        )
                    )
                ),
            )
        )
        return Equal(result, Dialog.Accepted)
