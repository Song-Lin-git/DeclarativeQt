from abc import ABC
from collections import defaultdict
from typing import Callable, Any, TypeVar, Iterable, Optional, Union, Dict, List, Tuple, get_origin, get_args

from DeclarativeQt.Resource.Grammars.RGrmBase import RGrmObject

Inf = float("inf")

_GT = TypeVar("_GT")
_XT = TypeVar("_XT")

Grammar = RGrmObject.Grammar
GStr = RGrmObject.GStr
GInt = RGrmObject.GInt
GList = RGrmObject.GList
GTuple = RGrmObject.GTuple
GDict = RGrmObject.GDict
DataBox = RGrmObject.DataBox
Key = RGrmObject.Key
Equal = lambda a0, a1: False if a0 != a1 else True
GExpDict: Grammar = lambda dt, keyExp, valExp: dict({keyExp(k, v): valExp(k, v) for k, v in dt.items()})
GExpList: Grammar = lambda lt, exp: [exp(x) for x in lt]
GEnumList: Grammar = lambda lt, exp: list([exp(i, x) for i, x in enumerate(lt)])
BaseObjects = RGrmObject


class BaseMethods(ABC):
    @staticmethod
    def SwitchListItem(lt: list, item: object, forward: bool = True):
        if item not in lt:
            return lt[0] if len(lt) > 0 else None
        index = lt.index(item)
        index += -1 if not forward else +1
        return lt[index % len(lt)]

    @staticmethod
    def CheckType(obj: object, hint: type):
        try:
            return isinstance(obj, hint)
        except TypeError:
            origin = get_origin(hint)
            args = get_args(hint)
            if origin is Union:
                return any(GExpList(args, lambda a0: BaseMethods.CheckType(obj, a0)))
            elif origin is DataBox and isinstance(obj, DataBox):
                if len(args) > 0:
                    return BaseMethods.CheckType(obj.data, args[0])
            elif origin in GTuple(list, List) and isinstance(obj, List):
                if len(args) > 0:
                    return all(GExpList(obj, lambda a0: BaseMethods.CheckType(a0, args[0])))
            elif origin in GTuple(tuple, Tuple) and isinstance(obj, Tuple):
                if len(args) > 0:
                    if len(obj) != len(args):
                        return False
                    return all(GEnumList(obj, lambda idx, a0: BaseMethods.CheckType(a0, args[idx])))
            elif origin in GTuple(dict, Dict) and isinstance(obj, Dict):
                if Equal(len(args), 2):
                    key_check = all(GExpList(obj.keys(), lambda a0: BaseMethods.CheckType(a0, args[0])))
                    val_check = all(GExpList(obj.values(), lambda a0: BaseMethods.CheckType(a0, args[1])))
                    return key_check and val_check
            return isinstance(obj, origin)

    @staticmethod
    def DtLambdaDict(dt: dict, keyExp: Callable = None, valExp: Callable = None):
        keyExp = BaseMethods.Validate(keyExp, lambda k, v: k)
        valExp = BaseMethods.Validate(valExp, lambda k, v: v)
        return GExpDict(dt, keyExp, valExp)

    @staticmethod
    def EraseListItems(lt: list, *items):
        lt = lt.copy()
        for item in items:
            if item in lt:
                lt.remove(item)
        return lt

    @staticmethod
    def CombineDict(*dt: dict):
        result = dict()
        for x in dt:
            result.update(x)
        return result

    @staticmethod
    def Validate(val: Optional[_GT], default: _XT) -> Union[_GT, _XT]:
        return val if val is not None else default

    @staticmethod
    def DictToDefault(dt: Dict, tp: type = None, defaultVal: Any = None, defaultExp: Callable = lambda: None):
        default_dt = defaultdict(tp) if tp is not None else RGrmObject.DataBox(
            defaultdict(lambda: defaultVal) if defaultVal is not None else defaultdict(defaultExp)
        ).data
        if dt is not None:
            for k, v in dt.items():
                default_dt[k] = v
        return default_dt

    @staticmethod
    def SetDictItem(dt: Dict, key, val):
        if key not in dt:
            return None
        dt[key] = val

    @staticmethod
    def GetDictItem(dt: Dict, key, default=None):
        if key in dt:
            return dt[key]
        return default

    @staticmethod
    def FixListLength(lt: List, n: int, default=None, defaultExp=None, expArg: bool = False):
        dif = n - len(lt)
        if dif > 0:
            if defaultExp is None:
                defaultExp = lambda *az: default
            lt += GExpList(range(dif), lambda i: defaultExp(i) if expArg else defaultExp())
        return lt[:n]

    @staticmethod
    def ExtendJoin(lt: Iterable, *rts: Iterable) -> List:
        result = list(lt)
        for rt in rts:
            for r in rt:
                if r not in result:
                    result.append(r)
        return result

    @staticmethod
    def SeqToFlatten(seq: Iterable) -> Tuple:
        unpack = list()
        for i in seq:
            if isinstance(i, Iterable) and not isinstance(i, str):
                unpack.extend(BaseMethods.SeqToFlatten(i))
            else:
                unpack.append(i)
        return tuple(unpack)
