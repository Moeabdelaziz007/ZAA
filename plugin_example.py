"""Simple calculator plugin used for tests."""
import math


class CalculatorPlugin:
    """Plugin that adds two numbers."""

    def execute(self, params):
        if not isinstance(params, dict):
            raise TypeError("params must be a dict")
        if "a" not in params or "b" not in params:
            raise ValueError("Missing arguments")
        a, b = params["a"], params["b"]
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("a and b must be numbers")
        result = a + b
        if math.isinf(result):
            raise OverflowError("Result out of range")
        if math.isnan(result):
            raise ValueError("Result is NaN")
        return {"result": result}
