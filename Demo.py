import sys

import numpy as np
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from DeclarativeQt.DqtCore.DqtBase import ReferState, Remember, Run
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import MainApplication
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.ComboBoxes.ComboBoxGroups.TimeEditor import TimeEditor
from DeclarativeQt.DqtUI.DqtMaven.Plotters.ManusPlotter import ManusPlotter
from DeclarativeQt.DqtUI.DqtMaven.Sliders.BaseSlider.Slider import Slider
from DeclarativeQt.DqtUI.DqtMaven.Sliders.ColoredSlider import ColoredSlider
from DeclarativeQt.DqtUI.DqtTools.AppMenu import AppMenuStyle
from DeclarativeQt.DqtUI.DqtWidgets.Container import Window, Column
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import GList, DictData, Key, GStr
from DeclarativeQt.Resource.Images.RIcon import RIcon
from DeclarativeQt.Resource.Strings.RString import RString

app = QApplication(sys.argv)

app.setStyleSheet(AppMenuStyle().getStyleSheet())
br = Remember(False)
data = Remember(10.0)
key = Remember("sin")
span = 20
npoint = 1000
smpFreq = npoint / span
tlist = np.linspace(0, span, npoint)
RString.log(br)
demo_app = MainApplication(
    Window(
        minSize=QSize(1080, 600),
        content=Column(
            autoContentResize=True,
            autoExpandContentAt=int(3),
            autoExpandToMaxCross=GList(0, 2, 3),
            style=DqtStyle().widgetLightStyle(outline=False),
            content=GList(
                IconButton(
                    fixedHeight=34,
                    icon=RIcon.loadIconPixmap(RIcon.Src.check),
                    styleEditor=ButtonStyle(
                        borderRadius=7,
                        fontFamily=RFont.YaHei,
                        borderWidth=2,
                        borderColor=ReferState(
                            br, referExp=lambda a0: RColor.hexSkyBlue if a0 else RColor.hexCyanBlue
                        ),
                    ),
                    onClick=lambda: Run(
                        key.setValue(key.value() + "0"), print(key.value())
                    ),
                ),
                ColoredSlider(
                    data=data,
                    direction=Slider.Horizontal,
                    percision=1000,
                    minVal=1,
                    maxVal=smpFreq / 2.0,
                    onValueChange=lambda: print(data.value()),
                ),
                TimeEditor(canvasModifier=TimeEditor.Canvas(editorHeight=34)),
                ManusPlotter(
                    curveData=DictData(
                        Key(key).Val(ReferState(
                            data, referExp=lambda a0: list(zip(
                                tlist.tolist(),
                                np.sin(2.0 * np.pi * a0 * tlist).tolist(),
                            ))
                        )),
                    ).data,
                    xLabel=GStr("时间/s"),
                )
            )
        )
    )
)
demo_app.run()

sys.exit(app.exec_())
