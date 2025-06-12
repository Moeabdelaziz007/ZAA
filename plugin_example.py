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
        result = a + b
        if math.isinf(result):
            raise OverflowError("Result out of range")
        if math.isnan(result):
            raise ValueError("Invalid number")
        return {"result": result}
