from itertools import chain
from typing import Callable, Dict, List, Tuple, Any, Optional

from DeclarativeQt.Resource.Grammars.RGrmBase import RGrmBase

Grammar = RGrmBase.Grammar
CommandFrame = Callable[..., str]
StrFrame = Callable[..., str]
StrCommand = str
Key = RGrmBase.BaseObjects.Key
Inf = RGrmBase.Inf
Continuous = float
Discrete = int
KeywordArgs = Any
VariableArgs = Any
AnyArgs = Optional[Any]
Uncountable = int
Countable = int

inRange = lambda val, minVal, maxVal: False if val < minVal or val >= maxVal else True
isEmpty: Grammar = lambda iterable: True if iterable is None or len(iterable) < 1 else False
isValid = lambda a0: True if a0 is not None else False
isAllValid = lambda *az: all([isValid(a0) for a0 in az])

Validate = RGrmBase.BaseMethods.Validate
GStr = RGrmBase.BaseObjects.GStr
GInt = RGrmBase.BaseObjects.GInt
DataBox = RGrmBase.BaseObjects.DataBox
GTuple = RGrmBase.BaseObjects.GTuple
GList = RGrmBase.BaseObjects.GList
GDict = RGrmBase.BaseObjects.GDict
GetDictItem = RGrmBase.BaseMethods.GetDictItem
SetDictItem = RGrmBase.BaseMethods.SetDictItem
PureList: Grammar = lambda lt: [x for x in lt if x is not None]
TupleData: Grammar = lambda *x: DataBox[Tuple](x)
ListData: Grammar = lambda *x: DataBox[List](list(x))
DictData: Grammar = lambda *kv: DataBox[Dict]({k: v for k, v in PureList(kv)})
GIters: Grammar = lambda *x: x
RepeatList: Grammar = lambda val, times: list([val for _ in range(times)])
SortedDict: Grammar = lambda dt, kvExp: GDict(sorted(dt.items(), key=lambda a0: kvExp(a0[0], a0[1])))
ReferList: Grammar = lambda lt, exp: list([exp(x) for x in lt])
ConditionList: Grammar = lambda lt, condition: list([x for x in lt if condition(x)])
EnumList: Grammar = RGrmBase.GEnumList
DtReferList: Grammar = lambda dt, exp: list([exp(k, v) for k, v in dt.items()])
SumNestedList: Grammar = lambda lt: sum(lt, [])
JoinLists: Grammar = lambda *lt: list(chain(*lt))
ReferDict: Grammar = lambda iterable, keyExp, valExp: dict({keyExp(x): valExp(x) for x in iterable})
EnumDict: Grammar = lambda iterable, keyExp, valExp: dict({keyExp(i, x): valExp(i, x) for i, x in enumerate(iterable)})
ConditionDict: Grammar = lambda dt, condition: dict({k: v for k, v in dt.items() if condition(k, v)})
DtReferDict: Grammar = RGrmBase.BaseMethods.DtReferDict
CombineDict: Grammar = RGrmBase.BaseMethods.CombineDict
DictToDefault: Grammar = RGrmBase.BaseMethods.DictToDefault
RevMapping: Grammar = lambda dt: dict({v: k for k, v in dt.items()})
ExpValue: Grammar = lambda x, exp: None if x is None else exp(x)
Equal = RGrmBase.Equal
ExecMethod = lambda exp: exp() if exp else None
ExtendJoin = RGrmBase.BaseMethods.ExtendJoin
EraseListItems = RGrmBase.BaseMethods.EraseListItems
CheckType = RGrmBase.BaseMethods.CheckType
FixListLength = RGrmBase.BaseMethods.FixListLength
MaxOfList: Grammar = lambda lt, exp: max(ReferList(lt, exp))
MinOfList: Grammar = lambda lt, exp: min(ReferList(lt, exp))
KvListToDict: Grammar = lambda lt: dict({k: v for k, v in lt})
SeqToFlatten = RGrmBase.BaseMethods.SeqToFlatten
LimitVal: Grammar = lambda val, minVal, maxVal: min(max(val, minVal), maxVal) if isValid(val) else None
NxLimitVal: Grammar = lambda val, a0, a1: LimitVal(val, a0, a1) if a0 < a1 else LimitVal(val, a1, a0)
IndexSubSeq: Grammar = lambda tar, sor: [sor.index(x) if x in sor else None for x in tar]
SwitchListItem: Grammar = RGrmBase.BaseMethods.SwitchListItem
