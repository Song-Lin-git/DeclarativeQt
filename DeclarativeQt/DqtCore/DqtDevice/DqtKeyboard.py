from functools import partial
from typing import List, Union

from PyQt5.QtGui import QKeySequence

from DeclarativeQt.Resource.Grammars.RGrammar import LambdaList, isEmpty

KeyCode = str
KeyOperator = str


class DqtKeyboard:
    keyReturn: KeyCode = "Return"
    keyEnter: KeyCode = "Enter"
    keyCtrl: KeyCode = "Ctrl"
    optCombo: KeyOperator = ", "
    optAnd: KeyOperator = "+"

    @staticmethod
    def multiShortCuts(*keys: Union[str, int, QKeySequence]) -> List[QKeySequence]:
        toSequence = lambda a0: QKeySequence(a0)
        return LambdaList(keys, partial(toSequence))

    @property
    def keyEnterReturn(self) -> List[QKeySequence]:
        return self.multiShortCuts(self.keyReturn, self.keyEnter)

    @staticmethod
    def keySequence(*keys: str) -> QKeySequence:
        if isEmpty(keys):
            return QKeySequence()
        return QKeySequence(DqtKeyboard.optAnd.join(keys))
