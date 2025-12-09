import sqlite3
from sqlite3 import Cursor
from typing import List, Union, Optional

from DeclarativeQt.Resource.FileTypes.RFileType import FilePath
from DeclarativeQt.Resource.Grammars.RGrammar import CommandFrame, ReferList, isEmpty, Grammar, ConditionList, \
    DtReferList, GIters, Equal, StrCommand
from DeclarativeQt.Resource.Strings.RString import Symbol, RString

DataType = str
FieldMark = Union[str, CommandFrame]


class SqlComposer:
    pNone: Symbol = ""
    pCommandGap: Symbol = " "
    pEnding: Symbol = ";"
    pItemGap: Symbol = ", "
    pAllFields: Symbol = "*"
    pAnd: Symbol = "and"
    pOr: Symbol = "or"
    pNull: Symbol = "null"
    dtINT: DataType = "integer"
    dtSTRING: DataType = "text"
    dtFLOAT: DataType = "real"
    opLastInsertRowid: StrCommand = "select last_insert_rowid();"

    def __init__(self, dbFilePath: FilePath = None):
        self._cmd = ""
        self._connection = None
        self._connected = False
        self._dbFilePath = None
        if dbFilePath:
            self._connection = sqlite3.connect(dbFilePath)
            self._connected = True
            self._dbFilePath = dbFilePath
        self.equalFrame: CommandFrame = lambda x, y: f"{x} = {y}"
        self.isFrame: CommandFrame = lambda x, y: f"{x} is {y}"
        self.unequalFrame: CommandFrame = lambda x, y: f"{x} != {y}"
        self.greaterFrame: CommandFrame = lambda x, y: f"{x} > {y}"
        self.lessFrame: CommandFrame = lambda x, y: f"{x} < {y}"
        self.atLeastFrame: CommandFrame = lambda x, y: f"{x} >= {y}"
        self.atMostFrame: CommandFrame = lambda x, y: f"{x} <= {y}"
        self.plusFrame: CommandFrame = lambda x, y: f"{x} + {y}"
        self.minusFrame: CommandFrame = lambda x, y: f"{x} - {y}"
        self.stringFrame: CommandFrame = lambda x: f"\'{x}\'"
        self.bracketFrame: CommandFrame = lambda x: f"({x})"
        self.maxFrame: CommandFrame = lambda x: f"max({x})"
        self.andFrame: CommandFrame = lambda x, y: f"{self.bracketFrame(x)} and {self.bracketFrame(y)}"
        self.orFrame: CommandFrame = lambda x, y: f"{self.bracketFrame(x)} or {self.bracketFrame(y)}"
        self.notFrame: CommandFrame = lambda x: f"not {self.bracketFrame(x)}"
        self.betweenAndFrame: CommandFrame = lambda x, a, b: f"{x} between {a} and {b}"
        self.limitFrame: CommandFrame = lambda x: f"limit {x}"
        self.likeFrame: CommandFrame = lambda x, y: f"{x} like \'%{y}%\'"
        self.leftLikeFrame: CommandFrame = lambda x, y: f"{x} like \'{y}%\'"
        self.rightLikeFrame: CommandFrame = lambda x, y: f"{x} like \'%{y}\'"
        self.joinDateTimeFrame: CommandFrame = lambda date, time: f"datetime({date} || \' \' || {time})"
        self.datetimeFrame: CommandFrame = lambda x: f"datetime({x})"
        self.coalesceFrame: CommandFrame = lambda x, d: f"coalesce({x}, {d})"
        self.orderByFrame: CommandFrame = lambda exp: f"order by {exp}"
        self.primaryKeyMark: FieldMark = "primary key"
        self.notNullMark: FieldMark = "not null"
        self.defaultNullMark: FieldMark = "default null"
        self.defaultMark: FieldMark = lambda value: f"default {value}"
        self.autoIncrementMark: FieldMark = "autoincrement"
        self.primaryKeyAutoIncrementMark: FieldMark = "primary key autoincrement"
        self._toStrList: Grammar = lambda items: ReferList(items, lambda x: str(x))
        self._itemsFrame: CommandFrame = lambda items: self.pItemGap.join(self._toStrList(items))
        self._bktItemsFrame: CommandFrame = lambda items: self.bracketFrame(self._itemsFrame(items))
        self._marksFrame: CommandFrame = lambda marks: self.pCommandGap.join(marks).strip()
        self._fieldFrame: CommandFrame = lambda name, tp, marks: f"{name} {tp} {self._marksFrame(marks)}".strip()
        self._createFrame: CommandFrame = lambda table, fields: f"create table if not exists {table} {fields}"
        self._updateFrame: CommandFrame = lambda table, equations: f"update {table} set {equations}"
        self._selectFrame: CommandFrame = lambda items, table: f"select {items} from {table}"
        self._whereFrame: CommandFrame = lambda cmd: f"where {cmd}"
        self._whereNotFrame: CommandFrame = lambda cmd: f"where not {self.bracketFrame(cmd)}"
        self._deleteFrame: CommandFrame = lambda table: f"delete from {table}"
        self._dropFrame: CommandFrame = lambda table: f"drop table if exists {table}"
        self._insertFrame: CommandFrame = lambda table, keys, values: f"insert into {table} {keys} values {values}"

    def linkConditions(self, *conditions, opt: str):
        opt = self.pCommandGap + opt + self.pCommandGap
        return opt.join(ReferList(conditions, lambda x: self.bracketFrame(x)))

    def cmdEnd(self):
        if isEmpty(self._cmd) or Equal(self._cmd[-1], self.pEnding):
            return self
        self._cmd += self.pEnding
        return self

    def cmdAppend(self, appendix: str, end: bool = True):
        prefix = self.pCommandGap if not isEmpty(self._cmd) else self.pNone
        appendix = appendix.rstrip(self.pEnding)
        self._cmd += str(prefix + appendix) if len(appendix) > 0 else self.pNone
        self._cmd += self.pEnding if end else self.pNone
        return self

    def whereNot(self, condition: str, end: bool = True):
        return self.where(self.notFrame(condition), end)

    def where(self, condition: str, end: bool = True):
        if isEmpty(self._cmd):
            return self
        self._cmd += str(self.pCommandGap + self._whereFrame(condition)) if len(condition) > 0 else self.pNone
        self._cmd += self.pEnding if end else self.pNone
        return self

    def insert(self, table: str, values: dict):
        if isEmpty(values) or isEmpty(table):
            return self
        lt_keys = self._bktItemsFrame(list(values.keys()))
        lt_values = self._bktItemsFrame(list(values.values()))
        self._cmd += self._insertFrame(table, keys=lt_keys, values=lt_values) + self.pEnding
        return self

    def dropTable(self, table: str):
        if isEmpty(table):
            return self
        self._cmd += self._dropFrame(table) + self.pEnding
        return self

    def createTable(self, table: str, fields: List[List[str]]):
        if isEmpty(table):
            return self
        lt_fields = ConditionList(fields, lambda x: len(x) > 1)
        lt_fields = ReferList(lt_fields, lambda x: self._fieldFrame(x[0], x[1], x[2:]))
        self._cmd += self._createFrame(table, self._bktItemsFrame(lt_fields)) + self.pEnding
        return self

    def deleteData(self, table: str):
        if isEmpty(table):
            return self
        self._cmd += self._deleteFrame(table)
        return self

    def update(self, table: str, values: dict):
        if isEmpty(values) or isEmpty(table):
            return self
        equations = self._itemsFrame(DtReferList(values, lambda k, v: self.equalFrame(k, v)))
        self._cmd += self._updateFrame(table, equations)
        return self

    def select(self, items: List[str], table: str):
        if isEmpty(items) or isEmpty(table):
            return self
        self._cmd += self._selectFrame(items=self._itemsFrame(items), table=table)
        return self

    @property
    def command(self):
        return self._cmd

    @property
    def dbFilePath(self):
        return self._dbFilePath

    def clear(self):
        self._cmd = self.pNone
        return self

    def isCommandEnded(self):
        return len(self._cmd) > 0 and self._cmd[-1] in GIters(self.pEnding)

    def commit(self, showLog: bool = True) -> bool:
        if not self._connected or not self.isCommandEnded():
            return False
        try:
            self._connection.commit()
            if showLog:
                RString.log(self._cmd)
            cursor = self._connection.cursor()
            cursor.execute(self._cmd)
            self._connection.commit()
        except sqlite3.Error as e:
            RString.log(str(e), RString.lgError)
            RString.log(str(self._cmd), RString.lgError)
            self._cmd = self.pNone
            return False
        self._cmd = self.pNone
        return True

    def fetchall(self, showLog: bool = True) -> Union[list, None]:
        if not self._connected or not self.isCommandEnded():
            return None
        try:
            self._connection.commit()
            if showLog:
                RString.log(self._cmd)
            cursor = self._connection.cursor()
            cursor.execute(self._cmd)
            datas = cursor.fetchall()
        except sqlite3.Error as e:
            RString.log(str(e), RString.lgError)
            RString.log(str(self._cmd), RString.lgError)
            self._cmd = self.pNone
            return None
        self._cmd = self.pNone
        return datas

    def execute(self, showLog: bool = True) -> Optional[Cursor]:
        if not self._connected or not self.isCommandEnded():
            return None
        try:
            self._connection.commit()
            if showLog:
                RString.log(self._cmd)
            cursor = self._connection.cursor()
            cursor.execute(self._cmd)
            self._connection.commit()
        except sqlite3.Error as e:
            RString.log(str(e), RString.lgError)
            RString.log(str(self._cmd), RString.lgError)
            self._cmd = self.pNone
            return None
        self._cmd = self.pNone
        return cursor

    def isConnected(self):
        return self._connected

    def connect(self, dbFilePath: str):
        self._connection = sqlite3.connect(dbFilePath)
        self._connected = True
        return self

    def close(self):
        self._connection.close()
        self._connection = None
        self._connected = False
        return self
