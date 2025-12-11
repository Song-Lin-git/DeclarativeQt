from abc import abstractmethod
from typing import Dict, Any, Self

from PyQt5.QtCore import QObject

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.Resource.Grammars.RGrammar import GetDictItem, SetDictItem, Validate


class DqtStyleEditor(QObject):
    def __init__(self, styleValues: Dict[str, RState[Any]]):
        super().__init__()
        self._styleSources = Validate(styleValues, dict())
        self._defaultStyles = Remember.getDictValue(self._styleSources.copy())
        for k, v in self._styleSources.items():
            if isinstance(v, Remember):
                v.setAlwaysValid(self._defaultStyles[k])

    @abstractmethod
    def getStyleSheet(self, *args, **kwargs) -> str:
        pass

    @property
    def styles(self) -> Dict[str, Any]:
        return self._styleSources

    def setStyle(self, key: str, val: object) -> Self:
        SetDictItem(self._styleSources, key, val)
        return self

    def getStyle(self, key: str) -> Any:
        return Remember.getValue(GetDictItem(self._styleSources, key))
