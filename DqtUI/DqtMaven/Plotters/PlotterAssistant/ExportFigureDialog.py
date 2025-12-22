import os
from typing import Tuple, Callable

from PyQt5.QtCore import QSize, QSizeF, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog
from matplotlib.figure import Figure

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.DqtCore.DqtCanvas import DqtCanvas
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.Dialogs.MetaDialogs.NoteDialog import NoteDialog
from DeclarativeQt.DqtUI.DqtMaven.Labels.PixmapLabel import PixmapLabel
from DeclarativeQt.DqtUI.DqtMaven.Plotters.BasePlotter.MultiAxisPlotter import MultiAxisPlotter
from DeclarativeQt.DqtUI.DqtMaven.Plotters.PlotterAssistant.PlotterDialog.PlotterDialog import PlotterDialog
from DeclarativeQt.DqtUI.DqtMaven.Spacers.LinearSpacer import VerticalSpacer
from DeclarativeQt.DqtUI.DqtWidgets.Container import Column, Row
from DeclarativeQt.Resource.Colors.RColor import HexColor, RColor
from DeclarativeQt.Resource.FileTypes.RFileType import RFileType
from DeclarativeQt.Resource.Grammars.RGrammar import GList, DataBox, isValid, isEmpty, Validate, ReferList, \
    Equal, ExpValue
from DeclarativeQt.Resource.Graphics.GtrTools.GtrPillow import PilGraphic
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Images.RImage import LutRatio
from DeclarativeQt.Resource.Strings.RString import RString, Semantics, NLIndex

ExportOptionArg = Tuple[QPixmap, HexColor, Semantics, Callable[[Figure], bool]]


class ExportFigureDialog(PlotterDialog):
    DefaultDpi: int = int(300)
    PlotterSizeLimitBox: QSize = QSize(1640, 960)

    def __init__(
            self,
            drivePlotter: MultiAxisPlotter,
            parent: QWidget = None,
            dialogTitle: str = None,
            dialogOffset: QPoint = None,
            language: RState[NLIndex] = None,
            buttonWidth: int = int(160),
            buttonHeight: int = int(34),
            buttonSpacing: int = int(10),
            borderRadius: int = int(3),
            buttonFontSize: float = float(9.2),
            dialogHPadding: int = int(20),
            dialogVPadding: int = int(30),
            **options: ExportOptionArg,
    ):
        dialogTitle = Validate(dialogTitle, RString.pEmpty)
        self._lng = Remember.getValue(Validate(language, RString.EnglishIndex))
        self._ax, self._fig, self._plotter = drivePlotter.plotterCopy(curvesCopy=True)
        canvas_size: QSize = drivePlotter.size()
        canvas_aspect: LutRatio = DqtCanvas.rectAspect(canvas_size)
        limit_size: QSize = DqtCanvas.fillLimitBox(canvas_aspect, self.PlotterSizeLimitBox)
        if DqtCanvas.compareSize(limit_size, self._plotter.size()) < 0:
            self._plotter = DataBox(PixmapLabel(
                pixmap=PilGraphic.toQPixmap(PilGraphic.fromMatplotFig(self._fig)),
                size=limit_size,
            )).data
        super().__init__(
            fixSize=True,
            parent=parent,
            offset=dialogOffset,
            title=dialogTitle,
            contentPaddingRatio=0.001,
            figures=GList(self._fig),
            content=Column(
                autoContentResize=True,
                alignment=Column.Align.Right,
                padding=dialogVPadding,
                horizontalPadding=dialogHPadding,
                options=GList(Column.AutoSizeNoRemain),
                content=GList(
                    self._plotter, VerticalSpacer(height=int(10)),
                    Row(
                        options=GList(Row.NoPadding),
                        spacing=buttonSpacing,
                        content=GList(
                            IconButton(
                                fixedWidth=buttonWidth,
                                fixedHeight=buttonHeight,
                                iconSizeRatio=QSizeF(0.8, 0.8),
                                styleEditor=ButtonStyle(
                                    borderRadius=borderRadius,
                                    fontSize=buttonFontSize,
                                ),
                                icon=RIcon().loadIconPixmap(RIcon.Src.output),
                                text=RString.stExportFigure[self._lng],
                                onClick=lambda: self.actExportFigure(self._lng),
                            ),
                            *ReferList(
                                options.values(), lambda a0:
                                IconButton(
                                    fixedWidth=buttonWidth,
                                    fixedHeight=buttonHeight,
                                    iconSizeRatio=QSizeF(0.8, 0.8),
                                    icon=QPixmap(a0[0]),
                                    styleEditor=ButtonStyle(
                                        borderRadius=borderRadius,
                                        fontSize=buttonFontSize,
                                        backgroundColor=RColor.setQStyleAlpha(
                                            Validate(a0[1], RColor.hexIceBlue), 0.16
                                        ),
                                        hoverBackground=RColor.setQStyleAlpha(
                                            Validate(a0[1], RColor.hexIceBlue), 0.36
                                        ),
                                        pressedBackground=RColor.setQStyleAlpha(
                                            Validate(a0[1], RColor.hexIceBlue), 0.68
                                        ),
                                    ),
                                    text=ExpValue(a0[2], lambda b0: b0[self._lng]),
                                    onClick=lambda: ExpValue(a0[3], lambda b0: b0(self._fig)),
                                ),
                            )
                        )
                    ), VerticalSpacer(height=int(10)),
                )
            )
        )

    @property
    def fig(self):
        return self._fig

    def actExportFigure(
            self, language: RState[NLIndex] = None,
            dpi: int = DefaultDpi, escape: bool = False,
    ) -> None:
        lng = Remember.getValue(Validate(language, self._lng))
        file_path = DataBox(QFileDialog.getSaveFileName(
            parent=self, caption=RString.stExportFigure[lng],
            directory=os.path.join(os.getcwd(), RString.stFigure[lng]),
            filter=RFileType().joinFilters(RFileType.fltPng, RFileType.fltJpg)
        )).data[0]
        if not isValid(file_path) or isEmpty(file_path):
            return None
        self._fig.savefig(file_path, dpi=dpi)
        if Equal(NoteDialog.information(
                text=RString.joinWords(
                    RString.stAlreadyExportToFile[lng],
                    RString.pLinefeed, file_path
                ), language=lng, parent=self,
                buttonHint=NoteDialog.Ok | NoteDialog.Escape,
        ), NoteDialog.Ok) and escape:
            self.accept()
        return None
