import os
import sys

# Ensure the repository root is on the path when tests run
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from plugin_example import CalculatorPlugin


def test_calculator_adds_numbers():
    plugin = CalculatorPlugin()
    result = plugin.execute({"a": 5, "b": 3})
    assert result == {"result": 8}
