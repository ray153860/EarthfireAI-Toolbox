# EarthfireAI Toolbox

一组面向学习与基础工程校核的确定性工具。当前公开候选版本包含单位换算、量纲检查、静液柱压差、静态压力梯度和两列 CSV 直线拟合。数值由程序计算，不由语言模型猜测。

## 已实现

- Pint 单位换算和量纲一致性检查。
- 恒密度假设下 `ΔP = ρgh`。
- 静态压力梯度 `dP/dz = ρg`。
- 两列 CSV 的带截距普通最小二乘直线拟合，输出斜率、截距、R² 与 RMSE。
- 命令行 JSON 输出，便于其他 AI 或程序调用。

## 安装

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

本版本要求 Python 3.12 或更高版本。以上命令会把依赖安装到项目自己的虚拟环境中。

## 示例

```powershell
.\.venv\Scripts\earthfire-toolbox.exe convert 10 bar MPa
.\.venv\Scripts\earthfire-toolbox.exe dimensions "kg/m^3*m/s^2*m" Pa
.\.venv\Scripts\earthfire-toolbox.exe hydrostatic 1.10 "g/cm^3" 3000 m
.\.venv\Scripts\earthfire-toolbox.exe gradient 1.10 "g/cm^3"
.\.venv\Scripts\earthfire-toolbox.exe fit-csv .\examples\linear_sample.csv
```

## 测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 适用边界

- 静液柱计算假设密度恒定，深度必须是真垂深。
- 不自动推断表压/绝压、深度基准、温度或多相流影响。
- 直线拟合不自动删除异常点，也不证明模型适用于实际实验。
- 两列 CSV 的 X 值必须至少包含两个不同数值；全部相同时斜率无法唯一确定，程序会明确报错。
- JSON 输出只包含有限数值，不输出非标准的 `NaN` 或无穷值。
- 结果用于学习和复核；工程决策应核对标准、方法范围、输入单位和原始数据。

## 未包含

OCR、下载器、复杂网页读取、商业软件、ANSYS、专业模拟器和未通过验证的候选工具均未打包。

## 许可证

原创代码采用 Apache-2.0，见 `LICENSE`。
