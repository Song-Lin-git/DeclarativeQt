from typing import List, Any, Dict

from DeclarativeQt.Resource.Grammars.RGrammar import Validate, isEmpty, isValid
from DeclarativeQt.Resource.PhyMetrics.RPhyMetric import Measurements, MeasureUnit
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDatabase import DataField
from DeclarativeQt.Storage.SqliteDb.SqlDbKernel.SqlDbMethod import SqlDbMethod, DataTranslator, \
    SqlTableData
from DeclarativeQt.Storage.SqliteDb.SqlDbVariant.PhyDbKernel.PhyDatabase import PhyDatabase


class PhyDbMethod(SqlDbMethod):
    @staticmethod
    def fetchDbTableDataToAppMeasureUnit(
            phyDb: PhyDatabase, fields: List[DataField] = None,
            readyData: SqlTableData = None,
            appUnits: Dict[str, MeasureUnit] = None, translator: DataTranslator = None,
    ) -> SqlTableData:
        converted = list()
        dbQuantity = phyDb.fieldPhysicalQuantity
        dbMeasure = phyDb.fieldMeasureUnits
        appMeasure = Validate(appUnits, dict())
        measurements = Measurements.UnitPhyMeasureMap
        fields = Validate(fields, phyDb.dbFields)
        simpleFetch = SqlDbMethod.fetchSqlTable
        data = readyData if isValid(readyData) else simpleFetch(phyDb, fields, translator=translator)
        if isEmpty(data):
            return None
        for row in data.copy():
            rowData: List[Any] = list(row)
            for i, item in enumerate(rowData):
                if item is None:
                    continue
                field = fields[i]
                if field in dbQuantity and dbQuantity[field] in appMeasure:
                    dbUnit = dbMeasure[field]
                    appUnit = appMeasure[dbQuantity[field]]
                    measurement = measurements[dbUnit]
                    rowData[i] = measurement.conversion(item, dbUnit, appUnit)
            converted.append(tuple(rowData))
        return converted

    @staticmethod
    def convertAppRowDataToDbMeasureUnit(
            phyDb: PhyDatabase, appUnits: Dict[str, MeasureUnit] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        converted = kwargs.copy()
        dbQuantity = phyDb.fieldPhysicalQuantity
        dbMeasure = phyDb.fieldMeasureUnits
        appMeasure = Validate(appUnits, dict())
        measurements = Measurements.UnitPhyMeasureMap
        for field, arg in converted.items():
            if field in dbQuantity and dbQuantity[field] in appMeasure:
                if isinstance(arg, str):
                    arg = None if isEmpty(arg) else float(arg)
                dbUnit = dbMeasure[field]
                appUnit = appMeasure[dbQuantity[field]]
                measurement = measurements[dbUnit]
                converted[field] = measurement.conversion(arg, appUnit, dbUnit)
        return converted
