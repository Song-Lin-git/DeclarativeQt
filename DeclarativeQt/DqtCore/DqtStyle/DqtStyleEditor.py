from abc import abstractmethod, ABC
from typing import Dict, Any, Self

from DeclarativeQt.DqtCore.DqtBase import Remember, RState
from DeclarativeQt.Resource.Grammars.RGrammar import GetDictItem, SetDictItem, Validate


class DqtStyleEditor(ABC):
    def __init__(self, styleValues: Dict[str, RState[Any]]):
        self._styleSources = Validate(styleValues, dict())

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
