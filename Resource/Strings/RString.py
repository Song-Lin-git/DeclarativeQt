import re
import string
from abc import ABC
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, Callable, Union, Optional, List, Any

import yaml
from dateutil import parser

from DeclarativeQt.Resource.Grammars.RGrammar import RepeatList, Equal, isEmpty, DictToDefault, ReferList, Validate, \
    StrFrame, GList, PureList

_ThisFilePath = __file__

Symbol = str
Phrase = str
PhraseFrame = Callable[..., str]
Semantics = Dict
SemanticFrame = Callable[..., Dict]
DTimeType = Optional[Union[str, datetime]]
NLIndex = str
NLTranslate = Dict[str, Union[str, Semantics]]


class RString(ABC):
    ChineseIndex: NLIndex = "ch"
    EnglishIndex: NLIndex = "en"
    NLSourceAt = Path(r"NLSource/Strings.yaml")
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
                RString.log(str(e), RString.lgError)
                return False
            return True
        elif Equal(tp, datetime):
            try:
                parser.parse(timestr=val)
            except Exception as e:
                RString.log(str(e), RString.lgError)
                return False
            return True
        return False

    @staticmethod
    def toDatetime(dtime: str) -> Optional[datetime]:
        try:
            dtime = parser.parse(timestr=dtime)
        except Exception as e:
            RString.log(str(e), RString.lgError)
            return None
        return dtime

    @staticmethod
    def dateToStandard(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RString.log(str(e), RString.lgError)
                return None
        return dtime.strftime(RString.frDefaultDateFormat)

    @staticmethod
    def timeToStandard(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RString.log(str(e), RString.lgError)
                return None
        return dtime.strftime(RString.frDefaultTimeFormat)

    @staticmethod
    def datetimeToStandard(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RString.log(str(e), RString.lgError)
                return None
        return dtime.strftime(RString.frDefaultDatetimeFormat)

    @staticmethod
    def datetimeToISO8601(dtime: DTimeType) -> Optional[str]:
        dtime = Validate(dtime, datetime.now())
        if isinstance(dtime, str):
            try:
                dtime = parser.parse(timestr=dtime)
            except Exception as e:
                RString.log(str(e), RString.lgError)
                return None
        return dtime.isoformat()

    @staticmethod
    def decimalMinPlace(item: Union[float, Decimal]) -> Optional[int]:
        if not RString.isDecimal(item):
            return None
        dot = RString.pDot
        item = RString.frDecimalRound(RString.DecimalPrecision).format(float(item))
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
        min_place = RString.decimalMinPlace(item)
        if min_place is None:
            return None
        xp = max(min_place, xp)
        item = RString.frDecimalRound(xp).format(float(item))
        item = item.rstrip(str(0))
        if Equal(item[-1:], RString.pDot):
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
                RString.log(str(e), RString.lgError)
            return False
        if showLog:
            RString.log(str(item), RString.lgData)
        return True

    @staticmethod
    def matchOne(source: str, tp: type) -> object:
        if Equal(tp, int):
            results = RString.matchInts(source)
        elif Equal(tp, float):
            results = RString.matchFloats(source)
        elif Equal(tp, Decimal):
            results = RString.matchFloats(source)
            results = ReferList(results, lambda a0: Decimal(str(a0)))
        else:
            return str(source)
        return results[0] if not isEmpty(results) else None

    @staticmethod
    def matchInts(source: str) -> Optional[List[int]]:
        source = RString.eraseBlank(source)
        matches = re.findall(RString.frIntMatch, source)
        results = list()
        for match in matches:
            if isEmpty(match):
                continue
            match = match.replace(RString.pEngComma, RString.pEmpty)
            try:
                match = int(match)
            except Exception as e:
                RString.log(str(e), RString.lgError)
                match = None
            results.append(match)
        return results

    @staticmethod
    def matchFloats(source: str) -> Optional[List[float]]:
        source = RString.eraseBlank(source)
        mistake = RString.pDot + RString.pDot
        source = source.replace(mistake, RString.pDot)
        matches = re.findall(RString.frFloatMatch, source)
        results = list()
        for match in matches:
            if isEmpty(match):
                continue
            match = match.replace(RString.pEngComma, RString.pEmpty)
            try:
                match = float(match)
            except Exception as e:
                RString.log(str(e), RString.lgError)
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
        return word.replace(RString.pBlank, RString.pEmpty)

    @staticmethod
    def blankRepeat(length: int) -> str:
        return RString.repeat(RString.pBlank, length)

    @staticmethod
    def completeWithBlank(source: str, length: int) -> str:
        return source + RString.blankRepeat(length - len(source))

    @staticmethod
    def digits(n: int) -> str:
        return str(n)

    @staticmethod
    def joinWords(*words: str) -> str:
        return RString.pEmpty.join(PureList(words))

    @staticmethod
    def bracket(contains: str, language: NLIndex = EnglishIndex) -> str:
        return RString.stLeftBracket[language] + contains + RString.stRightBracket[language]

    @staticmethod
    def repeat(source: str, times: int) -> str:
        return RString.pEmpty.join(RepeatList(source, max(times, 0)))

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
                if item[-1] in RString.Letters:
                    if source[end] in RString.Letters:
                        item += RString.pConnection
                item += RString.pLinefeed
            item.lstrip(RString.pBlank)
            result.append(item)
        start = turn * per
        result.append(source[start:])
        return RString.pEmpty.join(result).rstrip(RString.pLinefeed)

    @staticmethod
    def log(info: Any, port: str = None):
        norm = RString.lgNormal
        port = Validate(port, norm)
        print(port, info, norm, sep=RString.pEmpty)
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
    frExcelDateFormat: Phrase = "yyyy-mm-dd"
    frDefaultDatetimeFormat: Phrase = "%Y-%m-%d %H:%M:%S"
    frDefaultDateFormat: Phrase = "%Y-%m-%d"
    frDefaultTimeFormat: Phrase = "%H:%M:%S"
    frQStandardDateFormat: Phrase = "yyyy-MM-dd"
    frQStandardTimeFormat: Phrase = "HH:mm:ss"
    frQStandardDateTimeFormat: Phrase = "yyyy-MM-dd HH:mm:ss"
    frInf: Phrase = "inf"
    frUtf8: Phrase = "utf-8"
    frHexPrefix0x: Phrase = "0x"
    frFloatMatch: Phrase = r"[-+]?(?:[\d,]*\.?[\d,]*)(?:[eE][-+]?\d+)?"
    frIntMatch: Phrase = r"[-+]?[\d,]+"
    frDecimalRound: PhraseFrame = staticmethod(lambda x: "{" + f":.{x}f" + "}")
    frQuote: StrFrame = staticmethod(lambda text: f"\"{text}\"")
    frSingleQuote: StrFrame = staticmethod(lambda text: f"\'{text}\'")
    lgNormal: Symbol = "\033[0m"
    lgInfo: Symbol = "\033[34m"
    lgError: Symbol = "\033[31m"
    lgWarn: Symbol = "\033[33m"
    lgData: Symbol = "\033[36m"
    with open(Path(_ThisFilePath).parent / NLSourceAt, "r", encoding="utf-8") as file:
        loader = dict(yaml.safe_load(file))
        semantic = DictToDefault(loader, defaultExp=lambda: defaultdict(str))
    stRemove: Semantics = semantic["stRemove"]
    stDate: Semantics = semantic["stDate"]
    stLine: Semantics = semantic["stLine"]
    stCurveStyle: Semantics = semantic["stCurveStyle"]
    stPinner: Semantics = semantic["stPinner"]
    stAtDate: Semantics = semantic["stAtDate"]
    stViewTabularSpace: Semantics = semantic["stViewTabularSpace"]
    stPrintPreview: Semantics = semantic["stPrintPreview"]
    stAnalyzeTabularsInSpace: Semantics = semantic["stAnalyzeTabularsInSpace"]
    stTimeRange: Semantics = semantic["stTimeRange"]
    stStatisticalAnalysis: Semantics = semantic["stStatisticalAnalysis"]
    stSureToAnalyze: Semantics = semantic["stSureToAnalyze"]
    stPageDirection: Semantics = semantic["stPageDirection"]
    stLandscape: Semantics = semantic["stLandscape"]
    stPortrait: Semantics = semantic["stPortrait"]
    stMergeTabulars: Semantics = semantic["stMergeTabulars"]
    stCircleMarker: Semantics = semantic["stCircleMarker"]
    stViewFigureSpace: Semantics = semantic["stViewFigureSpace"]
    stConfirmInputInfos: Semantics = semantic["stConfirmInputInfos"]
    stExportFigToReport: Semantics = semantic["stExportFigToReport"]
    stConvertUnit: Semantics = semantic["stConvertUnit"]
    stDateRange: Semantics = semantic["stDateRange"]
    stReturn: Semantics = semantic["stReturn"]
    stCursorColor: Semantics = semantic["stCursorColor"]
    stCurveColor: Semantics = semantic["stCurveColor"]
    stNotAscendingTimeSeq: Semantics = semantic["stNotAscendingTimeSeq"]
    stContinue: Semantics = semantic["stContinue"]
    stManageSpecimens: Semantics = semantic["stManageSpecimens"]
    stOptManageSpecimens: Semantics = semantic["stOptManageSpecimens"]
    stBasicInfoForReport: Semantics = semantic["stBasicInfoForReport"]
    stPlotTabSpaceCurves: Semantics = semantic["stPlotTabSpaceCurves"]
    stTabsAllEmpty: Semantics = semantic["stTabsAllEmpty"]
    stExportAs: Semantics = semantic["stExportAs"]
    stDistributionHistogram: Semantics = semantic["stDistributionHistogram"]
    stAbbrTemperature: Semantics = semantic["stAbbrTemperature"]
    stNormQQPlot: Semantics = semantic["stNormQQPlot"]
    stAutoTightCanvas: Semantics = semantic["stAutoTightCanvas"]
    stSpecimenAlreadyExist: Semantics = semantic["stSpecimenAlreadyExist"]
    stSpecimenNameNotValid: Semantics = semantic["stSpecimenNameNotValid"]
    stUnitHasBeenConverted: Semantics = semantic["stUnitHasBeenConverted"]
    stYear: Semantics = semantic["stYear"]
    stIsComfirmToConvert: Semantics = semantic["stIsComfirmToConvert"]
    stConversionSucceed: Semantics = semantic["stConversionSucceed"]
    stAbbrCondition: Semantics = semantic["stAbbrCondition"]
    stNotMatchExRtData: Semantics = semantic["stNotMatchExRtData"]
    stAboveMold: Semantics = semantic["stAboveMold"]
    stBelowMold: Semantics = semantic["stBelowMold"]
    stSubgroupMeans: Semantics = semantic["stSubgroupMeans"]
    stRControlChart: Semantics = semantic["stRControlChart"]
    stXControlChart: Semantics = semantic["stXControlChart"]
    stXBarControlChart: Semantics = semantic["stXBarControlChart"]
    stSubgroupRanges: Semantics = semantic["stSubgroupRanges"]
    stManageAccounts: Semantics = semantic["stManageAccounts"]
    stMonth: Semantics = semantic["stMonth"]
    stMovingRangesChart: Semantics = semantic["stMovingRangesChart"]
    stMovingRanges: Semantics = semantic["stMovingRanges"]
    stIndividualValues: Semantics = semantic["stIndividualValues"]
    stGlobalUnitSetting: Semantics = semantic["stGlobalUnitSetting"]
    stTabularSpace: Semantics = semantic["stTabularSpace"]
    stTestHistory: Semantics = semantic["stTestHistory"]
    stSpecimenTestMethod: Semantics = semantic["stSpecimenTestMethod"]
    stSpecimenClassify: Semantics = semantic["stSpecimenClassify"]
    stFigureSpace: Semantics = semantic["stFigureSpace"]
    stDataQuery: Semantics = semantic["stDataQuery"]
    stTabular: Semantics = semantic["stTabular"]
    stGlobalLanguageSetting: Semantics = semantic["stGlobalLanguageSetting"]
    stWorkspace: Semantics = semantic["stWorkspace"]
    stDay: Semantics = semantic["stDay"]
    stGlobalSettings: Semantics = semantic["stGlobalSettings"]
    stHour: Semantics = semantic["stHour"]
    stSureToPlot: Semantics = semantic["stSureToPlot"]
    stPlotCurves: Semantics = semantic["stPlotCurves"]
    stClose: Semantics = semantic["stClose"]
    stCancel: Semantics = semantic["stCancel"]
    stBaseInfo: Semantics = semantic["stBaseInfo"]
    stOptManageAccounts: Semantics = semantic["stOptManageAccounts"]
    stAbbrFrequency: Semantics = semantic["stAbbrFrequency"]
    stAbbrStrainDegree: Semantics = semantic["stAbbrStrainDegree"]
    stSureToSortTabular: Semantics = semantic["stSureToSortTabular"]
    stSortTabular: Semantics = semantic["stSortTabular"]
    stTabHasBeenSorted: Semantics = semantic["stTabHasBeenSorted"]
    stSortingSucceed: Semantics = semantic["stSortingSucceed"]
    stQueryConditionSetup: Semantics = semantic["stQueryConditionSetup"]
    stRequire: Semantics = semantic["stRequire"]
    stError: Semantics = semantic["stError"]
    stFindDataInTotal: Semantics = semantic["stFindDataInTotal"]
    stMinute: Semantics = semantic["stMinute"]
    stSecond: Semantics = semantic["stSecond"]
    stAlreadyExportToFile: Semantics = semantic["stAlreadyExportToFile"]
    stItemsCount: Semantics = semantic["stItemsCount"]
    stSucceed: Semantics = semantic["stSucceed"]
    stCombineTabulars: Semantics = semantic["stCombineTabulars"]
    stRowsMulColumns: Semantics = semantic["stRowsMulColumns"]
    stConfirmCombineTabular: Semantics = semantic["stConfirmCombineTabular"]
    stEmptyTabular: Semantics = semantic["stEmptyTabular"]
    stHasBeenRenamedToNew: Semantics = semantic["stHasBeenRenamedToNew"]
    stUnexpectedFileType: Semantics = semantic["stUnexpectedFileType"]
    stCombine: Semantics = semantic["stCombine"]
    stTimeCondition: Semantics = semantic["stTimeCondition"]
    stTabularSize: Semantics = semantic["stTabularSize"]
    stFrom: Semantics = semantic["stFrom"]
    stTo: Semantics = semantic["stTo"]
    stEnd: Semantics = semantic["stEnd"]
    stStart: Semantics = semantic["stStart"]
    stTooManyDatas: Semantics = semantic["stTooManyDatas"]
    stExportFailed: Semantics = semantic["stExportFailed"]
    stFetchAll: Semantics = semantic["stFetchAll"]
    stFilterQuery: Semantics = semantic["stFilterQuery"]
    stFigureSpaceViewer: Semantics = semantic["stFigureSpaceViewer"]
    stCacheTabularToWorkspace: Semantics = semantic["stCacheTabularToWorkspace"]
    stHasBeenRenamed: Semantics = semantic["stHasBeenRenamed"]
    stTabularSpaceViewer: Semantics = semantic["stTabularSpaceViewer"]
    stIsSureToDelete: Semantics = semantic["stIsSureToDelete"]
    stCopyToWorkspace: Semantics = semantic["stCopyToWorkspace"]
    stExportToFile: Semantics = semantic["stExportToFile"]
    stHasBeenDeleted: Semantics = semantic["stHasBeenDeleted"]
    stConfirmRemove: Semantics = semantic["stConfirmRemove"]
    stOkConfirm: Semantics = semantic["stOkConfirm"]
    stWarning: Semantics = semantic["stWarning"]
    stFetchTabularFromSpace: Semantics = semantic["stFetchTabularFromSpace"]
    stClearTabularSpace: Semantics = semantic["stClearTabularSpace"]
    stHasBeenRestored: Semantics = semantic["stHasBeenRestored"]
    stClearFigureSpace: Semantics = semantic["stClearFigureSpace"]
    stLeftBracket: Semantics = semantic["stLeftBracket"]
    stRightBracket: Semantics = semantic["stRightBracket"]
    stFetchFigureFromSpace: Semantics = semantic["stFetchFigureFromSpace"]
    stFetch: Semantics = semantic["stFetch"]
    stChinese: Semantics = semantic["stChinese"]
    stAlreadySelected: Semantics = semantic["stAlreadySelected"]
    stConfirmFetch: Semantics = semantic["stConfirmFetch"]
    stRemind: Semantics = semantic["stRemind"]
    stEnglish: Semantics = semantic["stEnglish"]
    stInfomation: Semantics = semantic["stInfomation"]
    stFigure: Semantics = semantic["stFigure"]
    stExportFigure: Semantics = semantic["stExportFigure"]
    stNaming: Semantics = semantic["stNaming"]
    stConfirm: Semantics = semantic["stConfirm"]
    stCacheFigureToWorkspace: Semantics = semantic["stCacheFigureToWorkspace"]
    stSelectAll: Semantics = semantic["stSelectAll"]
    stUnselected: Semantics = semantic["stUnselected"]
    stCureTestDate: Semantics = semantic["stCureTestDate"]
    stCureTestTime: Semantics = semantic["stCureTestTime"]
    stCureTestStandard: Semantics = semantic["stCureTestStandard"]
    stCureTestSpecimen: Semantics = semantic["stCureTestSpecimen"]
    stSubmittingClient: Semantics = semantic["stSubmittingClient"]
    stCureTestOperator: Semantics = semantic["stCureTestOperator"]
    stIsQualified: Semantics = semantic["stIsQualified"]
    stCureTestReport: Semantics = semantic["stCureTestReport"]
    stExportReport: Semantics = semantic["stExportReport"]
    stCureTestProcess: Semantics = semantic["stCureTestProcess"]
    stLanguageSetting: Semantics = semantic["stLanguageSetting"]
    stLanguage: Semantics = semantic["stLanguage"]
    stYes: Semantics = semantic["stYes"]
    stNo: Semantics = semantic["stNo"]
    stLogin: Semantics = semantic["stLogin"]
    stLabelIsEmpty: Semantics = semantic["stLabelIsEmpty"]
    stLabelAlreadyExist: Semantics = semantic["stLabelAlreadyExist"]
    stSignUp: Semantics = semantic["stSignUp"]
    stTemperaturePreparation: Semantics = semantic["stTemperaturePreparation"]
    stFrequencySweep: Semantics = semantic["stFrequencySweep"]
    stStrainSweep: Semantics = semantic["stStrainSweep"]
    stTemperatureSweep: Semantics = semantic["stTemperatureSweep"]
    stSulfurizationTest: Semantics = semantic["stSulfurizationTest"]
    stStressRelaxation: Semantics = semantic["stStressRelaxation"]
    stTemperatureAnalysis: Semantics = semantic["stTemperatureAnalysis"]
    stTimed: Semantics = semantic["stTimed"]
    stPreheating: Semantics = semantic["stPreheating"]
    stDelay: Semantics = semantic["stDelay"]
    stCombinedSweep: Semantics = semantic["stCombinedSweep"]
    stSubtestType: Semantics = semantic["stSubtestType"]
    stDuration: Semantics = semantic["stDuration"]
    stFrequency: Semantics = semantic["stFrequency"]
    stAt: Semantics = semantic["stAt"]
    stPressure: Semantics = semantic["stPressure"]
    stStrain: Semantics = semantic["stStrain"]
    stBasicUnitsSetting: Semantics = semantic["stBasicUnitsSetting"]
    stAboveTemperature: Semantics = semantic["stAboveTemperature"]
    stBelowTemperature: Semantics = semantic["stBelowTemperature"]
    stStrainDegree: Semantics = semantic["stStrainDegree"]
    stLabelMessageBoxTitle: Semantics = semantic["stLabelMessageBoxTitle"]
    stUser: Semantics = semantic["stUser"]
    stUserName: Semantics = semantic["stUserName"]
    stUserId: Semantics = semantic["stUserId"]
    stPassword: Semantics = semantic["stPassword"]
    stTime: Semantics = semantic["stTime"]
    stDegree: Semantics = semantic["stDegree"]
    stForce: Semantics = semantic["stForce"]
    stTemperature: Semantics = semantic["stTemperature"]
    stRole: Semantics = semantic["stRole"]
    stCreateFile: Semantics = semantic["stCreateFile"]
    stOpenFile: Semantics = semantic["stOpenFile"]
    stImageInsertFailed: Semantics = semantic["stImageInsertFailed"]
    stErrorInfo: Semantics = semantic["stErrorInfo"]
    stPasswordNotMacth: Semantics = semantic["stPasswordNotMacth"]
    stUidEmptyError: Semantics = semantic["stUidEmptyError"]
    stUidAlreadyExist: Semantics = semantic["stUidAlreadyExist"]
    stNameEmptyError: Semantics = semantic["stNameEmptyError"]
    stRoleValidError: Semantics = semantic["stRoleValidError"]
    stUidNotExist: Semantics = semantic["stUidNotExist"]
    stSubtestTypeError: Semantics = semantic["stSubtestTypeError"]
    stPasswordL8Error: Semantics = semantic["stPasswordL8Error"]
    stPasswordCharError: Semantics = semantic["stPasswordCharError"]
    stFileOccupied: Semantics = semantic["stFileOccupied"]
    stCureTestNumber: Semantics = semantic["stCureTestNumber"]
    stElasticTorque: Semantics = semantic["stElasticTorque"]
    stViscousTorque: Semantics = semantic["stViscousTorque"]
    stComplexTorque: Semantics = semantic["stComplexTorque"]
    stCureRate: Semantics = semantic["stCureRate"]
    stElasticModulus: Semantics = semantic["stElasticModulus"]
    stViscousModulus: Semantics = semantic["stViscousModulus"]
    stComplexModulus: Semantics = semantic["stComplexModulus"]
    stLossTangent: Semantics = semantic["stLossTangent"]
    stCureTestCondition: Semantics = semantic["stCureTestCondition"]
    stRate: Semantics = semantic["stRate"]
    stTorque: Semantics = semantic["stTorque"]
    stLength: Semantics = semantic["stLength"]
    stUnitless: Semantics = semantic["stUnitless"]
