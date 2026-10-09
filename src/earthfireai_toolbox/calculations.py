from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from pint import UnitRegistry
from pint.errors import DimensionalityError, UndefinedUnitError


GRAVITY = 9.80665
ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)


def finite(value, name="数值") -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name}必须是有限数字")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name}必须是有限数字")
    return number


def convert(value, from_unit: str, to_unit: str) -> dict:
    number = finite(value)
    try:
        result = (number * ureg(from_unit)).to(to_unit)
    except (DimensionalityError, UndefinedUnitError) as exc:
        raise ValueError(f"单位无法换算：{exc}") from exc
    return {"value": number, "from_unit": from_unit, "result": float(result.magnitude), "to_unit": str(result.units)}


def dimensions(left: str, right: str) -> dict:
    try:
        left_d = ureg(left).dimensionality
        right_d = ureg(right).dimensionality
    except (UndefinedUnitError, TypeError) as exc:
        raise ValueError(f"单位表达式无效：{exc}") from exc
    return {"consistent": left_d == right_d, "left": str(left_d), "right": str(right_d)}


def hydrostatic(density, density_unit: str, tvd, tvd_unit: str) -> dict:
    rho = finite(density, "密度") * ureg(density_unit)
    depth = finite(tvd, "真垂深") * ureg(tvd_unit)
    if rho.magnitude <= 0 or depth.magnitude <= 0:
        raise ValueError("密度和真垂深必须大于零")
    pressure = (rho.to("kg/m^3") * GRAVITY * ureg("m/s^2") * depth.to("m")).to("MPa")
    return {"pressure_mpa": float(pressure.magnitude), "gravity_m_s2": GRAVITY, "assumption": "恒密度；深度为真垂深"}


def gradient(density, density_unit: str) -> dict:
    rho = finite(density, "密度") * ureg(density_unit)
    if rho.magnitude <= 0:
        raise ValueError("密度必须大于零")
    value = (rho.to("kg/m^3") * GRAVITY * ureg("m/s^2")).to("MPa/m")
    imperial = value.to("psi/ft")
    return {"mpa_per_m": float(value.magnitude), "psi_per_ft": float(imperial.magnitude)}


def fit_csv(path: str | Path, header: bool = True) -> dict:
    rows = list(csv.reader(Path(path).read_text(encoding="utf-8-sig").splitlines()))
    if header and rows:
        rows = rows[1:]
    if len(rows) < 2 or len(rows) > 1000:
        raise ValueError("数据点必须为 2 到 1000 个")
    points = []
    for index, row in enumerate(rows, start=2 if header else 1):
        if len(row) != 2:
            raise ValueError(f"第 {index} 行必须正好两列")
        points.append((finite(row[0], f"第 {index} 行 X"), finite(row[1], f"第 {index} 行 Y")))
    data = np.asarray(points, dtype=float)
    if np.all(data[:, 0] == data[0, 0]):
        raise ValueError("所有 X 值相同，无法唯一确定直线斜率")
    if np.all(data[:, 1] == data[0, 1]):
        return {
            "points": len(data),
            "slope": 0.0,
            "intercept": float(data[0, 1]),
            "r2": 1.0,
            "rmse": 0.0,
        }
    matrix = np.column_stack((data[:, 0], np.ones(len(data))))
    slope, intercept = np.linalg.lstsq(matrix, data[:, 1], rcond=None)[0]
    predicted = slope * data[:, 0] + intercept
    residual = data[:, 1] - predicted
    ss_res = float(np.sum(residual ** 2))
    ss_tot = float(np.sum((data[:, 1] - np.mean(data[:, 1])) ** 2))
    r2 = 1 - ss_res / ss_tot
    result = {
        "points": len(data),
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
        "rmse": float(np.sqrt(np.mean(residual ** 2))),
    }
    if not all(math.isfinite(value) for key, value in result.items() if key != "points"):
        raise ValueError("拟合结果不是有限数值，请检查输入数据")
    return result
