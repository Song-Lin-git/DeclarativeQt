import inspect
from functools import partial
from typing import Iterable, Dict, Union, Callable

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget

from DeclarativeQt.DqtCore.DqtBase import Remember, LambdaRemember, RState
from DeclarativeQt.Resource.Grammars.RGrammar import LambdaList, isValid
from DeclarativeQt.Resource.Strings.RString import Semantics, NLIndex


class MainApplication:
    def __init__(self, window: QMainWindow):
        self._window = window

    def run(self):
        self._window.show()


class BaseDqtGrammars:
    @staticmethod
    def SemanticRemember(language: RState[NLIndex], semantic: Semantics):
        exp = lambda a0: semantic[a0] if isValid(semantic) and isValid(a0) else None
        return LambdaRemember(language, lambdaExp=exp)

    @staticmethod
    def ValToRemember(value: object):
        if isinstance(value, Remember):
            return value
        return Remember(value)

    @staticmethod
    def SeqToRemember(sequence: Union[Iterable, Remember]):
        sequence = Remember.toValid(sequence, list())
        if isinstance(sequence, Remember):
            sequence.setSpread(True)
            return sequence
        lt = LambdaList(sequence, lambda item: BaseDqtGrammars.ValToRemember(item))
        return Remember(lt, spread=True)

    @staticmethod
    def MapToRemember(mapping: Union[Dict, Remember]):
        mapping = Remember.toValid(mapping, dict())
        if isinstance(mapping, Remember):
            mapping.setSpread(True)
            return mapping
        return Remember(Remember.rememberDictItems(mapping), spread=True)

    @staticmethod
    def Execute(dialog: QDialog):
        if not dialog:
            return None
        return dialog.exec_()

    @staticmethod
    def Callback(body: QWidget, method: Callable):
        if method is None:
            return None
        if len(inspect.signature(method).parameters) > 0:
            method = partial(method, body)
        return partial(method)

    @staticmethod
    def CompareSize(a0: QSize, a1: QSize):
        square = lambda size: size.width() * size.height()
        a0, a1 = square(a0), square(a1)
        return int(1) if a0 > a1 else int(-1 if a0 < a1 else int(0))
