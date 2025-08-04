import math
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget

from DeclarativeQt.DqtCore.DqtBase import LambdaRemember, Remember, Run
from DeclarativeQt.DqtCore.DqtMethods.DqtMethods import DqtMethods
from DeclarativeQt.DqtCore.DqtStyle.DqtStyle import DqtStyle
from DeclarativeQt.DqtCore.DqtSyntax.DqtSyntax import MainApplication
from DeclarativeQt.DqtUI.DqtMaven.Buttons.BorderedButton import ButtonStyle
from DeclarativeQt.DqtUI.DqtMaven.Buttons.IconButton import IconButton
from DeclarativeQt.DqtUI.DqtMaven.ComboBoxes.ComboBoxGroups.TimeEditor import TimeEditor
from DeclarativeQt.DqtUI.DqtMaven.Labels.IndicatorLabel import IndicatorLabel
from DeclarativeQt.DqtUI.DqtMaven.Plotters.ManusPlotter import ManusPlotter
from DeclarativeQt.DqtUI.DqtMaven.Sliders.BaseSlider.Slider import Slider
from DeclarativeQt.DqtUI.DqtMaven.Sliders.ColoredSlider import ColoredSlider
from DeclarativeQt.DqtUI.DqtTools.AppMenu import AppMenuStyle
from DeclarativeQt.DqtUI.DqtTools.AsyncWoker import AsyncWorker, RActor
from DeclarativeQt.DqtUI.DqtWidgets.Container import Window, Column
from DeclarativeQt.Resource.Colors.RColor import RColor
from DeclarativeQt.Resource.Fonts.RFont import RFont
from DeclarativeQt.Resource.Grammars.RGrammar import GList, DictData, Key, LambdaList, GTuple, GStr
from DeclarativeQt.Resource.Images.RIcon import RIcon

app = QApplication(sys.argv)
app.setStyleSheet(AppMenuStyle().getStyleSheet())
print(issubclass(Window, QWidget))
br = Remember(False)
data = Remember(0.0)


def calc():
    for i in range(1000000):
        x = Remember(None)
        x.setValue(1)


timer = Remember(0.0)
main_app = MainApplication(
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
                        borderColor=LambdaRemember(
                            br, lambdaExp=lambda a0: RColor.hexSkyBlue if a0 else RColor.hexCyanBlue
                        ),
                    ),
                    onClick=lambda a0: Run(
                        AsyncWorker(
                            thread=RActor(calc), parent=a0, timer=timer,
                            onFinished=lambda: print(DqtMethods.backtrackTypedParent(a0, Column, skip=10)),
                        ).start()
                    )
                ),
                IndicatorLabel(
                    text=LambdaRemember(
                        timer, lambdaExp=lambda a0: GStr(a0)
                    )
                ),
                ColoredSlider(
                    data=data,
                    direction=Slider.Horizontal,
                    percision=1000,
                    onValueChange=lambda: print(data.value()),
                ),
                TimeEditor(canvasModifier=TimeEditor.Canvas(editorHeight=34)),
                ManusPlotter(
                    datas=DictData(
                        Key("sin").Val(LambdaList(range(1000), lambda i: GTuple(i * 0.1, math.sin(i * 0.1)))),
                    ).data,
                    xLabel=GStr("时间/s")
                )
            )
        )
    )
)

main_app.run()
sys.exit(app.exec_())
