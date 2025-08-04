from abc import abstractmethod
from typing import List, Self, Any, Dict

from DeclarativeQt.Resource.FileTypes.RFileType import FilePath
from DeclarativeQt.Resource.Grammars.RGrammar import Validate
from DeclarativeQt.Resource.Strings.RString import NLIndex, RString
from DeclarativeQt.Storage.RStorage import RStorage
from DeclarativeQt.Storage.SqliteDb.SqlComposer.SqlComposer import SqlComposer
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import SqlDatabase, DBNaming, DataField, \
    FieldNLMap, FieldDefine
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDbMethod import SqlTableData


class RptDatabase(SqlDatabase):
    fdAutoId: DataField = "id"

    @property
    @abstractmethod
    def dbParamFields(self) -> List[DataField]:
        pass

    @property
    @abstractmethod
    def defaultRptParams(self) -> Dict[DataField, Any]:
        pass

    @abstractmethod
    def initRptParams(self) -> Self:
        pass

    @abstractmethod
    def fetchRptParams(self) -> Any:
        pass

    @abstractmethod
    def actRequestRptParams(self, *args: Any, **kwargs: Any) -> bool:
        pass

    @abstractmethod
    def updateRptParams(self, *args: Any, **kwargs: Any) -> Self:
        pass

    def fecthRptTableData(self, sql: SqlComposer = None) -> SqlTableData:
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return None
        return sql.select(self.dbParamFields, self.dbTableName).cmdEnd().fetchall()

    def updateRptTableData(self, sql: SqlComposer = None, **kwargs: Any) -> Self:
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return None
        kwargs = self.standardSqlRowData(sql=sql, **kwargs)
        sql.update(self.dbTableName, values=kwargs).cmdEnd().commit()
        return self

    @property
    def isPrimaryKeyAuto(self) -> bool:
        return True

    @property
    def dbPrimaryKeyField(self) -> DataField:
        return self.fdAutoId

    @property
    @abstractmethod
    def dbStringFields(self) -> List[DataField]:
        pass

    @property
    @abstractmethod
    def sql(self) -> SqlComposer:
        pass

    @property
    @abstractmethod
    def dbFieldDefinitions(self) -> FieldDefine:
        pass

    @staticmethod
    @abstractmethod
    def dbFieldNLMap(index: NLIndex = RString.EnglishIndex) -> FieldNLMap:
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

    DbFileDirAt = RStorage().getDir(RStorage.dirAppSetting)
