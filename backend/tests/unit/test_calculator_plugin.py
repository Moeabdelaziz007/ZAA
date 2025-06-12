
@pytest.fixture
def plugin():
    return CalculatorPlugin()

  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
  @pytest.fixture
  def plugin():
      return CalculatorPlugin()


  def test_addition_integers(plugin):
      assert plugin.execute({"a": 2, "b": 3})["result"] == 5


  def test_addition_floats(plugin):
      result = plugin.ex  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
    import math
    import pytest
    =======
    import pytest
    from plugin_example import CalculatorPlugin
    >>>>>>> main
  ecute({"a": 2.5, "b": 3.5})["result"]
      assert math.isclose(result, 6.0)


  def test_invalid_type_raises(plugin):
      with pytest.raises(TypeError):
          plugin.execute({"a": "1", "b": 1})


  def test_missing_argument_raises(plugin):
      with pytest.raises(ValueError):
          plugin.execute({"a": 1})
  =======
  def test_addition(plugin):
      assert plugin.execute({"a": 2, "b": 3})["result"] == 5

  def test_invalid_type(plugin):
      with pytest.raises(TypeError):
          plugin.execute({"a": "1", "b": 2})
  >>>>>>> main
