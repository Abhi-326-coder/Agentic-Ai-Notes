import pytest
from tools.calculator import calculator
from tools.time_tool import get_current_time
from tools.registry import TOOLS
from tools.executor import execute_tool

# to run the tests : python -m pytest


def test_calculator_addition():
    assert calculator("10 + 20") == 30


def test_calculator_multiplication():
    assert calculator("25 * 4") == 100


def test_calculator_division():
    assert calculator("100 / 5") == 20


def test_time_tool():
    result = get_current_time()

    assert isinstance(result, str)
    assert len(result) > 0
    
def test_calculator_through_registry():
    result = execute_tool(
        "calculator",
        {"expression": "10 + 20"}
    )

    assert result == 30


def test_time_through_registry():
    result = execute_tool(
        "time",
        {}
    )

    assert isinstance(result, str)
    
def test_unknown_tool():
    with pytest.raises(ValueError):
        execute_tool(
            "unknown_tool",
            {}
        )