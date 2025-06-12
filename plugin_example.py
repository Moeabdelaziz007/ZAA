 codex/resolve-merge-conflicts-and-update-tests
import math

class CalculatorPlugin:
    """Simple plugin to add two numeric values."""

    def execute(self, params):
        a = params.get("a")
        b = params.get("b")
        if a is None or b is None:
            raise ValueError("Missing arguments")
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numeric")
=======
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
 main
        result = a + b
        if math.isinf(result):
            raise OverflowError("Result out of range")
        if math.isnan(result):
 codex/resolve-merge-conflicts-and-update-tests
            raise ValueError("Invalid number")

            raise ValueError("Result is NaN")
 main
        return {"result": result}
