"""
Unit tests for the calculation logic in main.py.

Only the Calculator class is tested here (pure logic, no UI).
The HistoryManager and CalculatorApp (tkinter UI) are not covered
by automated tests in this file.
"""

import pytest

from main import Calculator


class TestCalculatorAdd:
    def test_add_positive_numbers(self):
        assert Calculator.calculate(2, 3, "Add") == 5

    def test_add_negative_numbers(self):
        assert Calculator.calculate(-2, -3, "Add") == -5

    def test_add_with_zero(self):
        assert Calculator.calculate(5, 0, "Add") == 5


class TestCalculatorSubtract:
    def test_subtract_positive_numbers(self):
        assert Calculator.calculate(5, 3, "Subtract") == 2

    def test_subtract_resulting_in_negative(self):
        assert Calculator.calculate(3, 5, "Subtract") == -2


class TestCalculatorMultiply:
    def test_multiply_positive_numbers(self):
        assert Calculator.calculate(4, 3, "Multiply") == 12

    def test_multiply_by_zero(self):
        assert Calculator.calculate(4, 0, "Multiply") == 0

    def test_multiply_negative_numbers(self):
        assert Calculator.calculate(-4, 3, "Multiply") == -12


class TestCalculatorDivide:
    def test_divide_positive_numbers(self):
        assert Calculator.calculate(10, 2, "Divide") == 5

    def test_divide_resulting_in_float(self):
        assert Calculator.calculate(5, 2, "Divide") == 2.5

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            Calculator.calculate(5, 0, "Divide")


class TestCalculatorInvalidOperation:
    def test_invalid_operation_raises(self):
        with pytest.raises(ValueError):
            Calculator.calculate(1, 2, "Modulo")

    def test_empty_operation_raises(self):
        with pytest.raises(ValueError):
            Calculator.calculate(1, 2, "")