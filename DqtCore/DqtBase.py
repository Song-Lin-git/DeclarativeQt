from collections import defaultdict
from functools import partial
from typing import Generic, TypeVar, Union, Callable, Iterable, Optional, Any, Tuple, List, Dict

from PyQt5.QtCore import pyqtSignal, QObject

from DeclarativeQt.Resource.Grammars.RDecorator import private
from DeclarativeQt.Resource.Grammars.RGrammar import ReferList, DtReferDict, isValid, Validate, GTuple, Equal, \
    GetDictItem
from DeclarativeQt.Resource.Grammars.RGrmBase import RGrmObject
from DeclarativeQt.Resource.Strings.RStr import RStr

_MT = TypeVar("_MT")

AlignVal = int
OptionKey = str
UiString = str
Run = RGrmObject.Run
Formula = Callable[..., _MT]
InputRequest = Callable[..., Tuple]
type RState[MT] = Union[MT, Remember[MT]]
OptionFlags = Optional[Iterable[OptionKey]]


class Remember(Generic[_MT], QObject):
    changed = pyqtSignal(object)
    activated = pyqtSignal(object, object)

    def __init__(self, value: _MT, signal: bool = True, sensitive: bool = False, spread: bool = False):
        super().__init__()
        self._value = None
        self._signal = signal
        self._sensitive = sensitive
        self._spread = spread
        self._dftVal = None
        self._connections = defaultdict(list)
        self._uniqueMethods = dict()
        self.setValue(value)

    def updateValue(self, updateExp: Callable[[Any], Any]):
        self.setValue(updateExp(self._value))
        return None

    # noinspection PyUnresolvedReferences
    def setValue(self, value: object):
        value = Remember.getValue(value)
        if value is None and self._dftVal is not None:
            value = self._dftVal
        if self._spread:
            if isinstance(value, List):
                value = Remember.rememberListItems(value)
            if isinstance(value, Dict):
                value = Remember.rememberDictItems(value)
        pre_value = self._value
        self._value = value
        if bool(pre_value != value or self._sensitive) and self._signal:
            self.changed.emit(value)
            self.activated.emit(value, pre_value)
        return None

    def setSpread(self, spread: bool):
        self._spread = spread
        self.setValue(self._value)
        return None

    def setAlwaysValid(self, val: object):
        val = Remember.getValue(val)
        if val is not None:
            self._dftVal = val
        return None

    def setAllowInvalid(self):
        self._dftVal = None
        return None

    # noinspection PyTypeChecker
    def isNotConnected(self):
        return not bool(self.isSignalConnected(self.changed) or self.isSignalConnected(self.activated))

    def value(self):
        return self._value

    def copy(self):
        return Remember[_MT](self._value, self._signal, self._sensitive)

    def equal(self, value):
        return False if self._value != Remember.getValue(value) else True

    def uniqueConnect(self, func: Callable, *args: Any, method: Callable = None, host: QObject = None):
        if func in self._uniqueMethods:
            self.disconnect(host=host, method=self._uniqueMethods[func])
        self._uniqueMethods[func] = partial(func, *args) if method is None else method
        self.connect(self._uniqueMethods[func], host=host)
        return None

    def uniqueActConnect(self, func: Callable, *args: Any, method: Callable = None, host: QObject = None):
        if func in self._uniqueMethods:
            self.disconnect(host=host, method=self._uniqueMethods[func])
        self._uniqueMethods[func] = partial(func, *args) if method is None else method
        self.actConnect(self._uniqueMethods[func], host=host)
        return None

    # noinspection PyUnresolvedReferences
    def connect(self, method: Callable, host: QObject = None, once: bool = False):
        if once:
            self.disconnect(method=method)
        self.changed.connect(method)
        self._connections[self.changed].append(GTuple(host, method))
        if isValid(host):
            # noinspection PyTypeChecker
            host.destroyed.connect(lambda: self.disconnect(host))
        return None

    # noinspection PyUnresolvedReferences
    def actConnect(self, method: Callable, host: QObject = None, once: bool = False):
        if once:
            self.disconnect(method=method)
        self.activated.connect(method)
        self._connections[self.activated].append(GTuple(host, method))
        if isValid(host):
            # noinspection PyTypeChecker
            host.destroyed.connect(lambda: self.disconnect(host))
        return None

    # noinspection PyUnresolvedReferences
    def disconnect(self, host: QObject = None, method: Callable = None):
        slot_count = 0
        log = list()
        for key, val in self._connections.items():
            signal: pyqtSignal = key
            for val_host, val_method in val:
                cancel_slot = False
                if isValid(method) and isValid(host):
                    if Equal(method, val_method) and Equal(host, val_host):
                        cancel_slot = True
                elif not isValid(method) and isValid(host):
                    if Equal(host, val_host):
                        cancel_slot = True
                elif isValid(method) and not isValid(host):
                    if Equal(method, val_method):
                        cancel_slot = True
                if cancel_slot:
                    slot_count += 1
                    try:
                        signal.disconnect(val_method)
                    except Exception as e:
                        log.append(GTuple(host, method, e))
                    self._connections[signal].remove(GTuple(val_host, val_method))
        return slot_count

    @staticmethod
    def rememberItem(item: Any):
        return item if isinstance(item, Remember) else Remember(item)

    @staticmethod
    def rememberDictItems(dt: dict):
        return DtReferDict(dt, lambda k, v: Remember.rememberItem(k), lambda k, v: Remember.rememberItem(v))

    @staticmethod
    def rememberListItems(lt: list):
        return ReferList(lt, lambda a0: Remember.rememberItem(a0))

    @staticmethod
    def obtainListItem(lt: object, idx: int):
        lt = Remember.getListValue(lt)
        if lt is None or idx >= len(lt):
            return None
        return lt[idx]

    @staticmethod
    def obtainDictItem(dt: object, key: object, default=None):
        dt = Remember.getDictValue(dt)
        return GetDictItem(dt, key, default)

    @staticmethod
    def toValid(item: object, default: object):
        if not isinstance(item, Remember):
            return Validate(item, default)
        if isValid(Remember.getValue(item)):
            return item
        item.setValue(default)
        return item

    @staticmethod
    def getValue(item: object):
        return item.value() if isinstance(item, Remember) else item

    @staticmethod
    def getListValue(items: object):
        items = Remember.getValue(items)
        if not isValid(items):
            return None
        return ReferList(items, lambda item: Remember.getValue(item))

    @staticmethod
    def getDictValue(items: object):
        items = Remember.getValue(items)
        if not isValid(items):
            return None
        return DtReferDict(items, lambda k, v: Remember.getValue(k), lambda k, v: Remember.getValue(v))


class ReferState(Generic[_MT], Remember[_MT]):
    def __init__(self, *states: RState[Any], referExp: Formula = None, value: _MT = None):
        super().__init__(value)
        self._states = states
        self._referExp = referExp if referExp else lambda *x: x
        self.updateRefValue()
        for state in self._states:
            if isinstance(state, Remember):
                # noinspection PyUnresolvedReferences
                state.changed.connect(partial(self.updateRefValue))

    @private
    def updateRefValue(self):
        result: Callable = partial(self._referExp)
        for state in self._states:
            result = partial(result, Remember.getValue(state))
        try:
            result = result()
        except Exception as e:
            RStr.log(str(e), RStr.lgError)
            return None
        self.setValue(result)
        return None


class Trigger(Remember[int]):
    trigged = pyqtSignal()

    def __init__(self):
        super().__init__(0)
        # noinspection PyUnresolvedReferences
        self.changed.connect(lambda: self.trigged.emit())

    def trig(self):
        self.setValue(self.value() + 1)

    def trigTimes(self):
        return self.value()
