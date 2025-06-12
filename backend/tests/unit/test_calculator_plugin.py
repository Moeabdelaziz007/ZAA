import pytest
from plugin_example import CalculatorPlugin

@pytest.fixture
def plugin():
    return CalculatorPlugin()

def test_addition(plugin):
    assert plugin.execute({"a": 2, "b": 3})["result"] == 5

def test_invalid_type(plugin):
    with pytest.raises(TypeError):
        plugin.execute({"a": "1", "b": 2})
