from typing import Dict, Callable

from DeclarativeQt.Resource.Grammars.RGrammar import DictData, Key, DictToDefault, ReferList, Equal
from DeclarativeQt.Resource.PhyMetrics.PhyMtrBase import PhyMtrBase
from DeclarativeQt.Resource.PhyMetrics.PhyMtrBase.PhyMtrBase import MeasureUnit, PhyMeasure, MsrSymbol
from DeclarativeQt.Resource.Strings.RStr import Symbol


class PhySymbols:
    pStrain: Symbol = "ε"
    pStrainDegree: Symbol = "γ"
    pAboveTemperature: Symbol = "AT"
    pBelowTemperature: Symbol = "BT"
    pTime: Symbol = "t"
    pFrequency: Symbol = "f"
    pCureRate: Symbol = "CR"
    pLossTangent: Symbol = "ΔTAN"
    pElasticTorque: Symbol = "S\'"
    pViscousTorque: Symbol = "S\'\'"
    pComplexTorque: Symbol = "S*"
    pElasticModulus: Symbol = "G\'"
    pViscousModulus: Symbol = "G\'\'"
    pComplexModulus: Symbol = "G*"


class PhyQuantity:
    Force = PhyMtrBase.ForceMeasure()
    Pressure = PhyMtrBase.PressureMeasure()
    Temperature = PhyMtrBase.TemperatureMeasure()
    Time = PhyMtrBase.TimeMeasure()
    Frequency = PhyMtrBase.FrequencyMeasure()
    Unitless = PhyMtrBase.UnitlessMeasure()
    Degree = PhyMtrBase.DegreeMeasure()
    Torque = PhyMtrBase.TorqueMeasure()
    Length = PhyMtrBase.LengthMeasure()
    Rate = PhyMtrBase.RateMeasure()


class Measurements:
    Force = PhyQuantity.Force
    Pressure = PhyQuantity.Pressure
    Temperature = PhyQuantity.Temperature
    Time = PhyQuantity.Time
    Frequency = PhyQuantity.Frequency
    Degree = PhyQuantity.Degree
    Length = PhyQuantity.Length
    Rate = PhyQuantity.Rate
    Torque = PhyQuantity.Torque
    Unitless = PhyQuantity.Unitless
    Unit: Callable = lambda: MeasureUnit(MeasureUnit.unit, 1.0)

    @staticmethod
    def conversion(value: float, origin: MeasureUnit, target: MeasureUnit):
        quantity = Measurements.UnitPhyMeasureMap[origin]
        if not Equal(quantity, Measurements.UnitPhyMeasureMap[target]):
            return value
        return quantity.conversion(value, origin, target)

    @staticmethod
    def getMeasureUnit(symbol: str) -> MeasureUnit:
        unitMap = DictToDefault(Measurements.MeasureSymbolUnitMap, defaultExp=Measurements.Unit)
        return unitMap[symbol]

    @staticmethod
    def switchMeasureUnit(measureUnit: MeasureUnit) -> MeasureUnit:
        measurement = Measurements.UnitPhyMeasureMap[measureUnit]
        units = measurement.QuantityUnits
        idx = units.index(measureUnit)
        return units[int(idx + 1) % len(units)]

    UnitPhyMeasureMap: Dict[MeasureUnit, PhyMeasure] = DictData(
        *ReferList(Force.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Force)),
        *ReferList(Pressure.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Pressure)),
        *ReferList(Time.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Time)),
        *ReferList(Frequency.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Frequency)),
        *ReferList(Temperature.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Temperature)),
        *ReferList(Degree.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Degree)),
        *ReferList(Length.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Length)),
        *ReferList(Torque.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Torque)),
        *ReferList(Rate.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Rate)),
        *ReferList(Unitless.QuantityUnits, lambda a0: Key(a0).Val(PhyQuantity.Unitless)),
    ).data
    MeasureSymbolUnitMap: Dict[MsrSymbol, MeasureUnit] = DictData(
        Key(Force.N.symbol).Val(Force.N),
        Key(Force.kgf.symbol).Val(Force.kgf),
        Key(Force.kN.symbol).Val(Force.kN),
        Key(Force.lbf.symbol).Val(Force.lbf),
        Key(Force.gf.symbol).Val(Force.gf),
        Key(Pressure.Pa.symbol).Val(Pressure.Pa),
        Key(Pressure.kPa.symbol).Val(Pressure.kPa),
        Key(Pressure.psi.symbol).Val(Pressure.psi),
        Key(Pressure.xpsi.symbol).Val(Pressure.xpsi),
        Key(Pressure.MPa.symbol).Val(Pressure.MPa),
        Key(Temperature.Celsius.symbol).Val(Temperature.Celsius),
        Key(Temperature.Fahrenheit.symbol).Val(Temperature.Fahrenheit),
        Key(Time.second.symbol).Val(Time.second),
        Key(Time.hour.symbol).Val(Time.hour),
        Key(Time.minute.symbol).Val(Time.minute),
        Key(Time.millisecond.symbol).Val(Time.millisecond),
        Key(Frequency.Hz.symbol).Val(Frequency.Hz),
        Key(Frequency.kHz.symbol).Val(Frequency.kHz),
        Key(Frequency.MHz.symbol).Val(Frequency.MHz),
        Key(Degree.Rad.symbol).Val(Degree.Rad),
        Key(Degree.piRad.symbol).Val(Degree.piRad),
        Key(Degree.Deg.symbol).Val(Degree.Deg),
        Key(Length.meter.symbol).Val(Length.meter),
        Key(Length.km.symbol).Val(Length.km),
        Key(Length.cm.symbol).Val(Length.cm),
        Key(Length.inch.symbol).Val(Length.inch),
        Key(Length.foot.symbol).Val(Length.foot),
        Key(Torque.Nm.symbol).Val(Torque.Nm),
        Key(Torque.kNm.symbol).Val(Torque.kNm),
        Key(Torque.lbfft.symbol).Val(Torque.lbfft),
        Key(Torque.lbfin.symbol).Val(Torque.lbfin),
        Key(Rate.ps.symbol).Val(Rate.ps),
        Key(Rate.pps.symbol).Val(Rate.pps),
        Key(Rate.pms.symbol).Val(Rate.pms),
        Key(Rate.ppms.symbol).Val(Rate.ppms),
        Key(Rate.pmin.symbol).Val(Rate.pmin),
        Key(Rate.ppmin.symbol).Val(Rate.ppmin),
        Key(Rate.ph.symbol).Val(Rate.ph),
        Key(Rate.pph.symbol).Val(Rate.pph),
        Key(Unitless.unit.symbol).Val(Unitless.unit)
    ).data
