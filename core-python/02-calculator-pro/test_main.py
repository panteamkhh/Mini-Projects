"""Unit tests for the Calculator logic (UI is not tested here)."""

from main import Calculator


def test_add():
    assert Calculator.calculate(4, 5, "Add") == 9


def test_subtract():
    assert Calculator.calculate(10, 4, "Subtract") == 6


def test_multiply():
    assert Calculator.calculate(3, 3, "Multiply") == 9


def test_divide():
    assert Calculator.calculate(10, 2, "Divide") == 5


def test_divide_by_zero():
    assert Calculator.calculate(10, 0, "Divide") == "Cannot divide by zero"
