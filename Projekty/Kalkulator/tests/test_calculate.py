import pytest
from calculate import Calculator


def test_add():
    calc = Calculator()
    assert calc.calculate(2, 3, "+") == 5


def test_subtract():
    calc = Calculator()
    assert calc.calculate(10, 4, "-") == 6


def test_multiply():
    calc = Calculator()
    assert calc.calculate(3, 4, "*") == 12


def test_divide():
    calc = Calculator()
    assert calc.calculate(10, 2, "/") == 5


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.calculate(5, 0, "/")


def test_power():
    calc = Calculator()
    assert calc.calculate(2, 8, "^") == 256


def test_unknown_operation():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.calculate(2, 3, "?")


def test_history():
    calc = Calculator()
    calc.calculate(2, 3, "+")
    calc.calculate(10, 2, "/")
    assert len(calc.history) == 2
    assert "2 + 3 = 5" in calc.history[0]
