from abc import ABC
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from DeclarativeQt.Resource.Grammars.RGrammar import GList, Equal, isValid
from DeclarativeQt.Resource.Strings.RString import RString

MsrFactor = float
MsrBias = float
MsrSymbol = str
MsrArith = str


class MeasureUnit:
    pMul: MsrArith = "·"
    pInverse: MsrArith = "⁻¹"
    unit: MsrSymbol = "-"

    def __init__(self, symbol: MsrSymbol, value: MsrFactor, isBase: bool = True):
        self.symbol = symbol
        self.value = value
        self.isBase = isBase

    def __eq__(self, other):
        if not isinstance(other, MeasureUnit):
            return False
        return Equal(self.symbol, other.symbol)

    def __hash__(self):
        return self.symbol.__hash__()

    def __mul__(self, other):
        if not isinstance(other, MeasureUnit) or Equal(other.symbol, self.unit):
            return self
        if Equal(self.symbol, self.unit):
            return other
        return MeasureUnit(self.symbol + self.pMul + other.symbol, self.value * other.value, False)

    def __rmul__(self, other):
        if not isinstance(other, MeasureUnit) or Equal(other.symbol, self.unit):
            return self
        if Equal(self.symbol, self.unit):
            return other
        return MeasureUnit(other.symbol + self.pMul + self.symbol, other.value * self.value, False)

    def __truediv__(self, other):
        if not isinstance(other, MeasureUnit) or Equal(other.symbol, self.unit):
            return self
        rsymbol = RString.bracket(other.symbol) if not other.isBase else other.symbol
        rsymbol += self.pInverse
        return MeasureUnit(self.symbol + self.pMul + rsymbol, self.value / other.value, False)

    def __rtruediv__(self, other):
        if not isinstance(other, MeasureUnit):
            return self
        if Equal(self.symbol, self.unit):
            return other
        rsymbol = RString.bracket(self.symbol) if not self.isBase else self.symbol
        rsymbol += self.pInverse
        return MeasureUnit(other.symbol + self.pMul + rsymbol, other.value / self.value, False)


class PhyMeasure(ABC):
    PhyMark = "PhyMark"
    QuantityUnits = list()
    ExponentFrame = "1e-{}"
    DecimalRound = RString.DecimalRound
    DecimalPrecision = RString.DecimalPrecision

    def __eq__(self, other):
        if not isinstance(other, PhyMeasure):
            return False
        return Equal(self.PhyMark, other.PhyMark)

    def __hash__(self):
        return self.PhyMark.__hash__()

    @staticmethod
    def conversion(value: float, origin: MeasureUnit, target: MeasureUnit) -> Optional[float]:
        if not isValid(value):
            return None
        return PhyMeasure.decimalRound(value * origin.value / target.value)

    @staticmethod
    def decimalRound(value: float) -> float:
        decimal_val = Decimal(str(value))
        exponent = Decimal(PhyMeasure.ExponentFrame.format(PhyMeasure.DecimalPrecision))
        try:
            rounded = decimal_val.quantize(exponent, rounding=ROUND_HALF_UP)
        except Exception as e:
            RString.log(str(e), RString.lgError)
            return value
        return float(rounded)


class UnitlessMeasure(PhyMeasure):
    PhyMark = "Unitless"
    unit: MeasureUnit = MeasureUnit(MeasureUnit.unit, 1.0)
    QuantityUnits = GList(unit)


class RateMeasure(PhyMeasure):
    PhyMark = "Rate"
    ps: MeasureUnit = MeasureUnit("s⁻¹", 1.0, False)
    pmin: MeasureUnit = MeasureUnit("min⁻¹", 1.0 / 60.0, False)
    ph: MeasureUnit = MeasureUnit("h⁻¹", pmin.value / 60.0, False)
    pms: MeasureUnit = MeasureUnit("ms⁻¹", 1000.0, False)
    pps: MeasureUnit = MeasureUnit("%·s⁻¹", ps.value * 0.01, False)
    ppmin: MeasureUnit = MeasureUnit("%·min⁻¹", pmin.value * 0.01, False)
    pph: MeasureUnit = MeasureUnit("%·h⁻¹", ph.value * 0.01, False)
    ppms: MeasureUnit = MeasureUnit("%·ms⁻¹", pms.value * 0.01, False)
    QuantityUnits = GList(pps, ppmin, pph, ppms, ps, pmin, ph, pms)


class TorqueMeasure(PhyMeasure):
    PhyMark = "Torque"
    Nm: MeasureUnit = MeasureUnit("N·m", 1.0, False)
    kNm: MeasureUnit = MeasureUnit("kN·m", 1000.0, False)
    lbfft: MeasureUnit = MeasureUnit("lbf·ft", 1.35582, False)
    lbfin: MeasureUnit = MeasureUnit("lbf·in", 0.112985, False)
    QuantityUnits = GList(Nm, kNm, lbfin, lbfft)


class ForceMeasure(PhyMeasure):
    PhyMark = "Force"
    N: MeasureUnit = MeasureUnit("N", 1.0)
    kgf: MeasureUnit = MeasureUnit("kgf", 9.80665)
    gf: MeasureUnit = MeasureUnit("gf", kgf.value / 1000.0)
    lbf: MeasureUnit = MeasureUnit("lbf", 4.44822)
    kN: MeasureUnit = MeasureUnit("kN", 1000.0)
    QuantityUnits = GList(N, kN, kgf, lbf, gf)


class PressureMeasure(PhyMeasure):
    PhyMark = "Pressure"
    Pa: MeasureUnit = MeasureUnit("Pa", 1.0)
    kPa: MeasureUnit = MeasureUnit("kPa", 1000.0)
    MPa: MeasureUnit = MeasureUnit("MPa", kPa.value * 1000.0)
    psi: MeasureUnit = MeasureUnit("psi", 6894.76)
    xpsi: MeasureUnit = MeasureUnit("lbf·in⁻²", 6894.76, False)
    QuantityUnits = GList(Pa, kPa, MPa, psi, xpsi)


class TimeMeasure(PhyMeasure):
    PhyMark = "Time"
    hour: MeasureUnit = MeasureUnit("h", 3600.0)
    minute: MeasureUnit = MeasureUnit("min", 60.0)
    second: MeasureUnit = MeasureUnit("s", 1.0)
    millisecond: MeasureUnit = MeasureUnit("ms", 0.001)
    QuantityUnits = GList(hour, minute, second, millisecond)


class FrequencyMeasure(PhyMeasure):
    PhyMark = "Frequency"
    Hz: MeasureUnit = MeasureUnit("Hz", 1.0)
    kHz: MeasureUnit = MeasureUnit("kHz", 1000.0)
    MHz: MeasureUnit = MeasureUnit("MHz", 1000.0 * kHz.value)
    QuantityUnits = GList(Hz, kHz, MHz)


class LengthMeasure(PhyMeasure):
    PhyMark = "Length"
    meter: MeasureUnit = MeasureUnit("m", 1.0)
    km: MeasureUnit = MeasureUnit("km", 1000.0)
    cm: MeasureUnit = MeasureUnit("cm", 0.01)
    inch: MeasureUnit = MeasureUnit("in", 0.0254)
    foot: MeasureUnit = MeasureUnit("ft", 0.3048)
    QuantityUnits = GList(meter, km, cm, inch)


class DegreeMeasure(PhyMeasure):
    PhyMark = "Degree"
    Rad: MeasureUnit = MeasureUnit("rad", 1.0)
    piRad: MeasureUnit = MeasureUnit("πrad", 6.2832)
    Deg: MeasureUnit = MeasureUnit("deg°", 0.01745)
    QuantityUnits = GList(Rad, piRad, Deg)


class TemperatureMeasure(PhyMeasure):
    PhyMark = "Temperature"
    Celsius: MeasureUnit = MeasureUnit("℃", 1.0)
    Fahrenheit: MeasureUnit = MeasureUnit("℉", 1.8)
    QuantityUnits = GList(Celsius, Fahrenheit)
    FahrenheitBias: MsrBias = 32.0

    def celsiusToFahrenheit(self, temperature: float):
        fahrenheit = temperature * self.Fahrenheit.value + self.FahrenheitBias
        return PhyMeasure.decimalRound(fahrenheit)

    def fahrenheitToCelsius(self, temperature: float):
        celsius = float(temperature - self.FahrenheitBias) / self.Fahrenheit.value
        return PhyMeasure.decimalRound(celsius)

    @staticmethod
    def conversion(value: float, origin: MeasureUnit, target: MeasureUnit):
        if not isValid(value):
            return None
        measurement = TemperatureMeasure()
        celsius = measurement.Celsius.symbol
        fahrenheit = measurement.Fahrenheit.symbol
        if Equal(origin.symbol, celsius) and Equal(target.symbol, fahrenheit):
            return measurement.celsiusToFahrenheit(value)
        elif Equal(origin.symbol, fahrenheit) and Equal(target.symbol, celsius):
            return measurement.fahrenheitToCelsius(value)
        return PhyMeasure.decimalRound(value)
