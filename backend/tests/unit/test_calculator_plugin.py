  <<<<<<< codex/resolve-merge-conflicts-in-files
import unittest
=======
 codex/remove-conflict-markers-and-refactor-tests
import unittest

from sss.plugin_example import CalculatorPlugin

  <<<<<<< codex/add-unit-tests-and-update-readme
   codex/add-unit-tests-and-update-readme
  import unittest
  from plugin_example import CalculatorPlugin, PluginRegistry, Agent
  >>>>>>> main

from sss.plugin_example import CalculatorPlugin

class TestCalculatorPlugin(unittest.TestCase):
    def test_addition(self):
        plugin = CalculatorPlugin()
        result = plugin.execute({'a': 5, 'b': 3})
          self.assertEqual(result, {'result': 8})

  <<<<<<< codex/resolve-merge-conflicts-in-files
  =======
    if __name__ == "__main__":
        unittest.main()
    =======
     codex/expand-tests-for-calculator-plugin-and-zerosystem
    import math
    import pytest

    from plugin_example import CalculatorPlugin

   main

    @pytest.fixture
    def plugin():
        return CalculatorPlugin()

   codex/remove-conflict-markers-and-refactor-tests
  class TestCalculatorPlugin(unittest.TestCase):
      def test_addition(self):
          plugin = CalculatorPlugin()
          result = plugin.execute({"a": 5, "b": 3})
          self.assertEqual(result, {"result": 8})


  if __name__ == "__main__":
      unittest.main()
  =======

    def test_addition_integers(plugin):
        assert plugin.execute({"a": 2, "b": 3})["result"] == 5


    def test_addition_floats(plugin):
        result = plugin.execute({"a": 2.5, "b": 3.5})["result"]
        assert math.isclose(result, 6.0)


    def test_addition_int_float_combinations(plugin):
        assert plugin.execute({"a": 2, "b": 3.5})["result"] == 5.5
        assert plugin.execute({"a": 2.5, "b": 3})["result"] == 5.5


    def test_extremely_large_integers(plugin):
        big = 10 ** 100
        assert plugin.execute({"a": big, "b": big})["result"] == big * 2


    def test_extremely_small_floats(plugin):
        result = plugin.execute({"a": 1e-308, "b": 1e-308})["result"]
        assert math.isclose(result, 2e-308)


    def test_float_overflow_raises(plugin):
        with pytest.raises(OverflowError):
            plugin.execute({"a": 1e308, "b": 1e308})


    def test_invalid_type_raises(plugin):
        with pytest.raises(TypeError):
            plugin.execute({"a": "1", "b": 1})


    def test_missing_argument_raises(plugin):
        with pytest.raises(ValueError):
            plugin.execute({"a": 1})


    def test_infinite_input(plugin):
        with pytest.raises(OverflowError):
            plugin.execute({"a": float("inf"), "b": 1})


    def test_nan_input(plugin):
        with pytest.raises(ValueError):
            plugin.execute({"a": float("nan"), "b": 1})
    >>>>>>> main
    =======
     codex/convert-unittest-to-pytest
    from sss.plugin_example import CalculatorPlugin


    def test_addition():
        plugin = CalculatorPlugin()
        result = plugin.execute({'a': 5, 'b': 3})
        assert result == {'result': 8}

    =======
    import os, sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    import unittest

    from plugin_example import CalculatorPlugin


    class TestCalculatorPlugin(unittest.TestCase):
        def test_addition(self):
            plugin = CalculatorPlugin()
            result = plugin.execute({"a": 5, "b": 3})
            self.assertEqual(result, {"result": 8})
     main
    <<<<<<< codex/add-unit-tests-and-update-readme
     main
    =======
      >>>>>> main
    >>>>>>> main
   main
  >>>>>>> main
