from typing import List, Callable, Optional

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget

from DeclarativeQt.DqtCore import DqtBase
from DeclarativeQt.DqtCore.DqtSyntax.DqtGrmBase import DqtGrmBase

RState = DqtBase.RState
PixelSTox = List[RState[int]]
FloatSTox = List[RState[float]]
StringSTox = List[RState[str]]
ColorSTox = List[RState[str]]
BoolSTox = List[RState[bool]]

DialogOffsetMethod = Callable[[QWidget], Optional[QPoint]]

MainApplication = DqtGrmBase.MainApplication
ValToState = DqtGrmBase.BaseDqtGrammars.ValToState
SeqToState = DqtGrmBase.BaseDqtGrammars.SeqToState
SmticToState = DqtGrmBase.BaseDqtGrammars.SmticToState
MapToState = DqtGrmBase.BaseDqtGrammars.MapToState
Callback = DqtGrmBase.BaseDqtGrammars.Callback
Execute = DqtGrmBase.BaseDqtGrammars.Execute
