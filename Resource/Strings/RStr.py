import re
import string
from abc import ABC
from datetime import datetime
from decimal import Decimal
from typing import Dict, Callable, Union, Optional, List, Any

from dateutil import parser

from DeclarativeQt.Resource.Grammars.RGrammar import RepeatList, Equal, isEmpty, ReferList, Validate, \
    StrFrame, GList, PureList
from DeclarativeQt.Resource.Strings.NLSource.Strings import Strings

_ThisFilePath = __file__

Symbol = str
Phrase = str
PhraseFrame = Callable[..., str]
Semantics = Dict[str, str]
SemanticFrame = Callable[..., Dict]
DTimeType = Optional[Union[str, datetime]]
NLIndex = str
NLTranslate = Dict[str, Union[str, Semantics]]


class RStr(ABC):
    CH: NLIndex = "ch"
    EN: NLIndex = "en"
    R = Strings
    Digits = list(string.digits)
    LowerLetters = list(string.ascii_lowercase)
    UpperLetters = list(string.ascii_uppercase)
    Letters = LowerLetters + UpperLetters
    DecimalPrecision = int(14)
    DecimalRound = int(6)

    @staticmethod
    def checkValue(val: str, tp: type) -> bool:
        if tp in GList(float, int, str, Decimal):
            try:
                tp(val)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                return False
            return True
        elif Equal(tp, datetime):
            try:
                parser.parse(timestr=val)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                return False
            return True
        return False

    @staticmethod
    def toDatetime(dtime: str) -> Optional[datetime]:
        try:
            dtime = parser.parse(timestr=dtime)
        except Exception as e:
            RStr.log(str(e), RStr.lgError)
            return None
        return dtime

    @staticmethod
    def dateToStandard(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                return None
        return dtime.strftime(RStr.frDefaultDateFormat)

    @staticmethod
    def timeToStandard(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                return None
        return dtime.strftime(RStr.frDefaultTimeFormat)

    @staticmethod
    def datetimeToStandard(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                return None
        return dtime.strftime(RStr.frDefaultDatetimeFormat)

    @staticmethod
    def datetimeToISO8601(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                return None
        return dtime.isoformat()

    @staticmethod
    def decimalMinPlace(item: Union[float, Decimal]) -> Optional[int]:
        if not RStr.isDecimal(item):
            return None
        dot = RStr.pDot
        item = RStr.frDecimalRound(RStr.DecimalPrecision).format(float(item))
        item = item.rstrip(str(0)).rstrip(dot)
        if dot not in item:
            return int(0)
        dx, px = item.split(dot)
        if int(dx) != 0:
            return int(0)
        vpx = px.lstrip(str(0))
        if len(vpx) <= 0:
            return int(0)
        return len(px) - len(vpx) + int(1)

    @staticmethod
    def decimalRound(item: Union[float, Decimal], xp: int) -> Union[str, Any]:
        min_place = RStr.decimalMinPlace(item)
        if min_place is None:
            return None
        xp = max(min_place, xp)
        item = RStr.frDecimalRound(xp).format(float(item))
        item = item.rstrip(str(0))
        if Equal(item[-1:], RStr.pDot):
            item += str(0)
        return item

    @staticmethod
    def isDecimal(item: Any, tolerant: bool = False, showLog: bool = False) -> bool:
        if isinstance(item, float) or isinstance(item, Decimal):
            return True
        if not tolerant:
            return False
        try:
            item = float(item)
        except Exception as e:
            if showLog:
                RStr.log(str(e), RStr.lgError)
            return False
        if showLog:
            RStr.log(str(item), RStr.lgData)
        return True

    @staticmethod
    def matchOne(source: str, tp: type) -> object:
        if Equal(tp, int):
            results = RStr.matchInts(source)
        elif Equal(tp, float):
            results = RStr.matchFloats(source)
        elif Equal(tp, Decimal):
            results = RStr.matchFloats(source)
            results = ReferList(results, lambda a0: Decimal(str(a0)))
        else:
            return str(source)
        return results[0] if not isEmpty(results) else None

    @staticmethod
    def matchInts(source: str) -> Optional[List[int]]:
        source = RStr.eraseBlank(source)
        matches = re.findall(RStr.frIntMatch, source)
        results = list()
        for match in matches:
            if isEmpty(match):
                continue
            match = match.replace(RStr.pEngComma, RStr.pEmpty)
            try:
                match = int(match)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                match = None
            results.append(match)
        return results

    @staticmethod
    def matchFloats(source: str) -> Optional[List[float]]:
        source = RStr.eraseBlank(source)
        mistake = RStr.pDot + RStr.pDot
        source = source.replace(mistake, RStr.pDot)
        matches = re.findall(RStr.frFloatMatch, source)
        results = list()
        for match in matches:
            if isEmpty(match):
                continue
            match = match.replace(RStr.pEngComma, RStr.pEmpty)
            try:
                match = float(match)
            except Exception as e:
                RStr.log(str(e), RStr.lgError)
                match = None
            results.append(match)
        return results

    @staticmethod
    def findAll(source: str, tar: str) -> List[int]:
        indexes = list()
        while tar in source:
            index = source.find(tar)
            indexes.append(index)
            source = source[index + len(tar):]
        return indexes

    @staticmethod
    def eraseBlank(word: str) -> str:
        return word.replace(RStr.pBlank, RStr.pEmpty)

    @staticmethod
    def blankRepeat(length: int) -> str:
        return RStr.repeat(RStr.pBlank, length)

    @staticmethod
    def completeWithBlank(source: str, length: int) -> str:
        return source + RStr.blankRepeat(length - len(source))

    @staticmethod
    def digits(n: int) -> str:
        return str(n)

    @staticmethod
    def joinWords(*words: str) -> str:
        return RStr.pEmpty.join(PureList(words))

    @staticmethod
    def bracket(contains: str, lang: NLIndex = EN) -> str:
        return RStr.R.stLeftBracket[lang] + contains + RStr.R.stRightBracket[lang]

    @staticmethod
    def repeat(source: str, times: int) -> str:
        return RStr.pEmpty.join(RepeatList(source, max(times, 0)))

    @staticmethod
    def wrapLongString(source: str, per: int = None):
        per = Validate(per, int(12))
        if len(source) < per:
            return source
        rest = len(source) % per
        piece = len(source) // per + int(1 if rest > 0 else 0)
        rest = rest if rest > 0 else per
        turn = piece - int(1)
        result = list()
        for i in range(turn):
            start, end = i * per, int(i + 1) * per
            item = source[start:end]
            if isEmpty(item):
                continue
            if not bool(rest <= int(per * 0.3) and i >= int(turn - 1)):
                if item[-1] in RStr.Letters:
                    if source[end] in RStr.Letters:
                        item += RStr.pConnection
                item += RStr.pLinefeed
            item.lstrip(RStr.pBlank)
            result.append(item)
        start = turn * per
        result.append(source[start:])
        return RStr.pEmpty.join(result).rstrip(RStr.pLinefeed)

    @staticmethod
    def log(info: Any, port: str = None):
        norm = RStr.lgNormal
        port = Validate(port, norm)
        print(f"{port}{info}{norm}")
        return None

    pTrue: Symbol = "√"
    pTable: Symbol = "tab"
    pFig: Symbol = "fig"
    pFalse: Symbol = "×"
    pAt: Symbol = "At"
    pMul: Symbol = "×"
    pDotMul: Symbol = "·"
    pEngComma: Symbol = ","
    pCnComma: Symbol = "，"
    pNull: Symbol = "Null"
    pUrlBlank: Symbol = "%20"
    pAbsoluteUrlPrefix: Symbol = "file:///"
    pForwardSlash: Symbol = "/"
    pBackSlash: Symbol = "\\"
    pLinefeed: Symbol = "\n"
    pBlank: Symbol = " "
    pEmpty: Symbol = ""
    pSpecialChars: Symbol = "!@#$%^&*()_+"
    pPlaceholder: Symbol = "placeholder"
    pConnection: Symbol = "-"
    pColon: Symbol = ":"
    pDot: Symbol = "."
    pGapColon: Symbol = ": "
    pSharp: Symbol = "#"
    pSuperscriptMinus: Symbol = "⁻"
    pMinus: Symbol = "-"
    pCambria: Symbol = "cambria"
    pMsyh: Symbol = "msyh"
    pOff: Symbol = "off"
    pTight: Symbol = "tight"
    pCenter: Symbol = "center"
    pList: Symbol = "list"
    pLabel: Symbol = "label"
    pNot: Symbol = "not"
    pOmit: Symbol = "···"
    pExcel: Symbol = "Excel"
    pDocx: Symbol = "Docx"
    pIn: Symbol = "in"
    pMinDate: Symbol = "1970-01-01"
    pPositiveInf: Symbol = "+∞"
    pGreater: Symbol = ">"
    pNegativeInf: Symbol = "-∞"
    pMinTime: Symbol = "00:00:00"
    pMaxTime: Symbol = "23:59:59"
    pMergeSort: Symbol = "mergesort"
    pLast: Symbol = "last"
    pCoerce: Symbol = "coerce"
    pWorkspace: Symbol = "workspace"
    pUnderlineConnection: Symbol = "_"
    lgNormal: Symbol = "\033[0m"
    lgInfo: Symbol = "\033[34m"
    lgError: Symbol = "\033[31m"
    lgWarn: Symbol = "\033[33m"
    lgData: Symbol = "\033[36m"
    frDefaultDateFormat: Phrase = "%Y-%m-%d"
    frDefaultTimeFormat: Phrase = "%H:%M:%S"
    frDefaultDatetimeFormat: Phrase = "%Y-%m-%d %H:%M:%S"
    frQStandardDateFormat: Phrase = "yyyy-MM-dd"
    frQStandardTimeFormat: Phrase = "HH:mm:ss"
    frQStandardDateTimeFormat: Phrase = "yyyy-MM-dd HH:mm:ss"
    frQuote: StrFrame = staticmethod(lambda text: f"\"{text}\"")
    frSingleQuote: StrFrame = staticmethod(lambda text: f"\'{text}\'")
    frDecimalRound: PhraseFrame = staticmethod(lambda x: "{" + f":.{x}f" + "}")
    frFloatMatch: Phrase = r"[-+]?(?:[\d,]*\.?[\d,]*)(?:[eE][-+]?\d+)?"
    frExcelDateFormat: Phrase = "yyyy-mm-dd"
    frInf: Phrase = "inf"
    frUtf8: Phrase = "utf-8"
    frHexPrefix0x: Phrase = "0x"
    frIntMatch: Phrase = r"[-+]?[\d,]+"
