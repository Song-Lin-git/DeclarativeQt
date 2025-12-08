from abc import ABC, abstractmethod
from typing import Dict, List, Self, Optional, Any

from DeclarativeQt.Resource.FileTypes.RFileType import FilePath
from DeclarativeQt.Resource.Grammars.RGrammar import GList, Validate, isEmpty, LimitVal, Key, DtReferDict, \
    DictData, ReferList, DictToDefault
from DeclarativeQt.Resource.Strings.RString import NLIndex, RString
from DeclarativeQt.Storage.SqliteDb.SqlComposer.SqlComposer import SqlComposer

FieldNLMap = Dict[str, str]
DataField = str
FieldDefine = List[List[str]]
DBNaming = str
SortOrder = int


class SqlDatabase(ABC):
    fdSort: DataField = "sorting"
    baseOrder: SortOrder = int(-1)

    @staticmethod
    @abstractmethod
    def dbFieldNLMap(index: NLIndex = RString.EnglishIndex) -> FieldNLMap:
        pass

    @property
    @abstractmethod
    def sql(self) -> SqlComposer:
        pass

    @property
    @abstractmethod
    def dbFieldDefinitions(self) -> FieldDefine:
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
    def isPrimaryKeyString(self) -> bool:
        return self.dbPrimaryKeyField in self.dbStringFields

    def reconnectSqlDb(self) -> Self:
        self.sql.connect(self.dbFilePath)
        return self

    def standardSqlRowData(self, sql: SqlComposer = None, **kwargs: Any):
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return kwargs
        dataWash = lambda a0: sql.pNull if a0 is None else a0
        kwargs = DtReferDict(kwargs, keyExp=lambda k, v: k, valExp=lambda k, v: dataWash(v))
        dataFrame = lambda k, v: sql.stringFrame(v) if k in self.dbStringFields else v
        kwargs = DtReferDict(kwargs, keyExp=lambda k, v: k, valExp=lambda k, v: dataFrame(k, v))
        kwargs = DictToDefault(kwargs, defaultVal=sql.pNull)
        return kwargs

    def insertSqlRowData(self, order: int = None, sql: SqlComposer = None, **kwargs: Any) -> Self:
        isAutoKey = self.isPrimaryKeyAuto
        if not isAutoKey and self.dbPrimaryKeyField not in kwargs:
            return self
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return self
        max_order = self.maxValidOrder(sql)
        order = max_order if order is None else LimitVal(order, self.minValidOrder(), max_order)
        row_key = kwargs[self.dbPrimaryKeyField] if not isAutoKey else None
        kwargs = self.standardSqlRowData(sql, **kwargs)
        kvPair = lambda k: Key(k).Val(kwargs[k])
        if not sql.insert(self.dbTableName, values=DictData(
                *ReferList(self.dbFields, lambda a0: kvPair(a0)), Key(self.fdSort).Val(order)
        ).data).commit():
            return self
        last_id = row_key if not isAutoKey else sql.cmdAppend(sql.opLastInsertRowid).fetchall()[0][0]
        if self.isPrimaryKeyString:
            last_id = sql.stringFrame(last_id)
        sql.update(self.dbTableName, values=DictData(
            Key(self.fdSort).Val(sql.plusFrame(self.fdSort, int(1)))
        ).data).where(sql.andFrame(
            sql.atLeastFrame(self.fdSort, order),
            sql.unequalFrame(self.dbPrimaryKeyField, last_id)
        )).commit()
        return self

    def updateSqlRowData(self, key: Any = None, sql: SqlComposer = None, **kwargs: Any) -> Self:
        if key is None:
            return self
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return self
        if self.isPrimaryKeyString:
            key = sql.stringFrame(key)
        kwargs = self.standardSqlRowData(sql, **kwargs)
        sql.update(self.dbTableName, values=kwargs).where(
            condition=sql.equalFrame(self.dbPrimaryKeyField, key)
        ).commit()
        return self

    def createSqlTable(self, sql: SqlComposer = None) -> Self:
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return self
        sql.createTable(self.dbTableName, fields=self.dbFieldDefinitions).cmdEnd().commit()
        return self

    def rebuildSqlTable(self, sql: SqlComposer = None) -> Self:
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return self
        sql.dropTable(self.dbTableName).cmdEnd().commit()
        self.createSqlTable(sql)
        return self

    def maxExistOrder(self, sql: SqlComposer = None) -> Optional[int]:
        sql = Validate(sql, self.sql)
        if not sql.isConnected():
            return None
        order = sql.select(GList(sql.maxFrame(self.fdSort)), self.dbTableName).cmdEnd().fetchall()
        return None if isEmpty(order) else order[0][0]

    def maxValidOrder(self, sql: SqlComposer = None) -> int:
        return Validate(self.maxExistOrder(sql), self.baseOrder) + int(1)

    def minValidOrder(self) -> int:
        return self.baseOrder + int(1)

    DbFields: List[DataField] = list()
    DbTableName: DBNaming = str()
    DbFilePath: FilePath = str()
