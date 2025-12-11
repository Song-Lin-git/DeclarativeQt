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

Callback = DqtGrmBase.BaseDqtGrammars.Callback
Execute = DqtGrmBase.BaseDqtGrammars.Execute
MainApplication = DqtGrmBase.MainApplication
ValToRemember = DqtGrmBase.BaseDqtGrammars.ValToRemember
SeqToRemember = DqtGrmBase.BaseDqtGrammars.SeqToRemember
SemanticRemember = DqtGrmBase.BaseDqtGrammars.SemanticRemember
CompareSize = DqtGrmBase.BaseDqtGrammars.CompareSize
