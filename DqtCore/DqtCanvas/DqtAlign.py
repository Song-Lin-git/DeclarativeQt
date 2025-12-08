from typing import Callable

from PyQt5.QtCore import Qt

from DeclarativeQt.DqtCore.DqtBase import AlignVal
from DeclarativeQt.Resource.Grammars.RGrammar import TupleData


class DqtAlign:
    Group: Callable = staticmethod(lambda h, v: h | v)
    Left: AlignVal = Qt.AlignLeft
    HCenter: AlignVal = Qt.AlignHCenter
    Right: AlignVal = Qt.AlignRight
    VCenter: AlignVal = Qt.AlignVCenter
    Center: AlignVal = Qt.AlignHCenter | Qt.AlignVCenter
    Top: AlignVal = Qt.AlignTop
    Bottom: AlignVal = Qt.AlignBottom
    Front = TupleData(Qt.AlignLeft, Qt.AlignTop).data
    Back = TupleData(Qt.AlignRight, Qt.AlignBottom).data
