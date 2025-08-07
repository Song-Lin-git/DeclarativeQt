from typing import List, Dict, Iterable, Optional

from DeclarativeQt.Resource.Grammars.RGrammar import GList, ReferList, Validate, isEmpty, LimitVal, DictData, Equal, \
    Key
from DeclarativeQt.Storage.SqliteDb.SqlComposer.SqlComposer import SqlComposer
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import SqlDatabase, DataField

DataTranslator = Dict[DataField, Dict[str, str]]
SqlTableData = Optional[List[Iterable]]


class BaseSqlDbMethod:
    @staticmethod
    def getTableFields(dbFile: str, tableName: str):
        sql = SqlComposer(dbFile)
        if not sql.isConnected():
            return None
        cursor = sql.select(GList(sql.pAllFields), tableName).cmdAppend(sql.limitFrame(0)).execute()
        return ReferList(cursor.description, lambda x: x[0])

    @staticmethod
    def getTableDatas(dbFile: str, tableName: str, fields: List[str] = None):
        sql = SqlComposer(dbFile)
        if not sql.isConnected():
            return None
        fields = Validate(fields, GList(sql.pAllFields))
        return sql.select(fields, tableName).cmdEnd().fetchall()


class SqlDbMethod:
    BaseMethod = BaseSqlDbMethod

    @staticmethod
    def fetchSqlTable(
            sqlDb: SqlDatabase, fields: List[DataField] = None,
            sort: bool = True, translator: DataTranslator = None
    ) -> SqlTableData:
        if sqlDb is None:
            return None
        sql = SqlComposer(sqlDb.dbFilePath)
        if not sql.isConnected():
            return None
        fields = Validate(fields, sqlDb.dbFields)
        sql.select(fields, sqlDb.dbTableName)
        if sort:
            sql.cmdAppend(sql.orderByFrame(sqlDb.fdSort))
        datas = sql.cmdEnd().fetchall()
        if translator is None or isEmpty(datas):
            return datas
        datas = ReferList(datas, lambda a0: list(a0))
        for field, mapping in translator.items():
            if field not in fields:
                continue
            idx = fields.index(field)
            translate = lambda a0: a0 if a0 not in mapping else mapping[a0]
            for row in datas:
                row[idx] = translate(row[idx])
        datas = ReferList(datas, lambda a0: tuple(a0))
        return datas

    @staticmethod
    def deleteDataRow(sqlDb: SqlDatabase, uniqueKey: dict):
        sql = SqlComposer(sqlDb.dbFilePath)
        locator = list()
        for k, v in uniqueKey.items():
            locator.append(sql.equalFrame(k, v))
        locator = sql.linkConditions(*locator, opt=sql.pAnd)
        order = sql.select(GList(sqlDb.fdSort), sqlDb.dbTableName).where(locator).fetchall()
        if isEmpty(order):
            return None
        order = order[0][0]
        result = sql.deleteData(sqlDb.dbTableName).where(locator).commit()
        if result:
            sql.update(sqlDb.dbTableName, DictData(
                Key(sqlDb.fdSort).Val(sql.minusFrame(sqlDb.fdSort, int(1)))
            ).data).where(sql.greaterFrame(sqlDb.fdSort, order)).commit()
        return None

    @staticmethod
    def rearrangeDataOrder(sqlDb: SqlDatabase, uniqueKey: dict, moveTo: int):
        sql = SqlComposer(sqlDb.dbFilePath)
        locator = list()
        for k, v in uniqueKey.items():
            locator.append(sql.equalFrame(k, v))
        locator = sql.linkConditions(*locator, opt=sql.pAnd)
        order = sql.select(GList(sqlDb.fdSort), sqlDb.dbTableName).where(locator).fetchall()
        if isEmpty(order):
            return None
        order = order[0][0]
        moveTo = LimitVal(moveTo, sqlDb.minValidOrder(), sqlDb.maxExistOrder(sql))
        if Equal(order, moveTo):
            return None
        if order > moveTo:
            sql.update(sqlDb.dbTableName, DictData(
                Key(sqlDb.fdSort).Val(sql.plusFrame(sqlDb.fdSort, int(1)))
            ).data).where(sql.andFrame(
                sql.atLeastFrame(sqlDb.fdSort, moveTo), sql.lessFrame(sqlDb.fdSort, order)
            )).commit()
        else:
            sql.update(sqlDb.dbTableName, DictData(
                Key(sqlDb.fdSort).Val(sql.minusFrame(sqlDb.fdSort, int(1)))
            ).data).where(sql.andFrame(
                sql.greaterFrame(sqlDb.fdSort, order), sql.atMostFrame(sqlDb.fdSort, moveTo)
            )).commit()
        sql.update(sqlDb.dbTableName, DictData(Key(sqlDb.fdSort).Val(moveTo)).data).where(locator).commit()
        return None
