from typing import Callable, Any, TypeVar, Generic

Grammar = Callable
GStr: Grammar = lambda x: "" if x is None else str(x)
GInt: Grammar = lambda x: None if x is None else int(x)
GTuple: Grammar = lambda *x: x
GList: Grammar = lambda *x: list(x)
GDict: Grammar = lambda *kv: dict({k: v for k, v in kv})

_BT = TypeVar("_BT")


class DataBox(Generic[_BT]):
    def __init__(self, data: _BT):
        self._data = data

    @property
    def data(self) -> _BT:
        return self._data

    @staticmethod
    def isValid(obj: object):
        if obj is None:
            return False
        if not isinstance(obj, DataBox):
            return True
        return False if obj.data is None else True


class Key(object):
    def __init__(self, key: Any):
        self._key = key

    def Val(self, val: Any) -> tuple:
        return GTuple(self._key, val)


class Run(object):
    def __init__(self, *cmds):
        self._result = cmds

    def act(self):
        self._result = list(self._result)
        return None

    @property
    def result(self):
        return self._result
