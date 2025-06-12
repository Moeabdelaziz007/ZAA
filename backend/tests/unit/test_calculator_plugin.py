import math
import pytest
from plugin_example import CalculatorPlugin

@pytest.fixture
def plugin():
    return CalculatorPlugin()

def test_addition_integers(plugin):
    assert plugin.execute({"a": 2, "b": 3})["result"] == 5

def test_addition_floats(plugin):
    result = plugin.execute({"a": 2.5, "b": 3.5})["result"]
    assert math.isclose(result, 6.0)

def test_invalid_type_raises(plugin):
    with pytest.raises(TypeError):
        plugin.execute({"a": "1", "b": 1})

def test_missing_argument_raises(plugin):
    with pytest.raises(ValueError):
        plugin.execute({"a": 1})
