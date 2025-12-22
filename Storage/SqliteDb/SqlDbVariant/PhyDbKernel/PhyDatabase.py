from abc import abstractmethod
from typing import List, Dict, Any

from DeclarativeQt.Resource.FileTypes.RFileType import FilePath
from DeclarativeQt.Resource.PhyMetrics.RPhyMetric import MeasureUnit
from DeclarativeQt.Resource.Strings.RStr import NLIndex, RStr
from DeclarativeQt.Storage.SqliteDb.SqlComposer.SqlComposer import SqlComposer
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import SqlDatabase, FieldNLMap, \
    DataField, DBNaming, FieldDefine


class PhyDatabase(SqlDatabase):
    physicalUnitSuffix = RStr.pForwardSlash

    @property
    @abstractmethod
    def fieldPhysicalSymbols(self) -> Dict[DataField, str]:
        pass

    @property
    @abstractmethod
    def physicalFields(self) -> List[DataField]:
        pass

    @property
    @abstractmethod
    def fieldPhysicalQuantity(self) -> Dict[DataField, DataField]:
        pass

    @property
    @abstractmethod
    def fieldMeasureUnits(self) -> Dict[DataField, MeasureUnit]:
        pass

    @property
    @abstractmethod
    def dbFieldDefinitions(self) -> FieldDefine:
        pass

    @property
    @abstractmethod
    def dbStringFields(self) -> List[DataField]:
        pass

    @property
    @abstractmethod
    def dbPrimaryKeyField(self) -> DataField:
        pass

    @property
    @abstractmethod
    def isPrimaryKeyAuto(self) -> bool:
        pass

    @property
    @abstractmethod
    def sql(self) -> SqlComposer:
        pass

    @staticmethod
    @abstractmethod
    def dbFieldNLMap(index: NLIndex = RStr.EN, **kwargs: Any) -> FieldNLMap:
        pass

    @property
    @abstractmethod
    def dbFields(self) -> List[DataField]:
        pass

    @property
    @abstractmethod
    def dbTableName(self) -> DBNaming:
        pass

    @property
    @abstractmethod
    def dbFilePath(self) -> FilePath:
        pass
