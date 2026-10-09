from pathlib import Path
import math
import tempfile
import unittest

from earthfireai_toolbox.calculations import convert, dimensions, fit_csv, gradient, hydrostatic


class CalculationTests(unittest.TestCase):
    def test_conversion_and_dimensions(self):
        self.assertAlmostEqual(convert(10, "bar", "MPa")["result"], 1.0, places=9)
        self.assertTrue(dimensions("kg/m^3*m/s^2*m", "Pa")["consistent"])
        self.assertFalse(dimensions("m", "s")["consistent"])

    def test_hydrostatic_and_gradient(self):
        self.assertAlmostEqual(hydrostatic(1.10, "g/cm^3", 3000, "m")["pressure_mpa"], 32.361945, places=6)
        self.assertAlmostEqual(gradient(1.10, "g/cm^3")["mpa_per_m"], 0.010787315, places=9)

    def test_fit_csv(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sample.csv"
            path.write_text("x,y\n0,1\n1,3\n2,5\n", encoding="utf-8")
            result = fit_csv(path)
            self.assertAlmostEqual(result["slope"], 2.0)
            self.assertAlmostEqual(result["intercept"], 1.0)
            self.assertAlmostEqual(result["r2"], 1.0)

    def test_fit_csv_rejects_constant_x(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "constant-x.csv"
            path.write_text("x,y\n1,2\n1,3\n1,4\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "X 值相同"):
                fit_csv(path)

    def test_fit_csv_constant_y_uses_finite_standard_json_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "constant-y.csv"
            path.write_text("x,y\n0,3\n1,3\n2,3\n", encoding="utf-8")
            result = fit_csv(path)
            self.assertEqual(result["r2"], 1.0)
            self.assertTrue(all(math.isfinite(value) for value in result.values()))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): hydrostatic(1, "g/cm^3", 0, "m")
        with self.assertRaises(ValueError): convert(float("nan"), "bar", "MPa")


if __name__ == "__main__": unittest.main()

