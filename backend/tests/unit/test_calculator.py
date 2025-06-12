from plugin_example import CalculatorPlugin


def test_calculator_adds_numbers():
    plugin = CalculatorPlugin()
    result = plugin.execute({"a": 5, "b": 3})
    assert result == {"result": 8}
